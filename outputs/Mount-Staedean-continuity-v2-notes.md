# Mount Staedean — shorter cut, continuity revision

The 98.83-second shorter cut is now the working version.

- The progress reveal uses the same medium beard length (0.36) and greying (0.27) as the preceding snowy bench scene. Both the close framing and mountain-wide framing use this corrected character.
- A much larger red arrow with a filled head and bold YOU ARE HERE label points to the tiny PM. It appears after the cut wide, preserving the reveal's timing.
- The windblown beard later in the film and the shorter cut's picture/sound timing are retained.

The correction lives in the D9_how_far shot in work/full-mount/mount_wind_film.py. Optional pm_beard and pm_grey parameters in work/staedean-cast/src/sets.py let this distant character keep his age; other mountain shots retain their original defaults.

Build with work/full-mount/build-continuity.py. This reuses the wind-edit cache and redraws the progress shot. For a fresh source-only rebuild, run build.py --render, then build-wind-edit.py, then build-continuity.py, all inside work/full-mount (or invoke those paths from the project root). See the included earlier editing guide for dependencies and browser configuration. After further changes to this reveal, remove the generated work/full-mount/continuity-edit folder before rebuilding.

Review the progress reveal: check the beard before the cut, then the large labelled arrow in the wide view. The prior movie exports remain unchanged.
