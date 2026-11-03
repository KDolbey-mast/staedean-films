import glob, subprocess, os
from timing import T
import sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "frames"
os.makedirs("vid", exist_ok=True)
scenes = []
total = 0
for s in range(1, 8):
    fs = sorted(glob.glob(f"{SRC}/S{s}_*.png"))
    args, chains = [], []
    for i, fp in enumerate(fs):
        d = T[os.path.basename(fp)[:5]]; total += d
        args += ["-framerate", "30", "-i", fp]
        fx = ""
        if s == 1 and i == 0: fx = ",fade=t=in:st=0:d=0.6"
        if s == 7 and i == len(fs) - 1: fx = f",fade=t=out:st={d - 1.2:.2f}:d=1.2"
        chains.append(f"[{i}:v]format=yuv420p,loop=-1:1,trim=duration={d},setpts=PTS-STARTPTS{fx}[v{i}]")
    fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(len(fs))) + f"concat=n={len(fs)}:v=1:a=0[out]"
    tmp, out = f"vid/scene{s}.tmp.mp4", f"vid/scene{s}.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", fc, "-map", "[out]", "-r", "30",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", tmp]
    subprocess.run(cmd, check=True); os.replace(tmp, out); scenes.append(out)
open("vid/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in scenes))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "vid/list.txt", "-c", "copy",
                "-movflags", "+faststart", "vid/MOUNT_STAEDEAN_animatic.tmp.mp4"], check=True)
os.replace("vid/MOUNT_STAEDEAN_animatic.tmp.mp4", "vid/MOUNT_STAEDEAN_animatic.mp4")
print("total seconds", round(total, 1))
