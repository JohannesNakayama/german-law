#!/usr/bin/env bash
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail
set -Eeuo pipefail

rm -rf german-law

wget -nv -r -l 3 -A epub -P . https://www.gesetze-im-internet.de/aktuell.html
mv www.gesetze-im-internet.de german-law

echo "Processing..."
find german-law -type f -name "*.epub" | \
parallel --bar -j+0 'pandoc "{}" -t gfm -o "{.}.md"; rm "{}"'
