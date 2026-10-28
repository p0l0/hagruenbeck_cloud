"""Services for Grünbeck Cloud integration."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse, callback

from .const import (
    DOMAIN,
    SERVICE_GET_SALT_MEASUREMENTS,
    SERVICE_GET_WATER_MEASUREMENTS,
    SERVICE_REGENERATE,
    SERVICE_UPDATE_DEVICE_PARAMETERS,
    SERVICE_UPDATE_DEVICE_PARAMETERS_SCHEMA,
)
from .coordinator import GruenbeckCloudCoordinator

_SERVICES_FLAG = f"{DOMAIN}_services_registered"

ALL_SERVICES = (
    SERVICE_UPDATE_DEVICE_PARAMETERS,
    SERVICE_REGENERATE,
    SERVICE_GET_SALT_MEASUREMENTS,
    SERVICE_GET_WATER_MEASUREMENTS,
)


def _get_coordinator(hass: HomeAssistant) -> GruenbeckCloudCoordinator:
    """Return a loaded coordinator (first config entry)."""
    entries = hass.data.get(DOMAIN, {})
    if not entries:
        msg = "Grünbeck Cloud is not loaded"
        raise ValueError(msg)
    return next(iter(entries.values()))


@callback
def register_services(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
) -> None:
    """Register integration services once for the domain."""
    if hass.data.get(_SERVICES_FLAG):
        return

    async def async_change_settings(call: ServiceCall) -> None:
        await _get_coordinator(hass).service_change_settings(call)

    async def async_regenerate(call: ServiceCall) -> None:
        await _get_coordinator(hass).service_regenerate(call)

    async def async_get_salt(call: ServiceCall) -> ServiceResponse:
        return await _get_coordinator(hass).service_get_device_salt_measurements(call)

    async def async_get_water(call: ServiceCall) -> ServiceResponse:
        return await _get_coordinator(hass).service_get_device_water_measurements(call)

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_DEVICE_PARAMETERS,
        async_change_settings,
        schema=SERVICE_UPDATE_DEVICE_PARAMETERS_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_REGENERATE,
        async_regenerate,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_SALT_MEASUREMENTS,
        async_get_salt,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_WATER_MEASUREMENTS,
        async_get_water,
        supports_response=SupportsResponse.ONLY,
    )
    hass.data[_SERVICES_FLAG] = True


@callback
def unregister_services(hass: HomeAssistant) -> None:
    """Remove services when no config entries remain loaded."""
    if hass.data.get(DOMAIN):
        return

    for service in ALL_SERVICES:
        if hass.services.has_service(DOMAIN, service):
            hass.services.async_remove(DOMAIN, service)

    hass.data.pop(_SERVICES_FLAG, None)
