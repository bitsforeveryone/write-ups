---
title: "grapefruit"
date: 2016-08-31T14:46:09-04:00
---

`grapefruit` is a suite of tools written by a few members of the team for use in
an Attack-Defend style CTF. The source is available on [Github][g].

[g]:https://github.com/bitsforeveryone/grapefruit

<!--more-->

It was written quickly, and there are bugs. However, we believe it addresses the
basic components needed to simplify Attack-Defense CTFs. There are 4 basic
components and all function independently.

### IDS

A simple IDS designed with CTFs in mind. Pcaps are parsed with tcpflow, and flows
are stored in an `sqlite3` database with an unobtrusive front-end written with Flask.

### Launcher

A CLI based throwing framework written in python for automating the scheduled
throwing of exploits and network chaff for distraction.

### Persistence

An experimental script for maintaining persistence on a box in a way that is
hard to observe in network traffic. Communications between the host and victim
change ports regularly, almost like frequency-hopping radio communications.

### Grapefuzz

Starter scripts for common fuzzing frameworks.

