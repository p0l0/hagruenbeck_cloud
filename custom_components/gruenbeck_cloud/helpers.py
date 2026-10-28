"""Helpers for the Grünbeck Cloud integration."""
from __future__ import annotations

from pygruenbeck_cloud.models import Device, DeviceError

from .const import ERROR_CODE_SALT_SUPPLY_LOW


def unresolved_errors(device: Device) -> list[DeviceError]:
    """Return unresolved device errors/warnings."""
    if not device.errors:
        return []
    return [error for error in device.errors if not error.is_resolved]


def has_unresolved_warning(device: Device) -> bool:
    """Return True if an unresolved warning exists."""
    return any(error.type == "warning" for error in unresolved_errors(device))


def has_salt_supply_low(device: Device) -> bool:
    """Return True if salt supply is reported low."""
    return any(
        error.error_code == ERROR_CODE_SALT_SUPPLY_LOW
        for error in unresolved_errors(device)
    )


def alert_key(error: DeviceError) -> tuple[int, str, str]:
    """Stable key for a device alert."""
    return (error.error_code, error.date.isoformat(), error.message)
