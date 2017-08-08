#!/usr/bin/env bash

make html
rsync --delete -az _build/html/ ~/src/sjl.bitbucket.org/flask-lesscss
hg -R ~/src/sjl.bitbucket.org commit -Am 'flask-lesscss: Update documentation.'
hg -R ~/src/sjl.bitbucket.org push
