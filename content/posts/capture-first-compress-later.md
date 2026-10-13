---
date: April 2026
title: The Calculation That Changed AERO-LITE
tags: [Design, Math, Iteration]
excerpt: I wanted to compress cabin air directly, but compression alone would not separate out CO₂. The numbers made me rethink the design: capture CO₂ first, then consider compressing a concentrated stream. That is where AERO-LITE changed direction.
slug: capture-first-compress-later
---

My first AERO-LITE design was wrong. Not slightly wrong. Fundamentally wrong. And I did not realize it until I ran the numbers.

## The Original Plan

I thought: cabin air goes in, a compressor squeezes it, and I have a useful CO₂ stream. Simple, right? One stage instead of four. Less complexity. Fewer parts.

But squeezing a gas mixture does not separate its components. Without a separate capture or separation step, compressed cabin air is still mostly nitrogen and oxygen.

I even started sketching the compressor placement in my 3D model. I was proud of how "elegant" it was.

## The Math

For a rough starting comparison, ordinary air is approximately:

- 78% nitrogen
- 21% oxygen
- About 0.04% CO₂ (roughly 400 ppm); CO₂ levels in an occupied enclosed space can be higher, depending on ventilation and other conditions
- Small amounts of other gases

At **1,000 ppm CO₂, only about 0.1% of the gas molecules are CO₂**. If I compress the whole mixture without separating it first, nearly all the gas being compressed is something other than the CO₂ I want to collect.

That does **not** prove that exactly 99% of the compression energy is wasted or that a new design will save a specific percentage of power. Actual energy use depends on pressure, flow, compressor efficiency, and the rest of the process. But it was enough to show me the problem with my first concept: compression alone would not give me a concentrated CO₂ stream.

I stared at the calculation for a long time. Then I felt stupid. Then I felt excited, because I had found a better question to solve.

## The Redesign

I threw out the single-stage idea and redesigned AERO-LITE around four steps:

1. **Dry:** Reduce moisture using silica gel.
2. **Trap:** Use zeolite 13X to adsorb CO₂ from the air stream.
3. **Release:** Regenerate the sorbent using heat so the captured CO₂ can be collected in a more concentrated stream.
4. **Compress:** In the intended later-stage system, compress that CO₂-rich stream for storage or further processing instead of compressing untreated cabin air.

My early prototype explored the sorbent and sensing parts of this idea. It did **not** establish the efficiency of a complete heated regeneration and compression cycle. Those parts still need validation.

The insight: **capture first, compress later.** Separate what you need before designing the energy-intensive steps around it.

## Why This Matters Beyond AERO-LITE

Every engineering decision is a trade-off. My original idea was simpler on paper, but it did not separate CO₂ from the rest of the air. The redesigned approach adds components and controls that might make separation and downstream compression more practical. Whether it saves mass or power is a question for later testing, not something my early prototype has proved.

I learned that the first idea is rarely the best idea. The best idea comes after you do the math, feel stupid, and fix it.
