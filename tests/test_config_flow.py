"""Test the bouncie config flow."""
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
import pytest

from custom_components.bouncie.config_flow import InvalidAuth
from custom_components.bouncie.const import DOMAIN


@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch("custom_components.bouncie.async_setup", return_value=True,), patch(
        "custom_components.bouncie.async_setup_entry",
        return_value=True,
    ):
        yield


async def test_form(hass, aioclient_mock) -> None:
    """Test we get the form."""

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
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
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

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"].lower() == DOMAIN
    print(result2["data"])
    assert result2["data"] == {
        "client_id": "mock_client_id",
        "client_secret": "mock_client_secret",
        "code": "mock_authorization_code",
        "redirect_uri": "http://mock-redirect-url",
        "scan_interval": 10,
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        side_effect=InvalidAuth,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_auth_failed(hass: HomeAssistant) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        return_value=False,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_bouncie_exception(hass: HomeAssistant) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "bounciepy.async_rest_api_client.AsyncRESTAPIClient.get_access_token",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "client_id": "mock_client_id",
                "client_secret": "mock_client_secret",
                "code": "mock_authorization_code",
                "redirect_uri": "http://mock-redirect-url",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}
