#!/bin/bash
# MORENE Reels batch ffmpeg builder
# 6 frames -> 1080x1920 H.264 yuv420p with xfade + audio
# f1=3s, f2-f6=4.8s, xfade=0.4s -> total 25s
# Offsets: t12=2.6, t23=7.0, t34=11.4, t45=15.8, t56=20.2

REELS_DIR="/Users/morrislin/mw-social-assets/MORENE/W_increment/Reels"
OUT_DIR="${REELS_DIR}/video"
AUDIO_DIR="/Users/morrislin/mw-social-assets/audio"

# Music map: calm=W1R1,W1R2,W2R1,W2R2,W4R2,W4R3; bright=W3R2,W5R1,W3R3,W5R3; contempl=W3R1,W5R2,W4R1
declare -A MUSIC_MAP
MUSIC_MAP["W1inc_R1"]="calm"
MUSIC_MAP["W1inc_R2"]="calm"
MUSIC_MAP["W2inc_R1"]="calm"
MUSIC_MAP["W2inc_R2"]="calm"
MUSIC_MAP["W3inc_R1"]="contempl"
MUSIC_MAP["W3inc_R2"]="bright"
MUSIC_MAP["W3inc_R3"]="bright"
MUSIC_MAP["W4inc_R1"]="contempl"
MUSIC_MAP["W4inc_R2"]="calm"
MUSIC_MAP["W4inc_R3"]="calm"
MUSIC_MAP["W5inc_R1"]="bright"
MUSIC_MAP["W5inc_R2"]="contempl"
MUSIC_MAP["W5inc_R3"]="bright"

# All 13 IDs (W1inc_R1 already done as pilot, but re-render is idempotent)
IDS=(W1inc_R1 W1inc_R2 W2inc_R1 W2inc_R2 W3inc_R1 W3inc_R2 W3inc_R3 W4inc_R1 W4inc_R2 W4inc_R3 W5inc_R1 W5inc_R2 W5inc_R3)

mkdir -p "$OUT_DIR"

for ID in "${IDS[@]}"; do
  TRACK="${MUSIC_MAP[$ID]}"
  AUDIO="${AUDIO_DIR}/MORENE_reels_${TRACK}.mp3"
  OUT="${OUT_DIR}/MORENE_${ID}.mp4"

  echo ">>> Building ${ID} [${TRACK}]..."

  ffmpeg -y \
    -loop 1 -t 3.0  -i "${REELS_DIR}/MORENE_${ID}_f1.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_${ID}_f2.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_${ID}_f3.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_${ID}_f4.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_${ID}_f5.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_${ID}_f6.png" \
    -i "$AUDIO" \
    -filter_complex "
      [0:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v0];
      [1:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v1];
      [2:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v2];
      [3:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v3];
      [4:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v4];
      [5:v]scale=1080:1920:force_original_aspect_ratio=disable,setsar=1,fps=30[v5];
      [v0][v1]xfade=transition=fade:duration=0.4:offset=2.6[x01];
      [x01][v2]xfade=transition=fade:duration=0.4:offset=7.0[x02];
      [x02][v3]xfade=transition=fade:duration=0.4:offset=11.4[x03];
      [x03][v4]xfade=transition=fade:duration=0.4:offset=15.8[x04];
      [x04][v5]xfade=transition=fade:duration=0.4:offset=20.2[xout];
      [6:a]afade=t=in:ss=0:d=0.5,afade=t=out:st=23.5:d=1.5[aout]
    " \
    -map "[xout]" -map "[aout]" \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 23 \
    -c:a aac -b:a 128k \
    -movflags +faststart -shortest \
    "$OUT" 2>/dev/null

  if [ $? -eq 0 ]; then
    DUR=$(ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT" 2>/dev/null)
    echo "  OK: ${OUT} (${DUR}s)"
  else
    echo "  FAILED: ${ID}"
  fi
done

echo ""
echo "=== Done ==="
ls -lh "${OUT_DIR}/"
