![Validate with hassfest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/workflows/Validate%20with%20hassfest/badge.svg) ![Hacs Validate](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/workflows/Hacs%20Validate/badge.svg) [![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer/badge)](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer) [![Downloads for latest release](https://img.shields.io/github/downloads/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/latest/total.svg)](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/releases/latest)

![GitHub release](https://img.shields.io/github/v/release/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer) [![maintained](https://img.shields.io/maintenance/yes/2020.svg)](#) [![maintainer](https://img.shields.io/badge/maintainer-%20%40RogerSelwyn-blue.svg)](https://github.com/RogerSelwyn) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) [![Community Forum](https://img.shields.io/badge/community-forum-brightgreen.svg)](https://community.home-assistant.io/t/custom-component-skyq-media-player/140306)


# Sky Q component for Home Assistant

The skyq platform allows you to control a Sky Q set top box.

**Note:** Whilst it will pull back information for UK boxes for current channel and live programme, it will do this for a very limited set of countries (currently UK, and any countries that use the same EPG/images, plus Italy). If you are in an unsupported country, or don't want this information set 'live_tv' to False in your config.

There is currently support for the following device types within Home Assistant:

- Media Player

## Screenshots

_Component showing current TV with default media control_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_1.png">

_Component showing application with default media control_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_2.png">

_Component showing recording with [Mini Media Player](https://github.com/kalkih/mini-media-player)_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_3.png">

## Installation

You can use HACS by adding this reposity as a custom Integration repository in HACS settings, or install the component manually:

- Put the files from `/custom_components/skyq/` in your folder `<config directory>/custom_components/skyq/`

For either install method you must also:

- Put the files from `/www/community/skyq/` in your folder `<config directory>/www/community/skyq/`

# Media Player Configuration

There are two methods of configuration, via the Homa Assistant Integrations UI dialogue or via YAML. You cannot use both for the same Sky Q box, please use one or the other. Previous YAML configurations are not migrated the GUI method.

## Integrations UI

At Integrations page, click to add a new Integration and search for Sky Q. Sky Q will only be visible if you have previously installed via one of the methods above and have restarted Home Assistant.

You will be asked to enter a host (which must be contactable on your network and name). The name defaults to Sky Q. Assuming the Sky Q box is switched on and the details are correct a device and entity will be created and be useable. You can then configure other items by clicking on Options on the Sky Q Integration card. Details are below.

## YAML

Add a skyq platform entry in your configuration.yaml as below.

### Example of basic configuration.yaml

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

Items marked '#' are not used for UI based configuration



| **YAML**                                        | **UI**                            | **Default** | **Details** |
| ------------------------------------------------|-----------------------------------|:-----------:|-------------|
| platform<br>_(string)(Required)_                | n/a                               |             |Must be set to skyq |
| host<br>_(string)(Required)_                    | Host                              |             | The IP of the SkyQ set top box, e.g., 192.168.0.10. |
| name<br>_(string)(Required)_                    | Name                              |             | The name you would like to give to the SkyQ set top box. |
| sources<br>_(list)(Optional)_                   | Custom Sources                    |  _Empty_    | List of channels or other commands that will appear in the source selection. |
| output_programme_image<br>_(boolean)(Optional)_ |Show programme<br>image            | True        | Enables you to disable returning images when watching recorded programmes. Useful if using a modified media player UI, where you don't want the background changing. |
| live_tv<br>_(boolean)(Optional)_                | Show live TV<br>details           | True        | Enables you to disable the retrieval of live TV programme information. Useful for people in those countries where the TV schedules are not available from awk.epgsky.com. |
| country<br>_(string)(Optional)_                 | Generate switches<br>for channels | _Empty_     | Overrides the detected country from the SkyQ box. Currently supports "GBR" and "ITA". In theory you shouldn't need to use this. |

### Sources

To configure sources, set as:

#### Via UI

```
{"<YourChanneName>": "<button>,<button>,<button>", "<YourChanneName2>": "<button>,<button>,<button>"}.
```

#### Via YAML

```
<YourChanneName> : ‘<button>,<button>,<button>’.
```

### Supported buttons

- sky, power, tvguide or home, boxoffice, search, sidebar, up, down, left, right, select, channelup, channeldown, i, dismiss, text, help, 
- play, pause, rewind, fastforward, stop, record
- red, green, yellow, blue
- 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

### Next/Previous Buttons

The behaviour of the next and previous buttons is fastforward and rewind (multiple presses to increase speed, play to resume)

### Sending Button Commands

If you are using [Mini Media Player](https://github.com/kalkih/mini-media-player) or some other player that supports sending 'play_media' commands, you can configure this in the front-end rather than having to configure a source and then assigning it to a button. For example, the below will send the 'channelup' button command to the Sky box:

```
shortcuts:
  buttons:
    - icon: 'mdi:chevron-up'
      id: channelup
      type: skyq
```
# Switch Generation Helper

A utility function has been created to generate yaml configuration for SkyQ enabled media players to support easy usage with other home assistant integrations, e.g. google home

Usage based on google home: _“turn on <source name / channel name> in the ”_

## Configuration

**generate_switches_for_channels** _(boolean)(Optional)_ Default False  
Generate switches for each item listed in source.
The files will be generated in <config folder>/skyq<room>.yaml

**room**_(string)(Optional)_ Default 'Default Room'  
The room where the SkyQ set top box is located.

Avoid using [ ] in the name: or room: of your device. This field is required if you have more than one SkyQ box being configured with switches

### Example configuration.yaml with switch generation

```
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
   room: Living Room
   generate_switches_for_channels: true
```

To integrate these generated switch configuration files, add the generated yaml to your configuration.yaml. The following example configuration implements the generated switches from the generate_switches_for_channels function.

```
switch:
- platform: template
  switches: !include  skyq<room*>.yaml
```
