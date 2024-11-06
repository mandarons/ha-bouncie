"""Tests for sensor.py."""
from datetime import timedelta

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
import homeassistant.util.dt as date_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from . import const, setup_platform


async def test_car_info_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
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


async def test_car_odometer_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_odometer")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_odometer")
    assert state.state == "120508"


async def test_car_address_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_address")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_address")
    assert (
        state.state == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["location"]["address"]
    )


async def test_car_fuel_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_fuel")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_fuel")
    assert state.state == "29"


async def test_car_speed_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_speed")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_speed")
    assert state.state == str(int(const.MOCK_VEHICLES_RESPONSE[0]["stats"]["speed"]))


async def test_car_mil_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_mil")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_mil")
    assert state.state == str(const.MOCK_VEHICLES_RESPONSE[0]["stats"]["mil"]["milOn"])


async def test_car_battery_sensor(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test getting all vehicles."""
    await setup_platform(hass, SENSOR_DOMAIN)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_battery")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_battery")
    assert (
        state.state
        == const.MOCK_VEHICLES_RESPONSE[0]["stats"]["mil"]["battery"]["status"]
    )


async def test_sensor_update(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test sensor auto-update."""
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


async def test_battery_info_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["stats"]["mil"]["battery"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_battery")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_battery")
    assert state.state == "Not available"


async def test_stats_mil_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["stats"]["mil"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_mil")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_mil")
    assert state.state == "Not available"


async def test_stats_location_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["stats"]["location"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_address")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_address")
    assert state.state == "Not available"


async def test_stats_fuel_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["stats"]["fuelLevel"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.my_prius_car_fuel")
    assert entry is not None
    state = hass.states.get("sensor.my_prius_car_fuel")
    assert state.state == "-1"


async def test_nickname_missing(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test battery info missing from bouncie server."""
    updated_response = list(const.MOCK_VEHICLES_RESPONSE)
    del updated_response[0]["nickName"]
    await setup_platform(hass, SENSOR_DOMAIN, updated_response)
    entity_registry = er.async_get(hass)
    entry = entity_registry.async_get("sensor.2007_toyota_prius_car_info")
    assert entry is not None
    entry = entity_registry.async_get("sensor.my_prious_car_info")
    assert entry is None
