#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/code-sections/rebuild-index.js"
echo ""
read -n 1 -s -r -p "Press any key to close..."
echo ""
