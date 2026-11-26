#!/usr/bin/env bash

ORIGEN="/home/edu/Desktop/Seguridad"
BASE="/home/edu/Backups/CronTest"
HOY="$(date +%F)"
DESTINO="$BASE/$HOY"
ULTIMA="$BASE/ultima"

mkdir -p "$BASE"

if [ -e "$ULTIMA" ]; then
    rsync -av --link-dest="$ULTIMA" "$ORIGEN"/ "$DESTINO"/
else
    rsync -av "$ORIGEN"/ "$DESTINO"/
fi

ln -sfn "$DESTINO" "$ULTIMA"