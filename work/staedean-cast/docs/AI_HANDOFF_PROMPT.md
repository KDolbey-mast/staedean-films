# Brief to paste into another AI assistant

I'm working on a series of short animated films for STAEDEAN, a B2B software company, with a recurring cast. I've attached the repo (or a zip of it). Please read `README.md`, then `docs/CAST.md` and `docs/STYLE.md`, before suggesting anything.

**The series so far**

1. *Mount Staedean* (2 min): a product manager carries a bright idea up a 20,000 m mountain of checkpoints. By the time he crawls to the customer at the summit, the idea is dead and the customer asks "Who are you?".
2. *The Door* (49 s): the same PM walks through a small door to the customer 20 m away. Weekly visits, fast failures, a handshake, the product catapulted over the mountain, and everyone serving customers together.

**How it's made:** everything is drawn by Python code generating SVG, rendered to PNG with headless Chromium (Playwright), scored with synthesised sound and encoded with ffmpeg. Every character is a puppet with dials (pose, mood, age, bulb brightness), available through `src/cast.py`. That is why the characters stay consistent.

**Rules**

- Use the cast through `src/cast.py`. Do not redraw characters frame by frame or invent new versions of them.
- Keep the continuity rules and brand rules in `docs/CAST.md`, and the look, timing and sound in `docs/STYLE.md`.
- The customer never wears STAEDEAN colours on his tie or cup.
- Keep the humour about the system, never about the people.
- If your environment can't run Chromium, say so and give me code changes to run on my own machine.
- Plain language, no em-dashes.

**What I'd like to do now:** [describe it here]
