#!/bin/bash
# Saves your OpenAI key to a private file OUTSIDE the repo, so you never paste it again.
# Nothing you paste is shown or printed. Safe to run from any folder.
set -e
DIR="$HOME/.config/cjac"
FILE="$DIR/openai_key"
mkdir -p "$DIR"
chmod 700 "$DIR"
printf "Paste your OpenAI key, then press Return (nothing will show on screen): "
read -r -s KEY
echo
# remove spaces, line breaks and quote marks that can sneak in when copying
KEY="$(printf '%s' "$KEY" | tr -d '[:space:]"'"'"'')"
if [ -z "$KEY" ]; then
  echo "Nothing was pasted. Copy the key again and re-run this."
  exit 1
fi
umask 077
printf '%s' "$KEY" > "$FILE"
chmod 600 "$FILE"
echo "Saved to $FILE"
echo "That file is private to your Mac user and is outside the repo."
echo "Length: ${#KEY} characters. Starts with: ${KEY:0:3}..."
