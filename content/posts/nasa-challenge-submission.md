---
date: May 2026
title: Submitting AERO-LITE to NASA
tags: [NASA, Competition, Storytelling]
excerpt: 8 slides, and a prototype that tweets CO₂ data. What I learned about telling a technical story to judges who see 50 decks a day. Also: why you should never claim 90% efficiency if you have not measured it yet.
slug: nasa-challenge-submission
---

I spent three months building a CO₂ capture prototype. I spent three weeks figuring out how to explain it in 8 slides.

## The Deck Is Not the Project

My first draft had 14 slides. I thought more detail = more impressive. I was wrong. The NASA guide said maximum 8 slides. I had to kill slides I loved.

The slide about zeolite pore structure? Gone. The slide about PTC heater thermal curves? Gone. What stayed was the story: **problem → gap → solution → proof.**

## The Voice Problem

I asked AI to help me write the first draft of my presentation. Big mistake. It came back sounding like a senior engineer wrote it from a cubicle. "AERO-LITE is a regenerative CO₂ preprocessor leveraging zeolite adsorption and thermal swing regeneration..." I read it out loud to my dad, who is my mentor as well, and he said it sounded like I was reading someone else's research paper. Judges want to hear a 14-year-old who actually built this thing on his desk, not a NASA press release. So I threw the AI draft away and wrote it myself. "I kept reading about Artemis and realized we know how to capture CO₂ on the ISS but we just vent CO₂ into space. We also have a Sabatier reactor that turns CO₂ back into Oxygen. What I did is connect these two dots — so astronauts on the Moon do not have to throw away their air." Way better.

## The Numbers Have to Match

My firmware had placeholder timing (10/10/2 minutes). My slides said 5/1/15 seconds. My architecture docs said ~80/20 split. A judge who clicks my GitHub repo would see three different stories.

I fixed the firmware to match the intended design: 5 minutes / 1 minute / 15 seconds. Then I fixed the slides. Then I triple-checked every claim. If you say "90% capture efficiency" and your prototype uses LED-simulated heaters, you better say "target: 90%, Phase 2 validation pending."

## The Photo Is Everything

Most middle school submissions are drawings or CAD renders. I have a photo of three mason jars with a live dashboard showing 1,029 ppm → 477 ppm. That photo is my secret weapon. It says "this kid actually built something" without me having to say it.

## What I Would Do Differently

- Start the deck earlier. I wrote it in the final week.
- Get feedback from someone who does not know engineering. If they understand the gap, the judges will too.
- Record a 30-second video of the dashboard updating. Even if it is optional, proof beats promises.

## The Waiting

I submitted on May 15, 2026. Now I wait. Whatever happens, I have a GitHub repo with 10+ commits, a working prototype, and a story that matters to me. That is the real prize.
