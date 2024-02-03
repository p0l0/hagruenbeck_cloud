"""Services for Grünbeck Cloud integration."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, SupportsResponse, callback

from .const import (
    DOMAIN,
    SERVICE_GET_SALT_MEASUREMENTS,
    SERVICE_GET_WATER_MEASUREMENTS,
    SERVICE_REGENERATE,
    SERVICE_UPDATE_DEVICE_PARAMETERS,
    SERVICE_UPDATE_DEVICE_PARAMETERS_SCHEMA,
)
from .coordinator import GruenbeckCloudCoordinator


@callback
def register_services(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
) -> None:
    """Register integration services."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_DEVICE_PARAMETERS,
        coordinator.service_change_settings,
        schema=SERVICE_UPDATE_DEVICE_PARAMETERS_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REGENERATE,
        coordinator.service_regenerate,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_SALT_MEASUREMENTS,
        coordinator.service_get_device_salt_measurements,
        supports_response=SupportsResponse.ONLY,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_WATER_MEASUREMENTS,
        coordinator.service_get_device_water_measurements,
        supports_response=SupportsResponse.ONLY,
    )
