"""Approved short gag with the recurring mountain as distant scenery.

Use a separate cache and output so the previous approved movie stays available.
Only the setting is replaced: poses, camera cuts and audio use the short version.
"""
import asyncio
import build
import sets
original_setting=build.d.setting
# Reuse the real mountain, route and checkpoints. Its own sky would cover the
# short's white-paper background, so remove that exact generated prefix only.
mountain=sets.big_mountain(show_sign=False).removeprefix(sets.sky())
background='<g transform="translate(350,180) scale(.75)" opacity=".55">'+mountain+'</g>'
def mountain_setting(t):
    return original_setting(t,background=background)
build.d.setting=mountain_setting
build.WORK=build.WORK/'mountain-v3'
if __name__=='__main__':
    asyncio.run(build.render())
    build.encode(build.ROOT/'work/bridge-test/binoculars-v2/soundtrack.wav',
                 'The-Perfect-Bridge-mountain-v3.mp4')
