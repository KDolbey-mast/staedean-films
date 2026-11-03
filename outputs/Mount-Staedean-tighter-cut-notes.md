# Mount Staedean — tighter cut and windblown beard

Two new exports preserve the preceding approved version:

- **Mount-Staedean-tighter-cut.mp4**: 98.83 seconds, approximately 22 seconds shorter.
- **Mount-Staedean-wind-beard-edition.mp4**: 120.75 seconds, original edit length with the beard correction.

Both use the approved clean wash colour, 1920×1080 output and sound.

## Beard correction

The shadow-like shape was the old beard extension: a flat strip along the ground, separate from the standing character's head. Crawling used another flat ground-level strip.

The replacement grows directly from the jaw in the same coordinate system as the head, so it follows the character's head turns and body movement. A travelling wave moves down the beard; motion increases toward the tip. Fine strands follow that wave. The old floor strip is suppressed whenever this wind treatment is selected. Wind strength is lower at the summit so it does not compete with the customer exchange.

## Editorial changes

The shorter version makes ordinary cuts at normal playback speed. It does not accelerate the character or pitch up the sound.

- Shorter early walks and arrival.
- Less hold time on sitting, the ticket call and the repeated checkpoint/bench scenes.
- Briefer route-choice and climbing shots.
- Removes the separate late-climb ellipsis close-up; the oxygen and crawling beats still communicate exhaustion.
- Shortens the summit approach and trims under a second from the long silence.
- Preserves the opening idea setup, ticket-printing gag, hard mountain-wide reveal, customer question, bulb extinction and final wording.

Sound uses the exact same source ranges as the picture. Five-millisecond audio fades at joins prevent clicks. The full-length corrected version is included for comparing the pacing.

## Code breadcrumbs

- `work/staedean-cast/src/wind_beard.py`: beard shape and travelling wave. `length`, `strength`, wave speed and width are the main tuning values.
- `work/staedean-cast/src/rig.py`: optional `beard_wind` setting passed from the body to the head. Existing callers keep the old drawing behavior by default, including The Door.
- `work/full-mount/mount_wind_film.py`: separate Mount staging for the wind treatment. Standing, close-up and crawling scenes supply the wind settings here.
- `work/full-mount/build-wind-edit.py`: renders changed scenes, reuses unchanged frames, exports the full corrected version, then makes the shorter version. The `TRIMS` table lists source frame ranges at 12 drawings per second; end indices are exclusive.
- `work/full-mount/wind-edit/edit-decisions.json`: exact short-cut shot starts and selected frame ranges.

To rebuild from a source-only archive, install the packages in `work/full-mount/requirements-lock.txt`, configure `ANIMATION_BROWSER` if needed, and first run `python work/full-mount/build.py --render` to create the original frame cache. Then run `python work/full-mount/build-wind-edit.py --proof` for previews or `python work/full-mount/build-wind-edit.py` for both new movies. For later beard changes, remove the generated `work/full-mount/wind-edit` folder before rebuilding, so cached frames are not reused.

## What to review

Compare the early bench montage between the two lengths. Watch the final ascent for the beard connection and flutter, then check whether the shorter approach and silence still give the ending enough weight. The original approved MP4 remains available unchanged.

## Verification

Rendered the nine affected ascent/summit shots, inspected standing, oxygen and crawling previews plus four successive wind poses, and decoded both complete MP4 exports without errors. The shorter version contains 1,186 drawings (98.83 seconds); the full corrected version contains 1,449 drawings (120.75 seconds).
