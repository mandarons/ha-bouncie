"""Tests for usage module."""
from datetime import timedelta
from unittest.mock import patch
import uuid

from homeassistant import config_entries
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers.json import JSONEncoder
import homeassistant.util.dt as date_util
from pytest_homeassistant_custom_component.common import async_fire_time_changed
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.bouncie.const import (
    APP_VERSION,
    DOMAIN,
    HEARTBEAT_INTERVAL,
    NEW_HEARTBEAT_ENDPOINT,
    NEW_INSTALLATION_ENDPOINT,
    STORAGE_KEY,
    STORAGE_VERSION,
)
from custom_components.bouncie.usage import BouncieStore, UsageData

from . import clean_up_bouncie_store, setup_platform


async def test_usage_heartbeat(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test heartbeat."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None
    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=True,
    ), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
                "scan_interval": 10,
            },
        )
        await hass.async_block_till_done()
    await setup_platform(hass, SENSOR_DOMAIN)

    async_fire_time_changed(hass, date_util.now() + HEARTBEAT_INTERVAL)
    await hass.async_block_till_done()
    assert len(aioclient_mock.mock_calls) == 2
    assert str(aioclient_mock.mock_calls[1][1]).endswith("heartbeat")
    clean_up_bouncie_store(hass=hass)


async def test_usage_heartbeat_none_before_heartbeat_interval(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test heartbeat before heartbeat interval."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None
    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=True,
    ), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
                "scan_interval": 10,
            },
        )
        await hass.async_block_till_done()
    await setup_platform(hass, SENSOR_DOMAIN)

    async_fire_time_changed(hass, date_util.now() + timedelta(seconds=10))
    await hass.async_block_till_done()
    assert len(aioclient_mock.mock_calls) == 1
    assert str(aioclient_mock.mock_calls[0][1]).endswith("installation")
    clean_up_bouncie_store(hass=hass)


async def test_install_upgrade(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test install upgrade."""

    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    store = BouncieStore(
        hass=hass,
        version=STORAGE_VERSION,
        key=STORAGE_KEY,
        encoder=JSONEncoder,
        atomic_writes=True,
    )
    store.save(data=UsageData(installation_id=uuid.uuid4(), app_version=APP_VERSION))
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None
    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=True,
    ), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
                "scan_interval": 10,
            },
        )
        await hass.async_block_till_done()
    await setup_platform(hass, SENSOR_DOMAIN)

    assert len(aioclient_mock.mock_calls) == 1
    assert str(aioclient_mock.mock_calls[0][1]).endswith("installation")
    assert "previousId" in aioclient_mock.mock_calls[0][2]
    assert aioclient_mock.mock_calls[0][2]["previousId"]
    clean_up_bouncie_store(hass=hass)


async def test_usage_install_response_error(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test heartbeat."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=400, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(
        NEW_HEARTBEAT_ENDPOINT, status=201, json={"message": "All good."}
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None
    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=True,
    ), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
                "scan_interval": 10,
            },
        )
        await hass.async_block_till_done()
    await setup_platform(hass, SENSOR_DOMAIN)

    assert len(aioclient_mock.mock_calls) == 1
    clean_up_bouncie_store(hass=hass)


async def test_usage_heartbeat_response_status_error(
    hass: HomeAssistant, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test heartbeat."""
    aioclient_mock.post(
        NEW_INSTALLATION_ENDPOINT, status=201, json={"id": str(uuid.uuid4())}
    )
    aioclient_mock.post(NEW_HEARTBEAT_ENDPOINT, status=400, json={"error": "Not good."})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] is None
    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=True,
    ), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):

        await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
                "scan_interval": 10,
            },
        )
        await hass.async_block_till_done()
    await setup_platform(hass, SENSOR_DOMAIN)

    async_fire_time_changed(hass, date_util.now() + HEARTBEAT_INTERVAL)
    await hass.async_block_till_done()
    assert len(aioclient_mock.mock_calls) == 2
    assert str(aioclient_mock.mock_calls[1][1]).endswith("heartbeat")
    clean_up_bouncie_store(hass=hass)
