"""Tests for device_tracker.py."""
from copy import deepcopy
from datetime import timedelta

from homeassistant.components.device_tracker import DOMAIN as DEVICE_TRACKER_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import homeassistant.util.dt as date_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from . import const, setup_platform


async def test_device_tracker(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, DEVICE_TRACKER_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("device_tracker.my_prius")
    assert entry is not None
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["source_type"] == "gps"
    assert (
        state.attributes["latitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lat"]
    )
    assert (
        state.attributes["longitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lon"]
    )
    assert (
        state.attributes["heading"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["heading"]
    )


async def test_device_tracker_update(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting updated value."""
    _, mock_controller = await setup_platform(hass, DEVICE_TRACKER_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("device_tracker.my_prius")
    assert entry is not None
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["source_type"] == "gps"
    assert (
        state.attributes["latitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lat"]
    )
    assert (
        state.attributes["longitude"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["lon"]
    )
    assert (
        state.attributes["heading"]
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["heading"]
    )
    instance = mock_controller.return_value
    updated_response = const.MOCK_VEHICLES_RESPONSE
    updated_response[0]["stats"]["location"]["heading"] = 235
    instance.get_all_vehicles.return_value = updated_response
    async_fire_time_changed(hass, date_util.now() + timedelta(seconds=10))
    await hass.async_block_till_done()
    state = hass.states.get("device_tracker.my_prius")
    assert state.state == "not_home"
    assert state.attributes["heading"] == 235


async def test_device_tracker_without_nickname(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test tracker setup when vehicle nickname is missing."""
    vehicles_response = deepcopy(const.MOCK_VEHICLES_RESPONSE)
    vehicles_response[0].pop("nickName")

    await setup_platform(hass, DEVICE_TRACKER_DOMAIN, vehicles_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("device_tracker.toyota_prius_2007_vin")

    assert entry is not None
    assert entry.unique_id == "toyota_prius_2007_vin_tracker"
    state = hass.states.get("device_tracker.toyota_prius_2007_vin")
    assert state is not None
