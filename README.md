# Gym Forge

Builds a weekly gym plan in your browser. No AI service, no API key, no account. Each exercise shows a two-frame demo animation, full steps, rest, effort, and a link to form videos.

## What works offline

- Everything except the Watch video links. The exercise library and all demo images are inside `index.html`.
- Open the page once with internet. After that the app opens without internet (a service worker stores the files).
- You also open `index.html` straight from a file on your computer. Offline saving of the app needs the hosted address.

## How plans are built

The page uses built-in rules, not a live AI model.

- Goal sets reps and rest.
- Level sets exercise choice, sets, effort, and cues:
  - Beginner: machines, cables, dumbbells, bodyweight. No technical lifts. 2 to 3 sets. Easy to moderate effort.
  - Intermediate: more free weights. 3 to 4 sets. 1 to 3 reps before failure.
  - Advanced: heavy top sets with back-off sets, tempo, RPE targets, deload notes.
- Equipment limits the exercises to full gym, dumbbells, or bodyweight.
- Days per week sets the split. Session length sets the exercise count.
- The skip box removes any exercise with a matching word.
- Shuffle makes a new version of the same plan.
- Save plan stores plans on your device. Download file saves one HTML page with images. Copy text and Print are included.

## Put it on GitHub Pages

1. Create a public repository on github.com.
2. Upload every file in this folder: `index.html`, `sw.js`, `manifest.webmanifest`, `icon.svg`, `template.html`, `build.py`, `README.md`.
3. Open Settings, then Pages.
4. Under Build and deployment, choose Deploy from a branch. Pick `main` and the `/ (root)` folder. Save.
5. Wait a few minutes. Open `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`.

## Add to iPhone home screen

Open the Pages address in Safari. Tap Share, then Add to Home Screen. Open the app once with internet first.

## Rebuild the page

Only needed if you change `template.html`.

1. `pip install pillow`
2. `python3 build.py`

The script downloads the exercise library and demo images, shrinks the images, and writes a new `index.html` (about 7 MB).

## Credits

Exercise data and images: https://github.com/yuhonas/free-exercise-db. Check the repository for its license terms.
