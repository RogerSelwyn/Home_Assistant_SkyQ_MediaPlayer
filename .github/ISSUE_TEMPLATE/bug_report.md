---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: Bug
assignees: ''

---

**Describe the bug**  
A clear and concise description of what the bug is.

**To Reproduce**  
Steps to reproduce the behavior:

**Expected behavior**  
A clear and concise description of what you expected to happen.

**Screenshots**  
If applicable, add screenshots to help explain your problem.

**Component versions**  
1. What version of SkyQ component are you using?
2. What was the last version where the problem was not shown?

**Your configuration**  
How have you setup your devices, by UI or YAML?

**Either - Your configuration from the options dialogue**  
Assuming you have the diagnostics enabled in your install, you can download your configuration from the Device dialogue by clicking on the three dots at bottom right of the Device Info card.

**Or - Your configuration.yaml**  
```yaml
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   live_tv: True
   country: "UK"
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
````
**Output of HA logs**  
Paste the relavant output of the HA log here.

**Additional context**  
Add any other context about the problem here.
