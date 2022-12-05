---
title: Schedule Sensor
nav_order: 10
---

# Schedule Sensor

One sensor, updated every minute, is created per SkyQ device (not Minis). The sensor is disabled by default. The sensor shows the following items:
- Status
  - 'scheduled' - There is an item scheduled in the future to record
  - 'recording' - There is an item being recorded currently
  - 'none' - Nothing is scheduled
- Box State - Powered on/off state 
- Scheduled Start Time (UTC)
- Scheduled End Time (UTC)
- Scheduled Title
- Recordings (array) - recordings currently in progress
  - Recording Start Time (UTC)
  - Recording Scheduled End Time (UTC)
  - Recording Title 
