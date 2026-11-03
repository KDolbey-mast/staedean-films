"""Build the revised full cut and an eight-second launch/catch review clip."""
import asyncio,subprocess,json,zipfile
from pathlib import Path
import build,director as d,imageio_ffmpeg,launch_shot
asyncio.run(build.render())
audio=build.soundtrack()
name='The-Door-catapult-edition.mp4'
build.encode(audio,name,'sequence-catapult')
start=next(start for start,s in d.timeline()[0] if s['name']=='L1_over_the_mountain')
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-ss',str(start),'-i',str(build.OUT/name),'-t',str(launch_shot.DURATION+2.5),'-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(build.OUT/'The-Door-catapult-preview.mp4')],check=True)
print('Full cut and launch/catch preview complete',flush=True)
