---
name: solar-inverter-arc-flash-reset
description: Standard operating procedure for solar inverter arc flash reset derived
  from field expert demonstration.
version: 1.0.0
license: Apache-2.0
author: Carlos Mendez
domain: solar
tags:
- solar
- field-ops
- expert-captured
fidelity_score: 95
status: certified
verified_by: Elena Rostova, Chief Inspector (SOLAR-991)
certifying_authority: Clean Energy Technical Alliance
audit_timestamp: '2026-10-04T07:24:48.497283Z'
signature_seal: 1eba1568a2ef83c3101b4213583875c95ee440ec9287aa34aff0ac20d151382f
---

# Solar Inverter Arc Flash Reset

## Overview
Standard operating procedure for solar inverter arc flash reset derived from field expert demonstration.

Originally captured from spoken field demonstration by **Carlos Mendez** (solar domain, source language: en).

## When to Use (Triggers)
- User encounters operational inconsistency in solar hardware
- Routine maintenance or diagnostic check for solar-inverter-arc-flash-reset
- Field technician needs guidance on When dealing with string inverter fault code F34, 

## Prerequisites & Tools
- Standard insulated hand tools
- Multimeter or calibration monitor
- Personal Protective Equipment (PPE)

## Step-by-Step Procedure
1. When dealing with string inverter fault code F34, you have to treat the DC bus like a loaded weapon
2. First rule: never open the DC disconnect switch while the inverter is under full load
3. Check the display and isolate the AC grid breaker first
4. After flipping the AC breaker, switch the DC rotary isolator to OFF
5. Now wait at least five full minutes
6. Do not open the door before five minutes! The internal DC bus capacitors hold 800 volts and need time to bleed down
7. Put on your Arc Flash face shield and 1000V rated gloves
8. Open the access panel and probe terminal blocks DC+ and DC- with a verified CAT IV multimeter

## Safety Warnings & Critical Gotchas
- ⚠️ **CRITICAL:** First rule: never open the DC disconnect switch while the inverter is under full load

## Troubleshooting & Diagnostics
- **Issue:** LED fails to blink or signal out of range
  **Resolution:** Check grounding wire contact and re-zero.
- **Issue:** Inconsistent voltage readout
  **Resolution:** Inspect gold connector pins for surface oxidation or static damage.

