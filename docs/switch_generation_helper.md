---
title: Switch Generation Helper
nav_order: 7
---

# Switch Generation Helper

A utility function has been created to generate yaml configuration for SkyQ enabled media players to support easy usage with other home assistant integrations, e.g. google home

Usage based on Google home: _“turn on <source name / channel name> in the ”_

## Configuration

| **YAML**                                        | **UI**                            | **Default** | **Details** |
| ------------------------------------------------|-----------------------------------|:-----------:|-------------|
| generate_switches_for_channels<br>_(boolean)(Optional)_ | Generate switches for channels | False | Generate switches for each item listed in source. The files will be generated in <config folder>/skyq<room>.yaml |
|room<br>_(string)(Optional)_                    | Room name                         | Default Room | The room where the SkyQ set top box is located. |

Avoid using [ ] in the name: or room: of your device. This field is required if you have more than one SkyQ box being configured with switches

**Example configuration.yaml with switch generation**

```yaml
media_player:
 - platform:  skyq
   name: SkyQ Living Room
   host: 192.168.0.10
   sources:
      SkyOne: '1,0,6'
      SkyNews: '5,0,1'
   generate_switches_for_channels: true
   room: Living Room
```

To integrate these generated switch configuration files, add the generated yaml to your configuration.yaml. The following example configuration implements the generated switches from the generate_switches_for_channels function.

```yaml
switch:
- platform: template
  switches: !include  skyq<room>.yaml
```

## Aliases

Because the name of the channel may not always be what you want to use to talk to Google Home, it is possible to place an alias file in the root of your Home Assistant configuration. This needs to be called `skyqswitchalias.yaml`. It is also possible to use this to rename some of the default switches, so you can change `play` to `engage` for example. The contents should be pairs of switchname and alias as below:

```yaml
BBC One South: BBC South
ComedyCentHD: Comedy Central HD
SkySpMainEvHD: Sky Sports Main Event HD
SkySp PL HD: Sky Sports Premier League HD
SkyPremiereHD: Sky Premiere HD
SkyFamilyHD: Sky Family HD
play: engage
```
