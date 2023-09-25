"""Support for Bouncie device tracker."""

from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import BouncieDataUpdateCoordinator, const

ATTRIBUTION = "Data provided by Bouncie"


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Bouncie vehicle trackers by config_entry."""
    coordinator = hass.data[const.DOMAIN][config_entry.entry_id]
    async_add_entities(
        [
            BouncieVehicleTracker(coordinator, vehicle_info)
            for vehicle_info in coordinator.data["vehicles"]
        ],
        True,
    )


class BouncieVehicleTracker(
    CoordinatorEntity[BouncieDataUpdateCoordinator], TrackerEntity
):
    """Representation of a Tesla car location device tracker."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: BouncieDataUpdateCoordinator,
        vehicle_info: dict,
    ) -> None:
        """Initialize car location entity."""
        self._vehicle_info = vehicle_info
        self._attr_has_entity_name = True
        self._attr_name = None
        self._attr_unique_id = slugify(f'{self._vehicle_info["nickName"]} tracker')
        self._attr_device_info = DeviceInfo(
            identifiers={(const.DOMAIN, self._vehicle_info["vin"])},
            manufacturer=self._vehicle_info[const.VEHICLE_MODEL_KEY]["make"],
            model=self._vehicle_info[const.VEHICLE_MODEL_KEY]["name"],
            name=self._vehicle_info["nickName"],
            hw_version=self._vehicle_info[const.VEHICLE_MODEL_KEY]["year"],
        )
        super().__init__(coordinator)

    @property
    def source_type(self):
        """Return device tracker source type."""
        return SOURCE_TYPE_GPS

    @property
    def longitude(self):
        """Return longitude."""
        return self._vehicle_info["stats"]["location"]["lon"]

    @property
    def latitude(self):
        """Return latitude."""
        return self._vehicle_info["stats"]["location"]["lat"]

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "heading": self._vehicle_info["stats"]["location"]["heading"],
            "speed": self._vehicle_info["stats"]["speed"],
        }

    @property
    def force_update(self):
        """Disable forced updated since we are polling via the coordinator updates."""
        return False

    @callback
    def _handle_coordinator_update(self) -> None:
        self._vehicle_info = [
            vehicle
            for vehicle in self.coordinator.data["vehicles"]
            if vehicle["vin"] == self._vehicle_info["vin"]
        ][0] or self._vehicle_info
        self.async_write_ha_state()
        return super()._handle_coordinator_update()
