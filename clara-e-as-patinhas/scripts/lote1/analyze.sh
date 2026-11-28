#!/bin/bash
# per-song analysis of chorus takes -> music/analysis/<slug>/
cd "$(dirname "$0")/../.."; export VM_TMP=/tmp/claude-0/-home-user-YouTube/d850b732-f9ee-5afb-a405-beaa03bb820f/scratchpad
s=$1; shift; mkdir -p music/analysis/$s
for k in "$@"; do A=music/masters/lote1/$s/chorus_$k.wav
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $A)
  python3 scripts/pilot/analyze_take.py $A --json music/analysis/$s/take_$k.json > /dev/null
  python3 scripts/voice_match.py check $A --win $(python3 -c "print(round($D/2,2))") --json music/analysis/$s/voice_$k.json | tail -1 | sed "s/^/$k VOICE /"
  python3 scripts/whisper_words.py $A music/analysis/$s/whisper_$k.json > /dev/null && python3 -c "import json;j=json.load(open('music/analysis/$s/whisper_$k.json'));t=json.load(open('music/analysis/$s/take_$k.json'));print('$k TAKE',{x:t[x] for x in ('tempo_bpm','key','lead_notes_covering_90pct','lead_range_semitones_p5_p95','lead_f0_median_hz')});print('$k WHISPER',j['text'])"
done
