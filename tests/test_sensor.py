"""Tests for sensor.py."""
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers import entity_registry as er
from . import setup_platform
from . import const
from bounciepy.exceptions import BouncieException


async def test_car_info_sensor(hass: HomeAssistant) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_info")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_info")
    assert state.state == "Not Running"
    assert (
        state.attributes["standardengine"]
        == const.MOCK_VEHICLES_RESPONSE[0]["standardEngine"]
    )
    assert state.attributes["vin"] == const.MOCK_VEHICLES_RESPONSE[0]["vin"]
    assert state.attributes["imei"] == const.MOCK_VEHICLES_RESPONSE[0]["imei"]


async def test_car_info_sensor_update_failed(
    hass: HomeAssistant, error_on_get_data
) -> None:
    """Test error on data update."""
    mock_entry, mock_controller = await setup_platform(hass, SENSOR_DOMAIN)
    mock_controller.return_value.get_all_vehicles.side_effect = BouncieException(
        "fetch error"
    )
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_info")
    assert entry is not None
