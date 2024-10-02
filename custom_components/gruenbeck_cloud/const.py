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

# Custom Unit of Measurement
UNIT_OF_DH: Final = "°dH"
UNIT_OF_MA_MIN: Final = "mAmin"
UNIT_OF_L_IMP: Final = "l/Imp"
UNIT_OF_M3_X_DH: Final = "m³x°dH"
UNIT_OF_L_HOUR: Final = "l/h"

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
