---
date: May 2026
title: Three Days in I²C Debugging Hell
tags: [ESP32, I2C, Debugging]
excerpt: My three SCD41 sensors were not responding reliably through the I²C multiplexer. The channel-mask calculation was correct, but my code was not consistently selecting the right channel before sensor reads. A story about testing assumptions, the Serial Monitor, and why sleep matters.
slug: i2c-debugging-hell
---

It was supposed to be simple. Three SCD41 CO₂ sensors, one TCA9548A multiplexer, one ESP32-S3. Select each multiplexer channel, scan for its sensor, and get three responses. Instead I kept seeing: **❌ NO DEVICES FOUND.**

## Day 1: It Is the Wiring

I checked every wire three times. SDA to GPIO 4. SCL to GPIO 5. 3.3V to VCC. GND to GND. I even color-coded them so I would not get confused. The I²C scanner still showed nothing.

I added 4.7kΩ pull-up resistors because the internet said to. Still nothing. I removed them because maybe the ESP32 internal pull-ups were enough. Still nothing. I put them back because I was desperate. Still nothing.

I went to bed angry.

## Day 2: It Is the Address

The SCD41 default address is 0x62. I checked the datasheet. I checked my code. I even printed the address in hex to make sure I was not going crazy. The address was right.

I tried swapping sensors. Maybe one was dead? I tried each sensor directly on the bus without the multiplexer. They all worked individually. The sensors were fine. The ESP32 was fine. The mux was the problem.

I went to bed frustrated.

## Day 3: The Multiplexer

I sat down with the TCA9548A datasheet and read it line by line. Its control register uses a bit mask to select channels: `0x01` for channel 0, `0x02` for channel 1, and `0x04` for channel 2.

My code used `Wire.write(1 << ch);`. That calculation was correct. For `ch = 0, 1, 2`, it produces exactly those values.

So the **mask formula was not the bug**. The problem was how my code used the selected channel. My initialization and sensor-reading paths did not always agree about which channel should be active. I had been relying on a channel selection made elsewhere in the program instead of ensuring the correct sensor channel was selected when I needed it.

I changed the code to select the intended channel right before communicating with its sensor. I also checked the sensor operations one at a time instead of treating the whole three-sensor setup as one problem.

The relevant part of the sensor-reading code looked like this:

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

- **Do not assume which mux channel is active.** Select the intended channel before communicating with its sensor. The bit-mask formula can be correct while the wrong channel is selected in the rest of the code.
- **Sleep matters.** Day 1 and Day 2 I was exhausted and chasing wrong theories. Day 3 I was rested and found it in an hour.
- **The Serial Monitor is your best friend.** Add debug prints. Lots of them. You can remove them later.
