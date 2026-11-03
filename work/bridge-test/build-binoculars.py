"""Separate revision cache keeps the approved original preview intact."""
import asyncio
import build
build.WORK = build.WORK / 'binoculars-v2'
if __name__ == '__main__':
    asyncio.run(build.render())
    build.encode(build.soundtrack(), 'The-Perfect-Bridge-binoculars-v2.mp4')
