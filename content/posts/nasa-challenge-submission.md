---
date: May 2026
title: Submitting AERO-LITE to NASA
tags: [NASA, Competition, Storytelling]
excerpt: Eight slides and a prototype with live CO₂ readings. What I learned about explaining a technical project without exaggerating what my first prototype actually proved.
slug: nasa-challenge-submission
---

I spent almost 2 months building a CO₂ capture prototype. I spent three weeks figuring out how to explain it in 8 slides.

## The Deck Is Not the Project

My first draft had 14 slides. I thought more detail = more impressive. I was wrong. The NASA guide said maximum 8 slides. I had to kill slides I loved.

The slide about zeolite pore structure? Gone. The slide about PTC heater thermal curves? Gone. What stayed was the story: **problem → gap → solution → proof.**

## The Voice Problem

I asked AI to help me write the first draft of my presentation. Big mistake. It came back sounding like a senior engineer wrote it from a cubicle. "AERO-LITE is a regenerative CO₂ preprocessor leveraging zeolite adsorption and thermal swing regeneration..." I read it out loud to my dad, who is my mentor as well, and he said it sounded like I was reading someone else's research paper. Judges want to hear a 14-year-old who actually built this thing on his desk, not a NASA press release. So I threw the AI draft away and wrote it myself. "I kept reading about Artemis and realized we know how to capture CO₂ on the ISS but we just vent CO₂ into space. We also have a Sabatier reactor that turns CO₂ back into Oxygen. What I did is connect these two dots — so astronauts on the Moon do not have to throw away their air." Way better.

## The Numbers Have to Match

My firmware had placeholder timing (10/10/2 minutes). My slides and architecture notes described a different schedule. A judge who opened my GitHub repo could have seen conflicting versions of how the system was supposed to operate.

I updated the firmware settings and slides to describe the same **intended cycle**: approximately **5 minutes of adsorption, 1 minute of regeneration, and 15 seconds of purging**. That adds up to **6 minutes 15 seconds**, not exactly 6 minutes. These were design timings, **not a measured result from a fully validated capture-and-regeneration cycle**.

Then I triple-checked the claims. My early prototype used LEDs to simulate parts of the heater-control sequence; that is not the same as demonstrating repeated thermal regeneration. If I mentioned **90% capture efficiency**, I had to label it as a **design target requiring future validation**, not a measured result.

## The Photo Is Everything

Most middle school submissions are drawings or CAD renders. I had a photo of three mason jars and a live dashboard. In one recorded view, the **Cabin sensor showed 1,029 ppm** and the **Purified sensor showed 477 ppm**. Those are useful readings from that test setup, but one observation does **not** establish capture efficiency or prove sustained performance. The photo still matters because it shows that I built real hardware and could read data from it.

## What I Would Do Differently

- Start the deck earlier. I wrote it in the final week.
- Get feedback from someone who does not know engineering. If they understand the gap, the judges will too.
- Record a 30-second video of the dashboard updating. Even if it is optional, proof beats promises.

## The Waiting

I submitted on May 15, 2026. Now I wait. Whatever happens, I have a GitHub repo with 10+ commits, a working prototype, and a story that matters to me. That is the real prize.

## The Win

The ceremony started at 6:00 PM Central on May 27, 2026. I had the Zoom open on my laptop and my parents on either side, which I pretended to be annoyed by but actually wanted.

They ran through Elementary School awards first. I watched team after team get called up — kids who built moss walls and water filters. I was happy for them and also quietly calculating how much longer until the Middle School section.

Then the slide changed.

**Middle School**  
**Top Individual Award**  
**Tilak Patel**  
**Thompson Thunders | AERO-LITE**  
**Thompson Middle School**

I did not breathe for about three seconds. My mom started clapping before I processed what I was looking at. My dad just pointed at the screen like I had not already seen it.

The judge said something about technical detail and mission awareness and systems thinking. I heard the words but I was staring at my name on a Space Center Houston slide and thinking about three months ago — mid-March, that first email from the STEM Innovation Team, the moment I realized I had eight weeks to build something I barely understood.

I thought about the SCD41 that would not show up on the I²C scanner for three days. The activated carbon I threw out after learning it loves water more than CO₂. The night I ran the nitrogen compression numbers and felt stupid, then redesigned everything. The 3D-printed housing that warped on the first print. The web dashboard that actually worked on the third try.

All of that was on that slide. Not the glass jars. Not the wires. The _decisions_ — why zeolite 13X, why thermal swing, why concentrate before compress, why a bimetallic failsafe when software alone is not enough.

That is what the judges saw. That is what they called out: mass, power, automation, safety, future development. Not buzzwords. Trade-offs I actually made at this desk.

I still have the prototype. It is still on my desk, still collecting dust, still running the same state machine. But now it is not just a project I submitted and hoped would work. It is a project that worked well enough to convince engineers who design actual spacecraft life support systems.

The repo is public. The build log is documented. And I no longer have to end this story with "whatever happens."

This is what happened.

**[Watch the ceremony →](https://github.com/iamtilakpatel/aero-lite/blob/main/media/videos/NASA_Challenge_Winner_Announcement.mp4)**  
**[GitHub repo →](https://github.com/iamtilakpatel/aero-lite)**
