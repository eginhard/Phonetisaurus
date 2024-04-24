# Dockerfile
# Pierre-André Noël, May 12th 2020
# Copyright © Element AI Inc. All rights reserved.
# Enno Hermann, 2024
# Apache License, Version 2.0
#
# Adapted from:
# https://github.com/kylebgorman/pynini/blob/7cf70e88733bd8dffdf132f7017769b44b91a67b/third_party/Dockerfile
#
# This builds `manylinux_2_28_x86_64` Python wheels for `phonetisaurus`, wrapping
# all its dependencies.
#
# This Dockerfile uses multi-stage builds; for more information, see:
# https://docs.docker.com/develop/develop-images/multistage-build/
#
# To build wheels, run:
#
#     docker build --rm --target=run-tests -t build-phonetisaurus-wheels .
#
# To extract the resulting wheels from the Docker image, run:
#
#     docker run --rm -v `pwd`:/io build-phonetisaurus-wheels cp -r /wheelhouse /io
#
# Notice that this also generates Cython wheels.
#
# Then, `twine` (https://twine.readthedocs.io/en/latest/) can be used to
# publish the resulting Phonetisaurus wheels.

# ******************************************************
# *** All the following images are based on this one ***
# ******************************************************
from quay.io/pypa/manylinux_2_28_x86_64 AS common

# The versions we want in the wheels.
ENV FST_VERSION "1.7.2"
ENV PHONETISAURUS_REV "master"

# ***********************************************************************
# *** Image providing all the requirements for building Phonetisaurus wheels ***
# ***********************************************************************
FROM common AS wheel-building-env

# Location of OpenFst and Phonetisaurus.
ENV FST_DOWNLOAD_PREFIX "https://www.openfst.org/twiki/pub/FST/FstDownload"
ENV PHONETISAURUS_GIT "https://github.com/eginhard/Phonetisaurus.git"

# Python used for compiling
ENV PYBIN "/opt/python/cp312-cp312/bin"

# Note that our certificates are not known to the version of wget available in this image.

# Install mitlm
RUN yum install -y autoconf-archive
RUN mkdir -p /src && cd /src \
    && git clone https://github.com/mitlm/mitlm.git \
    && cd mitlm \
    && sed -i 's/AX_CXX/#AX_CXX/g' configure.ac \
    && ./autogen.sh \
    && CFLAGS="-fPIC" ./configure --prefix=$PWD/usr --disable-shared \
    && make -j $(nproc) && make install \
    && export LD_LIBRARY_PATH=$PWD/usr/lib:$LD_LIBRARY_PATH

# Gets and unpack OpenFst source.
RUN yum install -y wget
RUN cd /tmp \
    && wget -q --no-check-certificate "${FST_DOWNLOAD_PREFIX}/openfst-${FST_VERSION}.tar.gz" \
    && tar -xzf "openfst-${FST_VERSION}.tar.gz" \
    && rm "openfst-${FST_VERSION}.tar.gz"

# Compiles OpenFst.
RUN cd "/tmp/openfst-${FST_VERSION}" \
    && CFLAGS="-fPIC" ./configure --with-pic --enable-static --disable-shared --enable-far --enable-ngram-fsts \
    && make -j $(nproc) && make install \
    && rm -rd "/tmp/openfst-${FST_VERSION}"

# Compile Phonetisaurus with bindings
RUN yum install -y epel-release python3-pip
RUN "${PYBIN}/python" -m pip install pybindgen
RUN cd /src && git clone "${PHONETISAURUS_GIT}" \
    && cd Phonetisaurus && git checkout -b build "origin/${PHONETISAURUS_REV}" \
    && CFLAGS="-fPIC" PYTHON="${PYBIN}/python" ./configure --enable-python --disable-static --enable-shared \
    && make -j $(nproc) && make install \
    && cp .libs/Phonetisaurus.so python/phonetisaurus \
    && cd python && mkdir bin && cp ../src/scripts/phonetisaurus-* bin/ \
    && mkdir phonetisaurus/bin \
    && cp ../rnnlm ../phonetisaurus-* /src/mitlm/usr/bin/* phonetisaurus/bin \
    && "${PYBIN}/pip" install . \
    && "${PYBIN}/python" -c "import phonetisaurus" \
    && cd script && PATH="${PYBIN}:/src/mitlm/usr/bin:${PATH}" ./e2e_test.sh

# # **********************************************************
# # *** Image making Phonetisaurus wheels (placed in /wheelhouse) ***
# # **********************************************************
FROM wheel-building-env AS build-wheels

# Compiles the wheels to a temporary directory.
RUN "${PYBIN}/pip" wheel -v "/src/Phonetisaurus/python" -w "/tmp/wheelhouse"

# Bundles external shared libraries into the wheels.
# See https://github.com/pypa/manylinux/tree/manylinux2014
RUN auditwheel repair /tmp/wheelhouse/phonetisaurus*.whl -w /wheelhouse/

# Copies over bottle wheel.
RUN cp /tmp/wheelhouse/bottle*.whl /wheelhouse

# Removes the non-repaired wheels.
RUN rm -rd /tmp/wheelhouse

# # *******************************************************
# # *** Installs wheels in a fresh (OpenFst-free) image ***
# # *******************************************************
FROM common AS install-from-wheel

# Grabs the wheels (but just the wheels) from the previous image.
COPY --from=build-wheels /wheelhouse /wheelhouse

# Installs the wheels in all our Pythons and try to import Phonetisaurus.
RUN for PYBIN in /opt/python/cp*/bin; do \
    "${PYBIN}/pip" install phonetisaurus-bindings --no-index -f /wheelhouse \
    && "${PYBIN}/python" -c "import phonetisaurus" \
    || exit 1; \
done

# ********************
# *** Run e2e test ***
# ********************
FROM install-from-wheel AS run-tests

# Copies Phonetisaurus end-to-end test and assets
COPY --from=wheel-building-env "/src/Phonetisaurus/python/script" /test

# Runs test for each of our Pythons.
RUN yum install -y wget
RUN for PYBIN in /opt/python/cp*/bin; do \
    cd /test && PATH="$PYBIN:$PATH" ./e2e_test.sh || exit 1; \
done
