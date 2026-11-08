#!/bin/zsh
# Usage: render.sh <lang> <out.mp4>   Composes the 1920x1080 WristNote demo (25 s, 30 fps).
set -e
cd "${0:A:h}"
L=$1; OUT=$2; C=clips; A=assets
source ./cuts-$L.sh   # cut points of the last capture in this language (see README)
# Timeline: A 0-3.4 tap · B 3.4-12.2 recording · C 12.2-15.2 processing · D 15.2-21.5 note · end 21.5-25
PX=1290; PY=100; WX=730; WY=360
cap() { # index start end
  echo "[$(( $1 + 8 )):v]format=rgba,fade=t=in:st=$2:d=0.4:alpha=1,fade=t=out:st=$(( $3 - 0.4 )):d=0.4:alpha=1[c$1];"
}
ffmpeg -v warning -y \
  -i $C/p_rec.mp4 -i $C/p_note.mp4 -i $C/w_idle.mp4 \
  -loop 1 -t 8.8 -i $C/w_rec.png -i $C/w_proc.mp4 -loop 1 -t 9.8 -i $C/w_done.png \
  -loop 1 -t 25 -i $A/bg.png -loop 1 -t 25 -i $A/frame.png -loop 1 -t 25 -i $A/tap.png \
  -loop 1 -t 25 -i $A/cap_${L}_1.png -loop 1 -t 25 -i $A/cap_${L}_2.png \
  -loop 1 -t 25 -i $A/cap_${L}_3.png -loop 1 -t 25 -i $A/cap_${L}_4.png \
  -loop 1 -t 25 -i $A/end_${L}.png \
  -loop 1 -t 25 -i $A/phone_mask.png -loop 1 -t 25 -i $A/watch_mask.png \
  -filter_complex "$(eval "echo \"$(cat graph.tmpl)\"")" \
  -map "[out]" -t 25 -r 30 -c:v libx264 -preset slow -crf 20 -movflags +faststart -an "$OUT"
echo "rendered $OUT"
