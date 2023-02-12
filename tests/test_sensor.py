"""Tests for sensor.py."""
from datetime import timedelta
import uuid

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
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


async def test_car_info_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
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
    clean_up_bouncie_store(hass=hass)


async def test_car_odometer_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_odometer")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_odometer")
    assert state.state == "120508"
    clean_up_bouncie_store(hass=hass)


async def test_car_address_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_address")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_address")
    assert (
        state.state == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["address"]
    )
    clean_up_bouncie_store(hass=hass)


async def test_car_fuel_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_fuel")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_fuel")
    assert state.state == "29"
    clean_up_bouncie_store(hass=hass)


async def test_car_speed_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_speed")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_speed")
    assert state.state == str(int(const.MOCK_VEHICLES_RESPONSE[0]["stats"]["speed"]))
    clean_up_bouncie_store(hass=hass)


async def test_car_mil_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_mil")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_mil")
    assert state.state == str(const.MOCK_VEHICLES_RESPONSE[0]["stats"]["mil"]["milOn"])
    clean_up_bouncie_store(hass=hass)


async def test_car_battery_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_battery")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_battery")
    assert state.state == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["battery"]["status"]
    clean_up_bouncie_store(hass=hass)


async def test_sensor_update(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test sensor auto-update."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    _, mock_controller = await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_info")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_info")
    assert state.state == "Not Running"
    instance = mock_controller.return_value
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    updated_response[0]["stats"]["isRunning"] = True
    instance.get_all_vehicles.return_value = updated_response
    async_fire_time_changed(hass, date_util.now() + timedelta(seconds=10))
    await hass.async_block_till_done()
    state = hass.states.get("sensor.my_prius_car_info")
    assert state.state == "Running"
    clean_up_bouncie_store(hass=hass)


async def test_battery_info_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["stats"]["battery"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_battery")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_battery")
    assert state.state == "Not available"
    clean_up_bouncie_store(hass=hass)
