"""Pre-loaded authentic real-world field expert demonstrations for instant hackathon demos."""

SAMPLE_DEMOS = {
    "industrial_sensor": {
        "title": "Industrial Robot Rotary Sensor Calibration",
        "contributor_name": "Ramesh Patel",
        "domain": "industrial",
        "language": "en",
        "transcript": (
            "Listen carefully, because if you rush this, you'll fry a four thousand dollar optical encoder. "
            "First, before you even open the enclosure door, strap on your grounded anti-static wristband and clip it to the chassis ground rail. "
            "Never touch the gold contact pins with bare fingers—skin oils and static will corrupt the pulse train. "
            "Once grounded, turn the calibration dial counterclockwise slowly until the blue status LED blinks exactly three times. "
            "That puts the chip into zero-offset mode. "
            "Next, use an insulated ceramic screwdriver to adjust potentiometer R14 until the multimeter reads between 4.95 and 5.05 volts DC. "
            "If the LED starts rapid-flashing red instead of blue, stop immediately—that means the optical disk is misaligned or has dust. "
            "Blow it with dry canned air only, never wipe it with a rag. "
            "Finally, tighten the locking collar to 1.2 Newton-meters torque. Reconnect the harness and confirm the control panel shows 'Ready'."
        )
    },
    "solar_inverter": {
        "title": "Solar String Inverter Arc-Flash Safe Reset",
        "contributor_name": "Carlos Mendez",
        "domain": "solar",
        "language": "en",
        "transcript": (
            "When dealing with string inverter fault code F34, you have to treat the DC bus like a loaded weapon. "
            "First rule: never open the DC disconnect switch while the inverter is under full load. Check the display and isolate the AC grid breaker first. "
            "After flipping the AC breaker, switch the DC rotary isolator to OFF. "
            "Now wait at least five full minutes. Do not open the door before five minutes! The internal DC bus capacitors hold 800 volts and need time to bleed down. "
            "Put on your Arc Flash face shield and 1000V rated gloves. "
            "Open the access panel and probe terminal blocks DC+ and DC- with a verified CAT IV multimeter. Confirm the voltage is strictly under 10 volts. "
            "Inspect the fuse holders for thermal discoloration. If clear, press the red hardware reset button for 8 seconds until the relay clicks. "
            "Close the door, latch both quarter-turn locks, switch on the DC isolator first, and then the AC breaker. Monitor grid synchronization for 60 seconds."
        )
    },
    "smart_irrigation": {
        "title": "Soil Moisture & Salinity TDR Probe Field Calibration",
        "contributor_name": "Priya Sharma",
        "domain": "agriculture",
        "language": "en",
        "transcript": (
            "If an IoT soil salinity probe drifts, the automated valves will either drown the crops or starve them of nutrients. "
            "Start by carefully digging out the sensor head using a plastic spade—never use a metal trowel or you'll scratch the stainless steel wave-guides. "
            "Once retrieved, rinse the three stainless rods thoroughly with deionized distilled water. "
            "Do not wipe the rods with abrasive paper; dry them only with lint-free optical wipes. "
            "Submerge the probe into standard 1.413 milliSiemens conductivity reference calibration solution. "
            "On the handheld field communicator, select 'Two-Point TDR Calibration'. "
            "Wait 45 seconds for temperature stabilization between the fluid and thermistor. "
            "Verify the dielectric constant reading reads 80.1 plus or minus 0.5. "
            "If reading drifts more than 5 percent, the internal epoxy potting has cracked and moisture has entered; replace the probe entirely. "
            "Re-insert the probe horizontally into undisturbed root-zone soil at 30 centimeters depth, ensuring zero air pockets around the rods."
        )
    }
}
