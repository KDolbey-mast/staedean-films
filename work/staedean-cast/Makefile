# Run from the repo root. Needs Python 3.10+, requirements.txt, Chromium for Playwright, ffmpeg.
STYLE ?= marker
PY = cd src && MS_STYLE=$(STYLE) python3
ENC = -vf "fps=24,format=yuv420p" -c:v libx264 -crf 19 -c:a aac -b:a 192k -af loudnorm=I=-16:TP=-1.5 -shortest

.PHONY: setup sheets film1 film2 check1 check2 clean

setup:
	pip install -r requirements.txt && playwright install chromium

sheets:            ## cast model sheets -> assets/sheets
	$(PY) make_sheets.py ../assets/sheets

check1:            ## one test frame per shot, film 1
	$(PY) film.py "" mid && echo "frames in src/film_seq"

check2:            ## one test frame per shot, film 2
	$(PY) film2.py "" mid && echo "frames in src/film2_frames"

film1:             ## Mount Staedean, about 15 min
	mkdir -p build src/vid
	$(PY) film.py
	cd src && python3 film_sound.py
	ffmpeg -y -framerate 12 -i src/film_seq/%05d.png -i src/vid/film.wav -map 0:v -map 1:a $(ENC) build/mount_staedean.mp4

film2:             ## The Door, about 6 min
	mkdir -p build src/vid
	$(PY) film2.py
	cd src && python3 film2_sound.py
	ffmpeg -y -framerate 12 -i src/film2_frames/%05d.png -i src/vid/film2.wav -map 0:v -map 1:a $(ENC) build/the_door.mp4

clean:
	rm -rf build src/film_seq src/film2_frames src/vid src/__pycache__
