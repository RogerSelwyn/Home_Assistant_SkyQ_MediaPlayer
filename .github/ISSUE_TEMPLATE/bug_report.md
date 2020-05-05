---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. What were you doing/watching at the time ?
2. What channel were you on?
3. What time did the problem occur?
4. Where are you (bear in mind component supports GBR/ITA at the moment)?

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Your config.yaml**
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
