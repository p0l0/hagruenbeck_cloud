"""Diagnostics support for Grünbeck Cloud."""
from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any, TypeVar, cast

import attr

from homeassistant.components.diagnostics import REDACTED, async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import CONF_DEVICE_ID, DOMAIN
from .coordinator import GruenbeckCloudCoordinator

_T = TypeVar("_T")

TO_REDACT = {CONF_USERNAME, CONF_PASSWORD}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict[str, dict[str, Any]]:
    """Return diagnostics for a config entry."""

    def redact_serial_number(serial_number: str, data_dict: _T) -> _T:
        """Redact Serial Number in each entry."""
        replace = re.compile(re.escape(serial_number), re.IGNORECASE)
        if isinstance(data_dict, str):
            return cast(_T, replace.sub(REDACTED, data_dict))

        if not isinstance(data_dict, (Mapping, list)):
            return data_dict

        if isinstance(data_dict, list):
            return cast(
                _T, [redact_serial_number(serial_number, val) for val in data_dict]
            )

        redacted = {**data_dict}
        result = {}  # type: ignore[var-annotated]

        for key, value in redacted.items():
            if value is None:
                result[key] = value  # type: ignore[assignment]
                continue
            if isinstance(value, str) and not value:
                result[key] = value
                continue
            if isinstance(value, str):
                redacted[key] = replace.sub(REDACTED, value)
            elif isinstance(value, Mapping):
                redacted[key] = redact_serial_number(serial_number, value)
            elif isinstance(value, list):
                redacted[key] = [
                    redact_serial_number(serial_number, item) for item in value
                ]

            # Replace also serial number in key
            new_key = replace.sub(REDACTED, key)
            if new_key != key:
                result[new_key] = redacted[key]
            else:
                result[key] = redacted[key]

        return cast(_T, result)

    data = {"entry": async_redact_data(config_entry.as_dict(), TO_REDACT)}
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Get Diagnostics from API
    data["coordinator"] = await coordinator.api.get_diagnostics()  # type: ignore[assignment]

    # Gather information how device is represented in Home Assistant
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    hass_device = device_registry.async_get_device(
        identifiers={(DOMAIN, config_entry.data[CONF_DEVICE_ID])}
    )
    if not hass_device:
        return data

    data["device"] = {**attr.asdict(hass_device), "entities": {}}

    hass_entities = er.async_entries_for_device(
        entity_registry,
        device_id=hass_device.id,
        include_disabled_entities=True,
    )

    for entity_entry in hass_entities:
        state = hass.states.get(entity_entry.entity_id)
        state_dict = None
        if state:
            state_dict = dict(state.as_dict())
            # entity_id is already provided
            state_dict.pop("entity_id", None)
            # context doesn't provide useful information
            # state_dict.pop("context", None)

        data["device"]["entities"][entity_entry.entity_id] = {
            **attr.asdict(
                entity_entry, filter=lambda attr, value: attr.name != "entity_id"
            ),
            "state": state_dict,
        }

    if not isinstance(config_entry.unique_id, str):
        return data

    return redact_serial_number(config_entry.unique_id, data)
