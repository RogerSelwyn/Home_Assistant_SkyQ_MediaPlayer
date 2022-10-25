---
title: Schedule Sensor
nav_order: 10
---

# Schedule Sensor

One sensor, updated every minute, is created per SkyQ device (not Minis) when 'Get Live Record Status' is enabled. The sensor shows the following items:
- Status
  - 'Scheduled' - There is an item scheduled in the future to record
  - 'Scheduled - off' - There is an item scheduled but the box is switched off
  - 'None' - Nothing is scheduled
- Scheduled Start Time (UTC)
- Scheduled End Time (UTC)
- Scheduled Title
- Recordings (array) - recordings currently in progress
  - Recording Start Time (UTC)
  - Recording Scheduled End Time (UTC)
  - Recording Title 
