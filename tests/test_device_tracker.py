"""Tests for device_tracker.py."""
from datetime import timedelta
import uuid

from homeassistant.components.device_tracker import DOMAIN as DEVICE_TRACKER_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import homeassistant.util.dt as date_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.bouncie.const import (
    NEW_HEARTBEAT_ENDPOINT,
    NEW_INSTALLATION_ENDPOINT,
)

from . import clean_up_bouncie_store, const, setup_platform


async def test_device_tracker(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
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
    clean_up_bouncie_store(hass=hass)


async def test_device_tracker_update(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting updated value."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
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
    clean_up_bouncie_store(hass=hass)
