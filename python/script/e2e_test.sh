#!/usr/bin/env bash

set -e

mkdir example
cd example

# Grab a copy of the latest version of CMUdict:
wget https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict

# Clean it up a bit and reformat:
cat cmudict.dict \
  | perl -pe 's/\([0-9]+\)//;
              s/\s+/ /g; s/^\s+//;
              s/\s+$//; @_ = split (/\s+/);
              $w = shift (@_);
              $_ = $w."\t".join (" ", @_)."\n";' \
                  > cmudict.formatted.dict

# Train a complete model with default parameters using the wrapper script.
phonetisaurus-train --lexicon cmudict.formatted.dict --seq2_del

# Generate pronunciations for a word list using the wrapper script:
phonetisaurus-apply --model train/model.fst --word_list ../words.list

cd ..
rm example -rd
