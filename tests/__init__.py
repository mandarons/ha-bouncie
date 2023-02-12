"""Tests for bouncie integration."""
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.bouncie.const import STORAGE_KEY, STORAGE_VERSION
from custom_components.bouncie.coordinator import AsyncRESTAPIClient
from custom_components.bouncie.usage import BouncieStore

from . import const


def setup_mock_controller(mock_controller, mock_vehicles_response):
    """Set up mock controller with mock data."""
    instance = mock_controller.return_value
    instance.get_access_token.return_value = True
    instance.get_all_vehicles.return_value = (
        mock_vehicles_response or const.MOCK_VEHICLES_RESPONSE
    )


async def setup_platform(
    hass: HomeAssistant,
    platform: str,
    mock_vehicles_response=None,
) -> MockConfigEntry:
    """Set up Bouncie platform."""
    mock_entry = MockConfigEntry(
        domain=const.DOMAIN, title="Bouncie", data=const.MOCK_CONFIG_ENTRY, options=None
    )
    mock_entry.add_to_hass(hass)

    with patch("custom_components.bouncie.PLATFORMS", [platform]), patch(
        "custom_components.bouncie.coordinator.AsyncRESTAPIClient",
        spec=AsyncRESTAPIClient,
    ) as mock_controller:
        setup_mock_controller(mock_controller, mock_vehicles_response)
        assert await async_setup_component(hass, const.DOMAIN, {})
    await hass.async_block_till_done()

    return mock_entry, mock_controller


def clean_up_bouncie_store(hass: HomeAssistant):
    """Remove Bouncie store."""
    store = BouncieStore(hass=hass, version=STORAGE_VERSION, key=STORAGE_KEY)
    store.remove()
