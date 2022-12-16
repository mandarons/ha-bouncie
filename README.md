# bouncie

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [bouncie][bouncie]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from blueprint API.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `bouncie`.
4. Download _all_ the files from the `custom_components/bouncie/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/bouncie/translations/en.json
custom_components/bouncie/__init__.py
custom_components/bouncie/coordinator.py
custom_components/bouncie/config_flow.py
custom_components/bouncie/const.py
custom_components/bouncie/manifest.json
custom_components/bouncie/sensor.py
custom_components/bouncie/strings.json
```

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[bouncie]: https://github.com/mandarons/ha-bouncie
[buymecoffee]: https://www.buymeacoffee.com/mandarons
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/mandarons/ha-bouncie.svg?style=for-the-badge
[commits]: https://github.com/mandarons/ha-bouncie/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/mandarons/ha-bouncie.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-mandarons-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/mandarons/ha-bouncie.svg?style=for-the-badge
[releases]: https://github.com/mandarons/ha-bouncie/releases
