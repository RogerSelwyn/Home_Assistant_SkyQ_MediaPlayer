The skyq platform allows you to control a SkyQ  set top box.

There is currently support for the following device types within Home Assistant:

-   Media Player

To begin with ensure your  SkyQ  set top box or boxes have static IP addresses.

Download the custom component into <config_folder>/custom_components/skyq

# Media Player

## Configuration

To add a  SkyQ  to your installation, add the following to your configuration.yaml file:

### Configuration variables

media_player:
-  platform:  skyq

**host**
_(string)(Required)_
The IP of the  SkyQ  set top box, e.g., 192.168.0.10.

**name**
_(string)( Required)_
The name you would like to give to the  SkyQ  set top box.

**sources**
_(list)( Required)_
List of channels or other commands that will appear in the source selection.

**room**
_(string)( Required)_
The room where the  SkyQ  set top box is located. 
Avoid using [ ] in the name: or room: of your device.

**name**
_(string)( Required)_
The name you would like to give to the  SkyQ  set top box.

**config_directory**
_(string)( Required)_
The location of your default configuration folder.

Hassbian default would be -  config_directory: '/home/homeassistant/.homeassistant/'
or 
'/config/' for hassio

# Switch Generation
A utilility function has been created to generate yaml configuraition for skyq enabled media players to support easy usage with ohter home assistant integrations lke google home

## Configuration

**generate_switches_for_channels**
_(boolean)( Required)_
Generate switches for each item listed in source.
The files will be generated in <config folder>/skyq<room>.yaml

Usage based on google home:  _“turn on <source name / channel name> in the ”_

To integrate these, add the generated  yaml, to your  configuration.yaml

The following example configuration implements the generated switches from the generate_switches_for_channels function.
```
switch:
- platform: template
  switches: !include  skyq<room*>.yaml
```

A full configuration example will look like the sample below:

# Example  configuration.yaml  entry
```
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   room: Living Room
   config_directory: '/home/homeassistant/.homeassistant/'
   generate_switches_for_channels: true
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
```

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

The behaviour of the next and previous buttons is  fastforward  and rewind (multiple presses to increase speed, play to resume)

