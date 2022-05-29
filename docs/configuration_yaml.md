---
title: YAML Configuration
nav_order: 4
---

# YAML Configuration

Add a skyq platform entry in your configuration.yaml as below.

**Example of basic configuration.yaml**

```
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   live_tv: True
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
```

## Configuration variables

| **YAML**                                        | **Default** | **Details** |
| ------------------------------------------------|:-----------:|-------------|
| platform<br>_(string)(Required)_                |             |Must be set to skyq |
| host<br>_(string)(Required)_                    |             | The IP of the SkyQ set top box, e.g., 192.168.0.10. |
| name<br>_(string)(Required)_                    |             | The name you would like to give to the SkyQ set top box. |
| sources<br>_(list)(Optional)_                   |  _Empty_    | List of channels or other commands that will appear in the source selection. |
| output_programme_image<br>_(boolean)(Optional)_ | True        | Allows you to disable returning images when watching recorded programmes. Useful if using a modified media player UI, where you don't want the background changing. |
| live_tv<br>_(boolean)(Optional)_                | True        | Allows you to disable the retrieval of live TV programme information. Useful for people in those countries where the TV schedules are not available from current known sources. |
| get_live_record<br>_(boolean)(Optional)_                | False       | Allows you to fetch the status of the currently playing item to see if it is a "Live Recording". |
| tv_device_class                             | True    | Sets device class to TV. Unticked sets it to Receiver. |
| country<br>_(string)(Optional)_                 | _Empty_     | Overrides the detected country from the SkyQ box. Currently supports "GBR", "ITA" and "DEU". In theory you shouldn't need to use this. |
| volume_entity<br>_(string)(Optional)_        | _Empty_     | Specifies the entity for which volume control actions will be passed through to. No validation of the entity is done via the UI, warnings will show in the log if an invalid entity is used. Must be a media_player entity. e.g. media_player.braviatv|
| epg_cache_len<br>_(integer)(Optional)_          | 20           |Allows you to configure the number of EPG channels to cache for the media browser. Larger numbers will cause slower initial load per day and consume more memory. |

## Sources

```
<YourChanneName> : ‘<button>,<button>,<button>’.
```
Example
```
  BBC1HD: '1,1,5'
  BBC2: '1,0,2'
```
