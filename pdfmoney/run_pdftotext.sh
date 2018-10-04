#!/bin/bash

IFS=$'\n';

for file in $(find '/\data/' -iname '*.pdf'); do /usr/bin/pdftotext -layout "$file"; done
