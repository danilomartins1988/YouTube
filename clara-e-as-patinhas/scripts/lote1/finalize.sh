#!/bin/bash
# finalize.sh SLUG EN_TAG ES_TAG : PT master, EN/ES vocals on the PT instrumental, instrumental master, Studio WAVs, scratchpad MP3s
set -e; cd "$(dirname "$0")/../.."
s=$1; EN=$2; ES=$3; M=music/masters/lote1/$s; ST=music/stems/lote1/$s
SCR=/tmp/claude-0/-home-user-YouTube/d850b732-f9ee-5afb-a405-beaa03bb820f/scratchpad; L=$SCR/lote1/$s; mkdir -p $L
for t in pt_v1 $EN $ES; do [ -f $ST/$t/vocals.wav ] || { python3 -m demucs --two-stems=vocals -n htdemucs -o $SCR/dm $M/full_$t.wav >/dev/null 2>&1; mkdir -p $ST/$t; mv $SCR/dm/htdemucs/full_$t/*.wav $ST/$t/; }; done
bash scripts/ep2/master.sh $M/full_pt_v1.wav $M/${s}_pt_final > /dev/null
for p in "en:$EN" "es:$ES"; do lg=${p%%:*}; t=${p##*:}
  ffmpeg -v error -y -i $ST/pt_v1/no_vocals.wav -i $ST/$t/vocals.wav -filter_complex "amix=inputs=2:normalize=0:duration=longest" -c:a pcm_s24le $M/${s}_${lg}_raw.wav
  bash scripts/ep2/master.sh $M/${s}_${lg}_raw.wav $M/${s}_${lg}_final > /dev/null; rm $M/${s}_${lg}_raw.wav; done
J=$(ffmpeg -hide_banner -nostats -i $ST/pt_v1/no_vocals.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i $ST/pt_v1/no_vocals.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le $M/${s}_instrumental.wav
ffmpeg -v error -y -i $M/${s}_instrumental.wav -b:a 256k $M/${s}_instrumental.mp3
D=$(python3 -c "import json;print(json.load(open('music/compositions/lote1/$s/sections.json'))['duration_ms']/1000+1.0)")  # video = song + 1 s tail
mkdir -p $L/youtube_studio_audio
for lg in pt en es; do
  cp $M/${s}_${lg}_final.mp3 $L/musica_completa_${lg^^}.mp3
  ffmpeg -v error -y -i $M/${s}_${lg}_final.wav -af "apad=whole_dur=$D" -t $D -c:a pcm_s24le -ar 48000 $L/youtube_studio_audio/${s}_audio_${lg}.wav
  printf "%s %s " $lg "$(ffprobe -v error -show_entries format=duration -of csv=p=0 $M/${s}_${lg}_final.wav)"; ffmpeg -nostats -i $M/${s}_${lg}_final.wav -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -A20 Summary | grep -E " I:|Peak:" | tr -s ' ' | tr '\n' ' '; echo
done
cp $M/${s}_instrumental.mp3 $L/instrumental.mp3
