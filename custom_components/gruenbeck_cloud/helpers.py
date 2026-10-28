"""Helpers for the Grünbeck Cloud integration."""
from __future__ import annotations

from datetime import date, timedelta

from pygruenbeck_cloud.models import DailyUsageEntry, Device, DeviceError

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


def daily_usage_value(
    entries: list[DailyUsageEntry] | None,
    *,
    days_ago: int,
    today: date | None = None,
) -> int | None:
    """Return usage value for a day relative to today."""
    if not entries:
        return None

    target = (today or date.today()) - timedelta(days=days_ago)
    for entry in entries:
        if entry.date == target:
            return entry.value
    return None
