---
title: Installation
nav_order: 2
---

# Installation

You can either use HACS or install the component manually:

- Put the files from `/custom_components/skyq/` in your folder `<config directory>/custom_components/skyq/`

If you wish to add to the provided application images (such as Netflix) place '.png' images with names the same as the application in the following folder:

- `<config directory>/custom_components/skyq/static/`

For channels where there is no EPG, this can also be utilised to provide a channel image. Place an image file in the same directory with the same name as your channel source name (e.g. raiuno.png).

### Media Player Configuration

There are two methods of configuration, via the [Home Assistant Integrations UI](./configuration_ui.md) dialogue or via [YAML](./configuration_yaml.md). You cannot use both for the same Sky Q box, please use one or the other. Previous YAML configurations are not migrated to the UI method, please continue to use YAML, or delete YAML, reboot and add via UI.

SSDP automatic discovery may also find your Sky Q devices giving you the option to install them with default names.
