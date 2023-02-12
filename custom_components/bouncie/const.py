"""Constants for the bouncie integration."""

from datetime import timedelta
import json
import logging
import os

DOMAIN = "bouncie"
USAGE_DOMAIN = "bouncie-usage"
LOGGER = logging.getLogger(__name__)

CONF_REDIRECT_URI = "redirect_uri"
CONF_CODE = "code"

VEHICLE_MODEL_KEY = "model"
VEHICLE_MAKE_KEY = "make"
VEHICLE_NAME_KEY = "name"
VEHICLE_YEAR_KEY = "year"
VEHICLE_STANDARD_ENGINE_KEY = "standardEngine"
VEHICLE_VIN_KEY = "vin"
VEHICLE_IMEI_KEY = "imei"
VEHICLE_STATS_KEY = "stats"
VEHICLE_LOCAL_TIMEZONE_KEY = "localTimeZone"
VEHICLE_LAST_UPDATED_KEY = "lastUpdated"
VEHICLE_ODOMETER_KEY = "odometer"
VEHICLE_LOCATION_KEY = "location"
VEHICLE_LATITUDE_KEY = "lat"
VEHICLE_LONGITUDE_KEY = "lon"
VEHICLE_HEADING_KEY = "heading"
VEHICLE_ADDRESS_KEY = "address"
VEHICLE_IS_RUNNING_KEY = "isRunning"
VEHICLE_SPEED_KEY = "speed"
VEHICLE_MIL_KEY = "mil"
VEHICLE_MIL_LAST_UPDATED_KEY = "lastUpdated"
VEHICLE_BATTERY_KEY = "battery"
VEHICLE_BATTERY_STATUS_KEY = "status"
VEHICLE_BATTERY_LAST_UPDATED_KEY = "lastUpdated"
VEHICLE_NICKNAME_KEY = "nickName"

ATTR_VEHICLE_MODEL_MAKE_KEY = "model_make"
ATTR_VEHICLE_MODEL_NAME_KEY = "model_name"
ATTR_VEHICLE_MODEL_YEAR_KEY = "model_year"
ATTR_VEHICLE_NICKNAME_KEY = "nickname"
ATTR_VEHICLE_STANDARD_ENGINE_KEY = "standardengine"
ATTR_VEHICLE_VIN_KEY = "vin"
ATTR_VEHICLE_IMEI_KEY = "imei"

ATTR_VEHICLE_STATS_LAST_UPDATED_KEY = "stats_last_updated"
ATTR_VEHICLE_STATS_ODOMETER_KEY = "stats_odometer"
ATTR_VEHICLE_STATS_LOCATION_LAT_KEY = "stats_location_lat"
ATTR_VEHICLE_STATS_LOCATION_LON_KEY = "stats_location_lon"
ATTR_VEHICLE_STATS_LOCATION_HEADING_KEY = "stats_location_heading"
ATTR_VEHICLE_STATS_LOCATION_ADDRESS_KEY = "stats_location_address"

ATTR_VEHICLE_FUEL_LEVEL_KEY = "fuellevel"
ATTR_VEHICLE_SPEED_KEY = "speed"

ATTR_VEHICLE_MIL_KEY = "mil"
ATTR_VEHICLE_MIL_LAST_UPDATED_KEY = "mil_lastupdated"

ATTR_VEHICLE_BATTERY_STATUS_KEY = "battery_status"
ATTR_VEHICLE_BATTERY_LAST_UPDATED_KEY = "battery_lastupdated"

NEW_INSTALLATION_ENDPOINT = "https://wapar-api.mandarons.com/api/installation"
NEW_HEARTBEAT_ENDPOINT = "https://wapar-api.mandarons.com/api/heartbeat"
with open(
    os.path.join(os.path.dirname(__file__), "manifest.json"), encoding="utf-8"
) as f:
    MANIFEST_DATA = json.load(f)
APP_VERSION = MANIFEST_DATA["version"]
APP_NAME = "ha-bouncie"
STORAGE_VERSION = 1
STORAGE_KEY = "core.ha-bouncie"
HEARTBEAT_INTERVAL = timedelta(days=1)
