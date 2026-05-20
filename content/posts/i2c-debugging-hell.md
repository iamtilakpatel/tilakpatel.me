---
date: May 2026
title: Three Days in I²C Debugging Hell
tags: [ESP32, I2C, Debugging]
excerpt: The SCD41 would not show up on the scanner. I checked wiring, pull-ups, addresses, and nearly gave up. Then I realized the multiplexer channel mask was wrong. A story about patience, Serial Monitor, and why sleep matters.
slug: i2c-debugging-hell
---

It was supposed to be simple. Three SCD41 CO₂ sensors, one TCA9548A multiplexer, one ESP32-S3. Turn it on, scan the bus, see three devices. Instead I saw: **❌ NO DEVICES FOUND.**

## Day 1: It Is the Wiring

I checked every wire three times. SDA to GPIO 4. SCL to GPIO 5. 3.3V to VCC. GND to GND. I even color-coded them so I would not get confused. The I²C scanner still showed nothing.

I added 4.7kΩ pull-up resistors because the internet said to. Still nothing. I removed them because maybe the ESP32 internal pull-ups were enough. Still nothing. I put them back because I was desperate. Still nothing.

I went to bed angry.

## Day 2: It Is the Address

The SCD41 default address is 0x62. I checked the datasheet. I checked my code. I even printed the address in hex to make sure I was not going crazy. The address was right.

I tried swapping sensors. Maybe one was dead? I tried each sensor directly on the bus without the multiplexer. They all worked individually. The sensors were fine. The ESP32 was fine. The mux was the problem.

I went to bed frustrated.

## Day 3: The Multiplexer

I sat down with the TCA9548A datasheet and read it line by line. The control register expects a channel mask: 0x01 for channel 0, 0x02 for channel 1, 0x04 for channel 2.

My code said: `Wire.write(1 << ch);`

That should work. 1 << 0 = 0x01. 1 << 1 = 0x02. 1 << 2 = 0x04. Perfect, right?

Except... I was calling `tcaSelect(ch)` with `ch = 0, 1, 2` for my three sensors. But somewhere in my init code, I had a copy-paste error where I was passing the wrong variable. One sensor init was calling `tcaSelect(0)` but then talking to the library as if it was on a different channel.

The mux was switching to channel 0, but my SCD41 library call was trying to read from the default bus without re-selecting the channel afterward. The channel got reset between the mux select and the sensor read.

I fixed it by making `tcaSelect()` part of every single read and write. No assumptions. The sensor read function now looks like:

```cpp
tcaSelect(0);
err = scd0.getDataReadyStatus(ready);
if (err == NO_ERROR && ready) {
    err = scd0.readMeasurement(co2, t, rh);
}
```

At 1:14 AM, the Serial Monitor printed:

```
[OK]  Ch0 Cabin running
[OK]  Ch1 Purified running
[OK]  Ch2 CO2 Tank running
```

I yelled. My mom knocked on my door to make sure I was okay.

## What I Learned

- **Never assume the bus state.** Always re-select the mux channel before every transaction.
- **Sleep matters.** Day 1 and Day 2 I was exhausted and chasing wrong theories. Day 3 I was rested and found it in an hour.
- **The Serial Monitor is your best friend.** Add debug prints. Lots of them. You can remove them later.
