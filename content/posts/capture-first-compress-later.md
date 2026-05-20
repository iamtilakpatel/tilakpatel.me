---
date: April 2026
title: The 99% Nitrogen Mistake
tags: [Design, Math, Iteration]
excerpt: I wanted to compress cabin air directly. Then I did the math and realized 99% of that energy compresses nitrogen, not CO₂. I felt stupid. Then I redesigned everything. That is where AERO-LITE actually became AERO-LITE.
slug: capture-first-compress-later
---

My first AERO-LITE design was wrong. Not slightly wrong. Fundamentally wrong. And I did not realize it until I ran the numbers.

## The Original Plan

I thought: cabin air goes in, compressor squeezes it, concentrated CO₂ comes out. Simple, right? One stage instead of four. Less complexity. Fewer parts.

I even started sketching the compressor placement in my 3D model. I was proud of how "elegant" it was.

## The Math

Cabin air is roughly:

- 78% nitrogen
- 21% oxygen
- 0.04% CO₂ (can rise to 1,000+ ppm in a sealed habitat, but still ~0.1%)
- Trace gases

If I compress 100 liters of cabin air to feed the Sabatier reactor, **99% of the energy goes into compressing nitrogen and oxygen**. Only ~0.1% of the molecules I am compressing are actually CO₂.

I stared at the calculation for a long time. Then I felt stupid. Then I felt excited — because I had found the real problem.

## The Redesign

I threw out the single-stage design and built the four-stage system:

1. **Dry:** Remove moisture (silica gel)
2. **Trap:** Capture CO₂ selectively (zeolite 13X)
3. **Release:** Heat to drive off concentrated CO₂
4. **Compress:** Now you are only compressing CO₂, not 99% nitrogen

The insight: **capture first, compress later.** Concentrate the useful stuff before you spend energy moving it.

## Why This Matters Beyond AERO-LITE

Every engineering decision is a trade-off. My original design traded simplicity for efficiency. The new design trades complexity for mass and power savings — which is the right trade when every pound to the Moon costs thousands.

I learned that the first idea is rarely the best idea. The best idea comes after you do the math, feel stupid, and fix it.
