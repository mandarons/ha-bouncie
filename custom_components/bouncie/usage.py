"""Usage module."""
from dataclasses import dataclass
from datetime import datetime
import os
from typing import Any

from aiohttp import ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.storage import Store
from homeassistant.util import json as json_util

from custom_components.bouncie.const import (
    APP_NAME,
    APP_VERSION,
    NEW_HEARTBEAT_ENDPOINT,
    NEW_INSTALLATION_ENDPOINT,
    STORAGE_KEY,
    STORAGE_VERSION,
)


@dataclass
class UsageData:
    """Usage data."""

    installation_id: str | None
    app_version: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Initialize analytics data from a dict."""
        return cls(
            data["installation_id"],
            data["app_version"],
        )


class BouncieStore(Store):
    """Bouncie local storage."""

    def load(self):
        """Load data."""
        data = json_util.load_json(self.path)
        return None if data == {} else data

    def save(self, data):
        """Save data."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        json_util.save_json(
            self.path,
            data,
            self._private,
            encoder=self._encoder,
            atomic_writes=self._atomic_writes,
        )

    def remove(self):
        """Remove storage."""
        if os.path.exists(self.path):
            os.unlink(self.path)


class Usage:
    """Usage class."""

    def __init__(self, hass: HomeAssistant, session: ClientSession) -> None:
        """Initialize Usage instance."""
        self._hass = hass
        self._data = UsageData(installation_id=None, app_version=APP_VERSION)
        self._session = session
        self._store = BouncieStore(
            hass=hass,
            version=STORAGE_VERSION,
            key=STORAGE_KEY,
            encoder=JSONEncoder,
            atomic_writes=True,
        )

    def load(self):
        """Load data from storage."""
        stored = self._store.load()
        if stored:
            self._data = UsageData.from_dict(stored)

    def save(self):
        """Save data to storage."""
        return self._store.save(data=self._data)

    async def install(self):
        """Record app installation or upgrade."""
        post_data = {"appName": APP_NAME, "appVersion": APP_VERSION}
        self.load()
        if self._data.installation_id:
            post_data["previousId"] = self._data.installation_id
        response = await self._session.post(
            url=NEW_INSTALLATION_ENDPOINT,
            data=post_data,
        )
        if response.status in (200, 201):
            response_data = await response.json()
            if "id" in response_data:
                self._data.installation_id = response_data["id"]
                self.save()
                return True
        return False

    async def heartbeat(self, _: datetime | None = None):
        """Record app heartbeat."""
        self.load()
        post_data = {"installationId": self._data.installation_id, "data": None}
        async with self._session.post(
            url=NEW_HEARTBEAT_ENDPOINT, data=post_data
        ) as response:
            if response.status in (200, 201):
                return True
        return False
