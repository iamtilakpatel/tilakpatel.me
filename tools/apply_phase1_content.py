#!/usr/bin/env python3
"""Apply the approved Phase 1 homepage editorial spec to content/data.json.

One-time tool: rewrites the `nav` and `home` objects with the copy approved in
"Final Homepage Editorial Specification v2" + the follow-up adjustments.
All copy below traces to approved decisions; factual fields trace to the
existing data.json / Markdown frontmatter. Run:  python tools/apply_phase1_content.py
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "content" / "data.json"
data = json.loads(DATA.read_text(encoding="utf-8"))

data["nav"] = {
    "brand": "TILAK PATEL",
    # Subpage navigation (labels updated per approved spec; real routes preserved)
    "links": [
        {"label": "My Journey", "url": "/about.html"},
        {"label": "Projects", "url": "/projects.html"},
        {"label": "Build Log", "url": "/blog.html"},
    ],
    # Homepage anchor navigation (visual design of the approved mockup)
    "home_anchors": [
        {"label": "Projects", "url": "#projects"},
        {"label": "Build Log", "url": "#build-log"},
        {"label": "Journey", "url": "#timeline"},
        {"label": "Beyond", "url": "#beyond"},
    ],
    "cta": {"label": "Contact", "url": "/#contact"},
}

data["home"] = {
    "hero": {
        "greeting": "Hi, I'm",
        "name_first": "Tilak",
        "name_last": "Patel",
        "role_start": "I like finding out why things work — ",
        "role_accent": "then building a better version.",
        "tagline": "Freshman · St. Charles North High School · Class of 2030",
        "intro": "In sixth grade, I built a LEGO grabber that could reach and grip, but couldn't bend the way I wanted. That question stayed with me. Today, I'm building robots and exploring engineering questions about life in space. This is where I share what I build, what goes wrong, and what I learn along the way.",
        "photo": "/assets/images/hero-photo.jpg",
        "photo_alt": "Tilak Patel",
        "buttons": [
            {"label": "Explore My Projects", "url": "#projects", "style": "primary", "arrow": "↓"},
            {"label": "Read My Story", "url": "#timeline", "style": "secondary", "arrow": "↘"},
        ],
    },
    "featured": {
        "heading": "Featured Engineering",
        "note": "Not everything here is finished. That is the point.",
    },
    "projects": [
        {
            "id": "aero-lite",
            "flagship": True,
            "label": "AERO-LITE · SPACE SYSTEMS",
            "award_note": "Top Individual Award · Middle School Division · NASA Carbon Capture Challenge 2026",
            "headline": "How could astronauts manage CO₂ on the Moon?",
            "description": "I started AERO-LITE after learning about a carbon capture challenge at Space Center Houston. My first approach was to compress cabin air directly, but after examining the problem more closely, I redesigned the system to concentrate CO₂ first. That decision shaped the prototype I eventually built.",
            "image": "/assets/images/aero-prototype.jpg",
            "image_alt": "AERO-LITE Phase 1 prototype — three mason jars with zeolite beads, silica gel, and CO₂ sensors on a desk",
            "image_caption": "Phase 1 prototype: three mason jars, a live ESP32-S3, and a dashboard updating every second.",
            "stats": [
                {"num": "3", "text": "live CO₂ sensors", "qualifier": "observed in the Phase 1 prototype"},
                {"num": "ESP32-S3", "text": "working prototype", "qualifier": "observed on the bench"},
                {"num": "Live", "text": "readings via web dashboard", "qualifier": "observed, updating every second"},
            ],
            "links": [
                {"label": "Explore the Build Story →", "url": "projects/aero-lite"},
                {"label": "GitHub ↗", "url": "https://github.com/iamtilakpatel/aero-lite"},
            ],
        },
        {
            "id": "ashtavakra",
            "flagship": False,
            "label": "ASHTAVAKRA · ROBOTICS",
            "note": "Independent project · Started in 8th grade, still evolving in high school",
            "headline": "The LEGO question became a Wi-Fi-controlled robotic arm.",
            "description": "After learning Arduino, electronics, and programming, I returned to that early idea as a six-degree-of-freedom arm controlled through a browser. I wrote the Arduino firmware myself, connected eight servos through a motor driver, and built the browser controls — so a command on screen could move a real joint.",
            "stats": [
                {"num": "6", "text": "degrees of freedom"},
                {"num": "8", "text": "servo motors"},
                {"num": "Wi-Fi", "text": "browser control"},
            ],
            "links": [
                {"label": "Explore the Build Story →", "url": "projects/ashtavakra"},
                {"label": "GitHub ↗", "url": "https://github.com/iamtilakpatel/ashtavakra"},
            ],
        },
    ],
    "build_log": {
        "heading": "Build Log",
        "intro": "What worked. What did not. What I learned.",
        "cards": [
            {
                "category": "Problem-solving",
                "tag": "Debugging",
                "headline": "The Robotic Arm Didn't Work. So I Stopped Guessing.",
                "excerpt": "I started by changing code until something worked. After a fried board, a missing I2C device, and strange servo channels, I learned a better way to solve: isolate one problem, test one assumption, and collect evidence before changing anything.",
                "url": "robotic-arm-engineering-problems.html",
                "link_label": "Read the build note →",
            },
            {
                "category": "Engineering judgment",
                "tag": "Rethinking",
                "headline": "The Calculation That Changed My Design",
                "excerpt": "I wanted to compress cabin air directly, but compression alone would not separate out CO₂. The numbers made me rethink the design: capture CO₂ first, then consider compressing a concentrated stream. That is where AERO-LITE changed direction.",
                "url": "capture-first-compress-later.html",
                "link_label": "Read the build note →",
            },
            {
                "category": "Communication",
                "tag": "Clear thinking",
                "headline": "Building It Wasn't the Same as Explaining It",
                "excerpt": "Eight slides and a prototype with live CO₂ readings. What I learned about explaining a technical project without exaggerating what my first prototype actually proved.",
                "url": "nasa-challenge-submission.html",
                "link_label": "Read the reflection →",
            },
        ],
        "all_link": {"label": "All Blog Posts →", "url": "blog.html"},
    },
    "journey": {
        "heading": "From Gears to Space Systems",
        "subtitle": "Each build raised a new question — and led me to the next one.",
        "link": {"label": "Explore the complete journey →", "url": "about.html"},
        "milestones": [
            {"date": "4TH–5TH GRADE · GEARS", "status": "completed", "status_label": "Completed", "title": "LEGO mechanisms", "text": "The first question that wouldn't let go."},
            {"date": "6TH GRADE · CODE + CIRCUITS", "status": "completed", "status_label": "Completed", "title": "Arduino starter kit", "text": "Code could make something happen in the real world."},
            {"date": "7TH–8TH GRADE · ROBOTICS", "status": "completed", "status_label": "Completed", "title": "From one servo to Ashtavakra", "text": "Controlling a mechanism from my phone became a 6-DoF arm."},
            {"date": "SPRING 2026 · SPACE SYSTEMS", "status": "completed", "status_label": "Completed", "title": "AERO-LITE takes shape", "text": "A lunar challenge pushed me past robotics — and made me revise the design."},
            {"date": "FALL 2026 · VISION AI", "status": "progress", "status_label": "In progress", "title": "From control to vision", "text": "Teaching Ashtavakra to sense more than it moves."},
            {"date": "LOOKING AHEAD · AEROSPACE", "status": "planned", "status_label": "Planned", "title": "The next question is still open", "text": "Bigger aerospace and rocketry builds, one testable question at a time."},
        ],
    },
    "beyond": {
        "heading": "Beyond the Workbench",
        "note": "A little about the person behind the projects.",
        "quote": "The projects may be mine, but the curiosity behind them has never grown alone.",
        "paragraphs": [
            "My dad gave me my first Arduino kit as a birthday gift. That small box of parts opened a new way to learn: ask a question, try something, and talk through what happened.",
            "He still mentors me with feedback and encouragement. That support has helped me keep investigating, revise my thinking, and explain what I am learning in my own voice.",
        ],
    },
    "how_i_build": {
        "heading": "How I Build",
        "note": "The tools matter. The way I test, debug, and document matters more.",
        "groups": [
            {"number": "01", "title": "Build", "text": "Start small, make a rough version real, and use it to discover what the sketch missed.", "chips": ["Prototype early", "Experiment"]},
            {"number": "02", "title": "Code", "text": "Test one assumption at a time and make the system's behavior visible before changing it.", "chips": ["Isolate the problem", "Expose the data"]},
            {"number": "03", "title": "Think", "text": "Compare trade-offs, improve the design from what I learn, and document the next decision.", "chips": ["Measure", "Revise", "Share"]},
        ],
        "more_link": {"label": "The fuller breakdown lives on the Journey page →", "url": "about.html"},
    },
    "contact": {
        "eyebrow": "STUDENT · BUILDER · ASPIRING AEROSPACE ENGINEER",
        "heading": "Want to compare notes?",
        "email_display": "iamtilakpatel [at] gmail [dot] com",
        "email": "iamtilakpatel@gmail.com",
        "copy_label": "Copy email",
        "github_label": "GitHub profile ↗",
        "github_url": "https://github.com/iamtilakpatel",
    },
}

DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("✓ content/data.json updated with approved Phase 1 copy")
