---
title: Media Browser
nav_order: 6
---

# Media Browser

Fetching data to support live programme information for the Media Browser is data intensive, so the information for upto 20 channels (configureable using the EPG Cache Length configuration value) are cached to improve performance. The first media browser access per day will be slow (whilst the data is fetched), further accesses will utilise cached data. If the programme line up for a channel changes during the day, this will not be reflected in the media browser.

Images for the current live programme on each channel should show along with the title of each programme. These are identified via the channel number, so if you are using a 'custom' source with a Sky Q favourite it won't be able show the live programme. Applications can be included, but for an image to show the image file name in your SkyQ install directory needs to match the name of the custom source.

In custom sources, if you have 'backup' as your first command, then this will be ignored when identifying the channel number to lookup the live programme for. This will not impact the set of commands sent to the Sky Box when you select a channel.
