#!/bin/bash
# usage: place_download.sh <target-name.txt> "<CASE>" "<OUTLET>" "<BYLINE>" "<DATE>" "<HEADLINE>" "<NOTE>"
set -e
DL="$HOME/mnt/Downloads"; DEST="$HOME/mnt/Projects/asymmetrical_refugee_legitimation/data/fulltext"
mkdir -p "$DEST"
src=$(ls -t "$DL"/*.tmp 2>/dev/null | head -1)
[ -z "$src" ] && { echo "no .tmp download found"; exit 1; }
{
  printf 'CASE: %s\nOUTLET: %s\nBYLINE (recorded): %s\nDATE (recorded): %s\nHEADLINE (recorded): %s\nNOTE: %s\n' "$2" "$3" "$4" "$5" "$6" "$7"
  # drop site boilerplate paragraphs
  grep -v -E '^(Create an account or log in to save stories\.|Thanks for liking this story!.*|Save|SHARE|Listen|Dear reader,|When our communities are navigating uncertainty.*|At MPR News, we.re committed.*|Do you want to receive the Minnesota Today newsletter.*|Getting these updates in your inbox.*|Get the Minnesota Today Newsletter.*|Providing Support for MPR.*)$' "$src"
} > "$DEST/$1"
mv "$src" "$DL/_to_delete_$(basename "$src")" 2>/dev/null || true
echo "$1  $(wc -w < "$DEST/$1") words"
