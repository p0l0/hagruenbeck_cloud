"""Platform for Grünbeck Cloud binary sensor."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import logging
from typing import Any

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .helpers import has_salt_supply_low, has_unresolved_warning, unresolved_errors
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class GruenbeckCloudEntityDescription(BinarySensorEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    extra_attr_fn: Callable[[Device], Mapping[str, Any] | None] = lambda _: None
    value_fn: Callable[[Device], bool | None]


BINARY_SENSORS: tuple[GruenbeckCloudEntityDescription, ...] = (
    GruenbeckCloudEntityDescription(
        key="has_error",
        translation_key="has_error",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda device: device.has_error,
        extra_attr_fn=lambda device: {
            "errors": [error.to_dict() for error in device.errors]  # type: ignore[union-attr]  # noqa: E501
            if device.errors is not None
            else []
        },
    ),
    GruenbeckCloudEntityDescription(
        key="has_warning",
        translation_key="has_warning",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=has_unresolved_warning,
        extra_attr_fn=lambda device: {
            "warnings": [
                error.to_dict()
                for error in unresolved_errors(device)
                if error.type == "warning"
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="salt_supply_low",
        translation_key="salt_supply_low",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=has_salt_supply_low,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities(
        GruenbeckCloudBinarySensorEntity(coordinator, description)
        for description in BINARY_SENSORS
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudBinarySensorEntity(GruenbeckCloudEntity, BinarySensorEntity):
    """Define a Grünbeck Cloud Binary Sensor."""

    entity_description: GruenbeckCloudEntityDescription

    def __init__(
        self,
        coordinator: GruenbeckCloudCoordinator,
        description: GruenbeckCloudEntityDescription,
    ) -> None:
        """Initialize our Grünbeck Sensor entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.serial_number}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return the state of our sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.entity_description.extra_attr_fn(self.coordinator.data)
