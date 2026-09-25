---
date: September 2026
title: When My Robotic Arm Didn’t Work: How I Learned to Solve Engineering Problems
tags: [Robotics, Engineering, Debugging]
excerpt: I started by changing code until something worked. After a fried board, a missing I2C device, strange servo channels, and a Wi-Fi address of 0.0.0.0, I learned a better way to debug: isolate one problem, test one assumption, and collect evidence before changing anything.
slug: robotic-arm-engineering-problems
---

The first time Ashtavakra, my 6 DoF robotic arm, stopped working, I did what I usually did.

I changed the code.

Then I changed something else.

Then another thing.

Eventually I had several changes and no idea which one mattered.

Building this robotic arm forced me to get better at debugging because there were too many possible failure points: power, wiring, I2C, Wi-Fi, firmware, servo mapping, mechanical alignment, and the browser controller.

Over time, I stopped asking, "What should I change?"

I started asking, "What can I test?"

## The Board I Fried

My first servo-control board was based on a PCA9685.

I supplied it with 7.4 volts.

The board was rated for less.

It died.

There was not much debugging to do after that.

But it changed how I approached hardware. Before connecting the replacement, I paid much closer attention to operating voltage, power requirements, and what the board was actually designed to handle.

I eventually moved to an Emakefun Motor Driver V5.2 that was better suited to the arm.

That mistake was expensive compared with a software bug, but it taught me something code could not: hardware does not give you an undo button.

## The Motor Driver That Would Not Respond

After replacing the board, I had another problem.

The Arduino could not communicate with the motor driver.

I expected the I2C address to be:

```text
0x40
```

I checked the main firmware and changed a few things.

Nothing.

This time, instead of continuing to modify the entire program, I wrote a tiny I2C scanner.

Its job was simple: scan the bus and tell me which devices it could actually see.

It found:

```text
0x60
```

The driver was fine.

My assumption was wrong.

That small test changed the way I debugged the rest of the project.

## The Servo Channels Made No Sense

Once communication worked, I assumed the physical servo connectors would map neatly to the control channels.

They did not.

The connector labeled like the next servo was not necessarily the next software channel.

Instead of trying random combinations inside the full arm firmware, I connected one servo and tested the channels one at a time.

That gave me the actual mapping I needed.

It was not an exciting test.

It was useful because it answered exactly one question.

That became the pattern I started following:

**reduce the system until only the problem you are testing remains.**

## The Arm Was Correct in Software and Wrong in Real Life

The next problem was different.

The servos were responding correctly, but some joints still did not line up properly.

The software might say 90 degrees, but a servo horn installed a few degrees off meant the physical arm did not agree.

At first, I thought the solution was to keep taking the joints apart and repositioning the horns.

Then I added a `SERVO_OFFSETS` configuration.

Each joint could have a small calibration value applied in software.

The issue was mechanical.

The most practical fix was partly software.

That made me stop thinking of hardware and code as separate problems.

## Wi-Fi Was Working, but the IP Was 0.0.0.0

One of the stranger bugs appeared when the Arduino connected to Wi-Fi.

The serial output sometimes showed:

```text
0.0.0.0
```

as the IP address.

My first reaction was that the Wi-Fi connection had failed.

It had not.

The code was checking the IP address before DHCP had finished assigning one.

I added retry logic and waited for the connection to finish before treating the network as ready.

Again, the symptom pointed at one thing while the actual problem was somewhere else.

## The Debug Page Became Part of the Project

At first, I thought debugging tools were temporary.

Once everything worked, I assumed I would delete them.

I ended up doing the opposite.

I kept a separate `debug.html` page.

I kept serial status output.

I kept individual test tools.

I added clearer connection feedback.

Those tools are now part of how I work on Ashtavakra.

If I change something and the arm behaves differently, I do not want my only debugging method to be watching eight motors and guessing.

## My Debugging Process Changed

Early in the project, my debugging process looked something like this:

```text
Something fails
      ↓
Change code
      ↓
Change wiring
      ↓
Try again
      ↓
Hope
```

Now it is closer to:

```text
Something fails
      ↓
Identify the smallest part I can test
      ↓
Test one assumption
      ↓
Look at the result
      ↓
Make one change
      ↓
Test again
```

I still get stuck.

I still make wrong assumptions.

The difference is that I now have a way to work through them.

## What I Actually Learned

The biggest lesson from debugging Ashtavakra was not how to use an I2C scanner or how DHCP works.

It was learning that a complicated problem becomes much easier when I stop treating the whole robot as one thing.

The arm is mechanical parts, electronics, power, firmware, networking, and a web interface.

When something fails, I can separate those pieces and test them one at a time.

That sounds obvious now.

It was not obvious when I started.

And I think that change in how I solve problems has been one of the most valuable parts of building the robot.

**[See Ashtavakra on GitHub →](https://github.com/iamtilakpatel/ashtavakra)**  
**[Project page →](https://tilakpatel.me)**
