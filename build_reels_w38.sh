#!/bin/bash
# MORENE W38 Reels builder — 6 frames -> 1080x1920 H.264 + royalty-free music
# f1=3s, f2-f6=4.8s, xfade=0.4s -> total 25s
REELS_DIR="/Users/morrislin/mw-social-assets/MORENE/W38/Reels"
OUT_DIR="${REELS_DIR}/video"
AUDIO_DIR="/Users/morrislin/mw-social-assets/audio"

IDS=(R1 R2 R3)
mkdir -p "$OUT_DIR"

for ID in "${IDS[@]}"; do
  case "$ID" in
    R1) TRACK="calm" ;;        # 8/27 初秋夜晚沉靜儀式
    R2) TRACK="contempl" ;;    # 8/30 梭羅×湖濱散記減法
    R3) TRACK="bright" ;;      # 9/2 前中後調換季搭配
  esac
  AUDIO="${AUDIO_DIR}/MORENE_reels_${TRACK}.mp3"
  OUT="${OUT_DIR}/MORENE_W38_${ID}.mp4"
  echo ">>> Building W38_${ID} [${TRACK}]..."

  ffmpeg -y \
    -loop 1 -t 3.0  -i "${REELS_DIR}/MORENE_W38_${ID}_f1.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_W38_${ID}_f2.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_W38_${ID}_f3.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_W38_${ID}_f4.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_W38_${ID}_f5.png" \
    -loop 1 -t 4.8  -i "${REELS_DIR}/MORENE_W38_${ID}_f6.png" \
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
echo "=== Done ==="; ls -lh "${OUT_DIR}/"
