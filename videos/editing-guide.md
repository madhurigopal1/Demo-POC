Editing Guide and Assembly Commands

This guide walks you through assembling the 2-minute highlight video using ffmpeg. Replace placeholders with your filenames.

Prerequisites
- ffmpeg installed
- Recorded MP4 clips for each POC: code_viz.mp4, data_classify.mp4, model_proto.mp4, data_map.mp4, recs.mp4, langchain_local.mp4, knowledge_mgmt.mp4, neuroai.mp4
- Opening and closing title PNGs: title.png, end.png
- Voiceover audio file (optional): voiceover.wav (if you record voice separately)

Concatenate clips with timing and transitions

1) Make sure each clip is trimmed to the desired length (see script timestamps):
- code_viz.mp4 -> 14s
- data_classify.mp4 -> 12s
- model_proto.mp4 -> 12s
- data_map.mp4 -> 12s
- recs.mp4 -> 12s
- langchain_local.mp4 -> 12s
- knowledge_mgmt.mp4 -> 12s
- neuroai.mp4 -> 12s

2) Example ffmpeg command to concatenate clips (create a file list first):

printf "file 'title.mp4'\nfile 'code_viz.mp4'\nfile 'data_classify.mp4'\nfile 'model_proto.mp4'\nfile 'data_map.mp4'\nfile 'recs.mp4'\nfile 'langchain_local.mp4'\nfile 'knowledge_mgmt.mp4'\nfile 'neuroai.mp4'\nfile 'end.mp4'" > files.txt

ffmpeg -f concat -safe 0 -i files.txt -c copy combined_nomusic.mp4

3) Add voiceover (if you have voiceover.wav) and music (bg.mp3):
ffmpeg -i combined_nomusic.mp4 -i voiceover.wav -i bg.mp3 -filter_complex "[1:a]volume=1[a1];[2:a]volume=0.2[a2];[0:a][a1][a2]amix=inputs=3:duration=shortest" -c:v copy -c:a aac final_video.mp4

4) Add captions burned into video (optional):
- Create subtitles.srt matching timestamps
- ffmpeg -i final_video.mp4 -vf subtitles=subtitles.srt -c:a copy final_with_subs.mp4

Notes
- If you record voiceover in segments, assemble them using the same concat approach before mixing with video.
- Use fade transitions by re-encoding segments with filter_complex if desired (more advanced ffmpeg usage).

