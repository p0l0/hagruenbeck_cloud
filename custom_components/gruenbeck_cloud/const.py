"""Constants for the Grünbeck Cloud integration."""
from datetime import timedelta
from typing import Final

import voluptuous as vol

DOMAIN: Final = "gruenbeck_cloud"
NAME: Final = "Grünbeck Cloud"
COORDINATOR: Final = "coordinator"
MANUFACTURER: Final = "Grünbeck Wasseraufbereitung GmbH"

# Configuration parameter
CONF_DEVICE_ID: Final = "device_id"

# Polling update interval
UPDATE_INTERVAL: Final = timedelta(seconds=360)

# Custom Device classes
DEVICE_CLASS_DH: Final = "°dH"
DEVICE_CLASS_DAYS: Final = "days"  # @TODO - We need to translate this!

# Services
SERVICE_UPDATE_DEVICE_PARAMETERS: Final = "change_settings"
SERVICE_PARAM_PARAMETER: Final = "parameter"
SERVICE_PARAM_VALUE: Final = "value"
SERVICE_UPDATE_DEVICE_PARAMETERS_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_PARAM_PARAMETER): str,
        vol.Required(SERVICE_PARAM_VALUE): vol.Any(str, int),
    }
)
SERVICE_GET_SALT_MEASUREMENTS: Final = "get_device_salt_measurements"
SERVICE_GET_WATER_MEASUREMENTS: Final = "get_device_water_measurements"
SERVICE_REGENERATE: Final = "regenerate"
