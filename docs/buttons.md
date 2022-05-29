---
title: Buttons
nav_order: 5
---

# Buttons

## Supported buttons

- sky, power, tvguide or home, boxoffice, search, sidebar, up, down, left, right, select, channelup, channeldown, i, dismiss, text, help,
- play, pause, rewind, fastforward, stop, record
- red, green, yellow, blue
- 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

## Next/Previous Buttons

The behaviour of the next and previous buttons is fastforward and rewind (multiple presses to increase speed, play to resume)

## Sending Button Commands

If you are using [Mini Media Player](https://github.com/kalkih/mini-media-player) or some other player that supports sending 'play_media' commands, you can configure this in the front-end rather than having to configure a source and then assigning it to a button. For example, the below will send the 'channelup' button command to the Sky box:

```
shortcuts:
  buttons:
    - icon: 'mdi:chevron-up'
      id: channelup
      type: skyq
```
You can also send a sequence of commands as a service call such as the below ('backup' is included here because you may need to exit the Sky EPG, it is not required):

```
service: media_player.play_media
target:
  entity_id: media_player.sky_q
data:
  media_content_type: skyq
  media_content_id: 1,0,5
```
