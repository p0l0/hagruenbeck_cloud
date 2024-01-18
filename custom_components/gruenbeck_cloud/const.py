"""Constants for the Grünbeck Cloud integration."""
from datetime import timedelta

DOMAIN = "gruenbeck_cloud"
NAME = "Grünbeck Cloud"
COORDINATOR = "coordinator"
MANUFACTURER = "Grünbeck Wasseraufbereitung GmbH"

# Configuration parameter
CONF_DEVICE_ID = "device_id"

# Polling update interval
UPDATE_INTERVAL = timedelta(seconds=360)

# Custom Device classes
DEVICE_CLASS_DH = "°dH"
DEVICE_CLASS_DAYS = "days"  # @TODO - We need to translate this!
