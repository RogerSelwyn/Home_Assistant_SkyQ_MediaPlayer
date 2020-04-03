[![CodeFactor](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer/badge)](https://www.codefactor.io/repository/github/rogerselwyn/home_assistant_skyq_mediaplayer)


# Custom Component for SkyQ Integration for Home Assistant

The skyq platform allows you to control a SkyQ set top box. 

**Note:** Whilst it will pull back information for UK boxes for current channel and live programme, it will not for non-UK boxes (unless they happen to use the same data sources, which is unlikely). If there is sufficient interest I can add a config option to disable it trying to retrieve live TV info, so that the integration does not error. However, in my opinion it then becomes a very limited integration

There is currently support for the following device types within Home Assistant:

-   Media Player

## Installation

To begin with it is recommended you ensure your SkyQ set top box or boxes have static IP addresses.

Download the custom component in to your folder <config_directory>/custom_components/skyq

# Media Player Configuration 

### Example of basic configuration.yaml
```
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   get_live_tv: True
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
```

## Configuration variables

media_player:
**platform** (string)(Required) 
Must be set to skyq

**host** _(string)(Required)_
The IP of the  SkyQ  set top box, e.g., 192.168.0.10.

**name** _(string)(Required)_
The name you would like to give to the  SkyQ  set top box.

**sources** _(list)(Required)_
List of channels or other commands that will appear in the source selection.

**name** _(string)(Required)_
The name you would like to give to the  SkyQ  set top box.

**output_programme_image** _(boolean)(Optional)_ Default True
Enables you to disable returning images when watching recorded programmes. Useful if using a modified media player UI, where you don't want the background changing.

**get_live_tv** _(boolean)(Optional)_ Default True
Ebales you to disable the retrieval of live TV programme. Useful for peoiple in those countries where the TV schedules are not available from awk.epgsky.com.

### Sources

To configure sources, set as 
```
<YourChanneName> : ‘<button>,<button>,<button>’.
```
### Supported buttons

sky, power,  tvguide  or home,  boxoffice, search, sidebar, up, down, left, right, select,  channelup,  channeldown,  i, dismiss, text, help,

play, pause, rewind,  fastforward, stop, record

red, green, yellow, blue

0, 1, 2, 3, 4, 5, 6, 7, 8, 9

### Next/Previous Buttons

The behaviour of the next and previous buttons is fastforward and rewind (multiple presses to increase speed, play to resume)


# Switch Generation Helper
A utility function has been created to generate yaml configuration for SkyQ enabled media players to support easy usage with other home assistant integrations, e.g. google home

Usage based on google home:  _“turn on <source name / channel name> in the ”_

## Configuration

**generate_switches_for_channels** _(boolean)(Optional)_ Default False
Generate switches for each item listed in source.
The files will be generated in <config folder>/skyq<room>.yaml

**config_directory** _(string)(Optional)_ Default '/config/'
The location of your configuration folder. 

The correct path required if generate_switches_for_channels is set to True to enable output generation of yaml files to the correct location

Hassbian default would be -  config_directory: '/home/homeassistant/.homeassistant/' or '/config/' for hassio

**room**
_(string)(Optional)_ Default 'Default Room'
The room where the  SkyQ  set top box is located. 

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
   config_directory: '/home/homeassistant/.homeassistant/'
   generate_switches_for_channels: true
```

To integrate these generated switch configuration files, add the generated yaml to your configuration.yaml. The following example configuration implements the generated switches from the generate_switches_for_channels function.

```
switch:
- platform: template
  switches: !include  skyq<room*>.yaml
```

