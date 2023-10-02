"""The bouncie integration."""
from __future__ import annotations

import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL, Platform
from homeassistant.core import Config, HomeAssistant

from .const import DOMAIN, LOGGER, VEHICLE_MODEL_KEY
from .coordinator import BouncieDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.DEVICE_TRACKER]


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up bouncie from a config entry."""

    coordinator = BouncieDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        config_entry=entry,
        update_interval=datetime.timedelta(seconds=entry.data[CONF_SCAN_INTERVAL]),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def patch_missing_data(vehicle_info):
    """Fill in missing data."""
    if "battery" not in vehicle_info["stats"]:
        vehicle_info["stats"]["battery"] = {
            "status": "Not available",
            "lastUpdated": "Not available",
        }
    if "mil" not in vehicle_info["stats"]:
        vehicle_info["stats"]["mil"] = {
            "milOn": "Not available",
            "lastUpdated": "Not available",
        }
    if "location" not in vehicle_info["stats"]:
        vehicle_info["stats"]["location"] = {
            "address": "Not available",
        }
    if "fuelLevel" not in vehicle_info["stats"]:
        vehicle_info["stats"]["fuelLevel"] = -1
    if "nickName" not in vehicle_info:
        vehicle_info["nickName"] = (
            str(vehicle_info[VEHICLE_MODEL_KEY]["year"])
            + " "
            + str(vehicle_info[VEHICLE_MODEL_KEY]["make"])
            + " "
            + str(vehicle_info[VEHICLE_MODEL_KEY]["name"])
        )
    return vehicle_info
