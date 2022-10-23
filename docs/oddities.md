---
title: Oddities
nav_order: 11
---

# Oddities

## Channel List

Some channels in the channel list have a channel number after them. This is because not all channel names are unique, and the core design was that in case channel numbers changed only channel name would be used for configuration.

Since there are a few channel names that are duplicates (e.g. Sky Comedy HD which currently appears as channel 114 and channel 308 with different content), the second and later channels in the list have the channel number appended. e.g Sky Comedy HD channel 144 is shown as 'Sky Comedy HD' whilst channel 308 is shown as 'Sky Comedy HD (308)', and is stored in the integrations configurationa s such.

Should Sky change the channel number at some future point, then it will be necessary to re-configure the integration.
