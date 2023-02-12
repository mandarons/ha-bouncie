# bouncie

[![CI - Main][build-shield]][build]
[![Tests](https://mandarons.github.io/ha-bouncie/badges/tests.svg)](https://mandarons.github.io/ha-bouncie/test-results/)
[![Coverage](https://mandarons.github.io/ha-bouncie/badges/coverage.svg)](https://mandarons.github.io/ha-bouncie/test-coverage/index.html)
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Discord][discord-badge]][discord]
<a href="https://www.buymeacoffee.com/mandarons" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 150px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

:love_you_gesture: Please star this repository if you end up using this integration. If it improved your life in any way, consider donating for my effort using 'Buy Me a Coffee' button above or sponsoring this project using GitHub Sponsors. It will help me continue supporting this product. :pray:

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) download `bouncie.zip` from [latest release](https://github.com/mandarons/ha-bouncie/releases/latest/).
4. Unzip `bouncie.zip` file in `custom_components` folder.
5. Restart Home Assistant
6. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "bouncie"

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

The `bouncie` integration uses the [Bouncie](https://www.bouncie.dev/) web service as a source for monitoring your car(s).

## Setup

To generate an Bouncie application credentials -

1. Go to the [Bouncie Developer Page](https://bouncie.dev/) page
2. Login with your `bouncie.com` credentials
3. Click on `+ ADD APPLICATION`
4. Provide a `name` for application e.g. Home Assistant Integration
5. Provide a unique `client_id` e.g. alphanumeric random string
6. Provide redirect URL to be your Home Assistant URL
7. Click on `SAVE`
8. Click on the "Users & Devices" tab at the top of the page.
9. Click on the "Authorize My Devices" blue button.
10. Choose 'Yes' when prompted to authorize devices to your application.
11. You should now see your account listed in the "Users & Devices" list.
12. Next to your listed account, click the "Expand" arrow to see your "Auhtorization Code"
13. Copy the alphanumeric listed under "Authorization Code" - this is your `authorization_code`
14. Note down following values to enter in Home Assistant
    1. Client ID
    2. Client Secret
    3. Redirect URL
    4. Authorization Code

> **Note**
>  This integration currently uses REST API only with polling. `scan_interval` (default is 10 seconds) can be set to a custom value in integration configuration setting.

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

---

[build]: https://github.com/mandarons/bounciepy/actions/workflows/ci-main-test-coverage.yml
[build-shield]: https://github.com/mandarons/bounciepy/actions/workflows/ci-main-test-coverage.yml/badge.svg
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg
[license-shield]: https://img.shields.io/github/license/mandarons/ha-bouncie.svg
[releases-shield]: https://img.shields.io/github/v/release/mandarons/ha-bouncie
[releases]: https://github.com/mandarons/ha-bouncie/releases
[discord]: https://discord.gg/HfAXY2ykhp
[discord-badge]: https://img.shields.io/discord/871555550444408883
[github-sponsors]: https://github.com/sponsors/mandarons
[github-sponsors-badge]: https://img.shields.io/github/sponsors/mandarons
