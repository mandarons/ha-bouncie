"""Support for Bouncie device tracker."""

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant
from homeassistant.util import slugify
from homeassistant.helpers.entity import DeviceInfo

from . import const

ATTRIBUTION = "Data provided by Bouncie"


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Bouncie vehicle trackers by config_entry."""
    coordinator = hass.data[const.DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            BouncieVehicleTracker(vehicle_info)
            for vehicle_info in coordinator.data["vehicles"]
        ]
    )


class BouncieVehicleTracker(TrackerEntity):
    """Representation of a Tesla car location device tracker."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        vehicle_info: dict,
    ) -> None:
        """Initialize car location entity."""
        self._vehicle_info = vehicle_info
        self._fuel_level = vehicle_info["stats"]["fuelLevel"]
        self._latitude = vehicle_info["stats"]["location"]["lat"]
        self._longitude = vehicle_info["stats"]["location"]["lon"]
        self._heading = vehicle_info["stats"]["location"]["heading"]
        self._name = vehicle_info["stats"]["location"]["address"]
        self._speed = vehicle_info["stats"]["speed"]
        self._attr_has_entity_name = True
        self._attr_unique_id = slugify(f'{self._vehicle_info["nickName"]} tracker')
        self._attr_device_info = DeviceInfo(
            identifiers={(const.DOMAIN, self._vehicle_info["vin"])},
            manufacturer=self._vehicle_info[const.VEHICLE_MODEL_KEY]["make"],
            model=self._vehicle_info[const.VEHICLE_MODEL_KEY]["name"],
            name=self._vehicle_info["nickName"],
            hw_version=self._vehicle_info[const.VEHICLE_MODEL_KEY]["year"],
        )

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude."""
        return self._longitude

    @property
    def latitude(self):
        """Return latitude."""
        return self._latitude

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "heading": self._heading,
            "speed": self._speed,
        }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False
