---
date: August 2026
title: How a LEGO Grabber Led Me to Build My Own Robotic Arm
tags: [Robotics, Arduino, Engineering]
excerpt: I started with a LEGO grabber that could not bend. A few years later, I was building my own Wi-Fi-controlled robotic arm, writing the firmware and web controller, and learning that the hardest part of robotics is often everything between "it moves" and "it works well."
slug: lego-grabber-to-robotic-arm
---

In 6th grade, I built a grabber out of LEGO.

It could grab things. It could extend. But it could not really bend.

That bothered me more than it probably should have.

## I Did Not Want a Kit

A couple of years later, I started looking at robotic arms online.

Most of the kits looked cool, but many followed the same pattern: assemble the parts, connect the electronics, install the provided software, and start controlling the arm.

I wanted to understand what was happening underneath.

What actually happens between moving a control on a screen and a robotic joint moving on a desk?

So I decided to build my own.

I named the arm **Ashtavakra**, after the Hindu sage remembered for extraordinary wisdom despite his unusual physical form. I liked the idea that capability is not defined by appearance. For me, that fits this project: the arm may look mechanical and imperfect on the outside, but what makes it interesting is the thinking, control, and problem-solving built into it.

## First Goal: Make One Servo Move

The current arm uses an Arduino UNO R4 WiFi, an Emakefun motor driver, and eight TD-8120MG servos.

That sounds organized now.

It was not organized when I started.

My first milestone was simply getting one servo to move correctly.

Then I needed two.

Then eight.

And that is when I realized that eight servos moving is not the same thing as a robotic arm moving well.

Large angle changes made joints jerk. Servo horns were not perfectly centered. Some motors were mounted in opposite directions. The motor driver's connector numbers did not map the way I expected.

Every time I solved one problem, I found the next one.

## I Wanted to Control It From My Phone

I could have used buttons or a joystick.

Instead, I wanted to open a browser on my phone and control the arm over Wi-Fi.

So I built my own controller using HTML, CSS, and JavaScript.

The browser sends commands to the Arduino UNO R4 WiFi. The Arduino processes them and sends the correct movement to the motor driver.

Now I can open the controller from a phone or laptop, connect to the arm's IP address, and move individual joints.

No app to install.

That was probably the first moment when the project felt less like "Arduino plus some motors" and more like a complete robotic system.

## Getting From "It Moves" to "It Works"

Once the arm could move, I started noticing everything that made the movement unreliable or awkward.

Some servo horns were slightly off-center, so I added software offsets instead of repeatedly taking the joints apart.

Large movements were too abrupt, so I added S-curve easing and speed control.

I added a home/reset position so every joint could return to a known starting point.

I added an emergency STOP.

I added a debug page and better status output because I was spending too much time guessing when something failed.

None of those features were in my original idea.

They appeared because I kept using the arm, finding weaknesses, and improving them.

## What Changed While Building It

At the beginning, success meant getting the arm to move.

As the project grew, I started paying more attention to why it moved the way it did, how the electronics and software affected each other, and how to diagnose a problem without changing everything at once.

I also stopped expecting the first design to be the final one.

The project has already gone through changes in the controller hardware, servo driver, software structure, calibration, motion handling, and debugging tools.

That iteration became part of the project instead of something I considered a setback.

## Where Ashtavakra Is Now

Today, Ashtavakra is a working 6-DoF robotic arm with a gripper that I can control over Wi-Fi from a browser.

The Arduino runs the motion-control firmware. The web interface is my own. The arm includes smooth movement, software calibration, speed control, reset behavior, and emergency stop.

But I do not consider it finished.

The next stages are about making the arm do more than respond to manual commands. I want to keep building on the same platform instead of starting over each time I add a capability.

That is probably the biggest change from the LEGO grabber I built in 6th grade.

The LEGO grabber was something I made.

Ashtavakra has become something I keep engineering.

**[GitHub repo →](https://github.com/iamtilakpatel/ashtavakra)**  
**[Project page →](https://tilakpatel.me)**
