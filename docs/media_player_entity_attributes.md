---
title: Media Player Entity Attributes
nav_order: 8
---

# Media Player Entity Attributes

The media player provides a main status, plus a range of attributes. The main attributes are common with other HA media players and provide detail on the currently playing item:
- source_list: BBC One South, BBC Two HD, ITV
- media_content_type: tvshow
- media_title: BBC Two HD
- media_series_title: Planet Earth II: A World of Wonder
- media_season: 2
- media_episode: 7
- media_channel: BBC Two HD
- source: BBC Two HD
- entity_picture_local: /api/media_player_proxy/media_player.sky_q_mini?token=6418e8bac0e0065a5276f3407e80d3f10157dbd6d7be93fc3d96582cbd6be80c&cache=450f5a402a3ce01c
- device_class: tv
- entity_picture: https://imageservice.sky.com/pd-image/1c54548b-4afa-4d8a-aab4-19e7201c26bb/16-9/456?territory=GB&provider=SKY&proposition=SKYQ
- icon: mdi:satellite-variant
- friendly_name: Sky Q Mini
- supported_features: 154547

The following items are specific to the SkyQ media player and are items requested by users of the integration:
- skyq_media_type - shows current media type being played
  - app - an application such as Netflix is being played
  - live - a live programme is being played (unknown if it has been paused previously or not)
  - liverecord - a live programme is being played as well as being recorded
  - pvr - a recording is being played
- skyq_transport_status
  - OK - standard status when all is OK, even in standby.
  - ERROR_PIN_REQUIRED - when the box is awaiting PIN entry. This can be used as a means of triggering automatic PIN entry.
  - Not present - if box is in lower power mode (overnight) or for an unsupported box (e.g. Sky Glass)
- skyq_channelno - the Sky Q channel being played. Not present if no channel has been identified (e.g. YouTube is being viewed)
