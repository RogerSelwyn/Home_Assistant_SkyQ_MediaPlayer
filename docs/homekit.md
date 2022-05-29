---
title: Homekit
nav_order: 9
---

# Homekit

The integration will expose the relevant controls to Homekit as long as it is configured in the Homekit integration. The Sky Q media player should be exposed as an accesory. Normally you will want `tv_device_class` to be enabled to provide the maximum functionality to Homekit, since this presents the box as a TV which can be managed by Apple Remote. If `tv_device_class` is disabled, then the Sky Q box is presented as a Receiver to Homekit which then presents a set of switches in the Home app. Note that in the list of available channels that is presented in the Home app, the current channel is always available even if not configured as a source in HA.
