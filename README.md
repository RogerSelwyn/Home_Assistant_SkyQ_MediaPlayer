![Validate with hassfest](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/workflows/Validate%20with%20hassfest/badge.svg) ![Hacs Validate](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/workflows/Hacs%20Validate/badge.svg) [![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer/badge)](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer) [![Downloads for latest release](https://img.shields.io/github/downloads/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/latest/total.svg)](https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/releases/latest)

![GitHub release](https://img.shields.io/github/v/release/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer) [![maintained](https://img.shields.io/maintenance/yes/2021.svg)](#) [![maintainer](https://img.shields.io/badge/maintainer-%20%40RogerSelwyn-blue.svg)](https://github.com/RogerSelwyn) [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) [![Community Forum](https://img.shields.io/badge/community-forum-brightgreen.svg)](https://community.home-assistant.io/t/custom-component-skyq-media-player/140306)


# Sky Q component for Home Assistant

The skyq platform allows you to control a Sky Q set top box.

**Note:** Whilst it will pull back information for current channel and live programme, it will do this for a very limited set of countries (currently UK, and any countries that use the same EPG/images, plus Italy and Germany). If you are in an unsupported country, or don't want this information set 'live_tv' to False in your config.

If you are able to supply details on where to reliably retrieve EPG information and images from, please raise a Feature Request with the relevant details and I'll look to include.

There is currently support for the following device types within Home Assistant:

- Media Player

### [Buy Me A ~~Coffee~~ Beer 🍻](https://buymeacoffee.com/rogtp)
I work on this integration because I like things to work well for myself and others, and for it to deliver as much as is achievable with the API. Please don't feel you are obligated to donate, but of course it is appreciated.

## Screenshots

_Component showing current TV with default media control_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_1.png">

_Component showing application with default media control_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_2.png">

_Component showing recording with [Mini Media Player](https://github.com/kalkih/mini-media-player)_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_3.png">

_Media Browser_

<img src="https://github.com/RogerSelwyn/Home_Assistant_SkyQ_MediaPlayer/blob/master/screenshots/skyq_4.png">

## Installation

You can use HACS by adding this repository as a custom Integration repository in HACS settings, or install the component manually:

- Put the files from `/custom_components/skyq/` in your folder `<config directory>/custom_components/skyq/`

If you wish to add to the provided application images (such as Netflix) place '.png' images names the same as the application in the following folder:

- `<config directory>/custom_components/skyq/static/`

For channels where there is no EPG, this can also be utilised to provide a channel image. Place an image file in the same directory with the same name as your channel source name (e.g. raiuno.png).

# Media Player Configuration

There are two methods of configuration, via the Home Assistant Integrations UI dialogue or via YAML. You cannot use both for the same Sky Q box, please use one or the other. Previous YAML configurations are not migrated to the UI method, please continue to use YAML, or delete YAML, reboot and add via UI.

## Integrations UI (from v2.2.0)

On the Integrations page, click to add a new Integration and search for Sky Q. Sky Q will only be visible if you have previously installed via one of the methods above and have restarted Home Assistant.

You will be asked to enter a host (which must be contactable on your network and name). The name defaults to Sky Q. Assuming the Sky Q box is switched on and the details are correct a device and entity will be created and be useable. You can then configure other items by clicking on Options on the Sky Q Integration card. Details are below.

If you want to add a second Sky Q box, just follow the same process again and add a new instance of the integration.

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

| **YAML**                                        | **UI**                            | **Default** | **Details** |
| ------------------------------------------------|-----------------------------------|:-----------:|-------------|
| platform<br>_(string)(Required)_                | n/a                               |             |Must be set to skyq |
| host<br>_(string)(Required)_                    | Host                              |             | The IP of the SkyQ set top box, e.g., 192.168.0.10. |
| name<br>_(string)(Required)_                    | Name                              |             | The name you would like to give to the SkyQ set top box. |
| sources<br>_(list)(Optional)_                   | Custom Sources                    |  _Empty_    | List of channels or other commands that will appear in the source selection. |
| output_programme_image<br>_(boolean)(Optional)_ |Show programme<br>image            | True        | Allows you to disable returning images when watching recorded programmes. Useful if using a modified media player UI, where you don't want the background changing. |
| live_tv<br>_(boolean)(Optional)_                | Show live TV<br>details           | True        | Allowsyou to disable the retrieval of live TV programme information. Useful for people in those countries where the TV schedules are not available from current known sources. |
| country<br>_(string)(Optional)_                 | Override Country | _Empty_     | Overrides the detected country from the SkyQ box. Currently supports "GBR", "ITA" and "DEU". In theory you shouldn't need to use this. |
| volume_entity<br>_(string)(Optional)_        | Entity to control<br>volume of | _Empty_     | Specifies the entity for which volume control actions will be passed through to. No validation of the entity is done via the UI, warnings will show in the log if an invalid entity is used. Must be a media_player entity. e.g. media_player.braviatv|
| epg_cache_len<br>_(integer)(Optional)_          | EPG Cache Length.                | 20           |Allows you to configure the number of EPG channels to cache for the media browser. Larger numbers will cause slower initial load per day and consume more memory. |

### Sources

To configure sources, set as:

#### Via UI

```
{"<YourChanneName>": "<button>,<button>,<button>", "<YourChanneName2>": "<button>,<button>,<button>"}.
```
Example 
```
{"BBC1HD": "1,1,5", "BBC2": "1,0,2"}
```

#### Via YAML

```
<YourChanneName> : ‘<button>,<button>,<button>’.
```
Example 
```
  BBC1HD: "1,1,5"
  BBC2: "1,0,2"
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

## Media Browser

Fetching data to support live programme information for the Media Browser is data intensive, so the information for upto 20 channels are cached to improve performance. The first media browser access per day will be slow (whilst the data is fetched), further accesses will utilise cached data. If the programme line up for a channel changes during the day, this will not be reflected in the media browser.

Images for the current live programme on each channel should show along with the title of each programme. These are identified via the channel number, so if you are using a 'custom' source with a Sky Q favourite it won't be able show the live programme. Applications can be included, but for an image to show the image file name in your www directory needs to match the name of the custom source.

In custom sources, if you have 'backup' as your first command, then this will be ignored when identifying the channel number to lookup the live programme for. This will not impact the set of commands sent to the Sky Box when you select a channel.

# Switch Generation Helper

A utility function has been created to generate yaml configuration for SkyQ enabled media players to support easy usage with other home assistant integrations, e.g. google home

Usage based on Google home: _“turn on <source name / channel name> in the ”_

## Configuration

| **YAML**                                        | **UI**                            | **Default** | **Details** |
| ------------------------------------------------|-----------------------------------|:-----------:|-------------|
| generate_switches_for_channels<br>_(boolean)(Optional)_ | Generate switches for channels | False | Generate switches for each item listed in source. The files will be generated in <config folder>/skyq<room>.yaml |
|room<br>_(string)(Optional)_                    | Room name                         | Default Room | The room where the SkyQ set top box is located. |

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
  switches: !include  skyq<room>.yaml
```

## Aliases

Because the name of the channel may not always be what you want to use to talk to Google Home, it is possible to place an alias file in the root of your Home Assistant configuration. This needs to be called `skyqswitchalias.yaml`. It is also possible to use this to rename some of the default switches, so you can change `play` to `engage` for example. The contents should be pairs of switchname and alias as below:

```
BBC One South: BBC South
ComedyCentHD: Comedy Central HD
SkySpMainEvHD: Sky Sports Main Event HD
SkySp PL HD: Sky Sports Premier League HD
SkyPremiereHD: Sky Premiere HD
SkyFamilyHD: Sky Family HD
play: engage
```

