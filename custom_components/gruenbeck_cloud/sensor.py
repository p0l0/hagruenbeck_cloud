"""Platform for Grünbeck Cloud sensor."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
import logging

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfMass, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DEVICE_CLASS_DAYS, DEVICE_CLASS_DH, DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


# @dataclass(frozen=True, kw_only=True)
@dataclass(kw_only=True)
class GruenbeckCloudEntityDescription(SensorEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], datetime | StateType]


SENSORS: tuple[GruenbeckCloudEntityDescription, ...] = (
    GruenbeckCloudEntityDescription(
        key="next_regeneration",
        translation_key="next_regeneration",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.next_regeneration,
    ),
    GruenbeckCloudEntityDescription(
        key="startup",
        translation_key="startup",
        device_class=SensorDeviceClass.DATE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.startup,
    ),
    GruenbeckCloudEntityDescription(
        key="last_service",
        translation_key="last_service",
        device_class=SensorDeviceClass.DATE,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.last_service,
    ),
    GruenbeckCloudEntityDescription(
        key="raw_water",
        translation_key="raw_water",
        native_unit_of_measurement=DEVICE_CLASS_DH,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.raw_water,
    ),
    GruenbeckCloudEntityDescription(
        key="soft_water",
        translation_key="soft_water",
        native_unit_of_measurement=DEVICE_CLASS_DH,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.soft_water,
    ),
    GruenbeckCloudEntityDescription(
        key="soft_water_quantity",
        translation_key="soft_water_quantity",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.soft_water_quantity,
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_counter",
        translation_key="regeneration_counter",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.regeneration_counter,
    ),
    GruenbeckCloudEntityDescription(
        key="current_flow_rate",
        translation_key="current_flow_rate",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.current_flow_rate,
    ),
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_volume",
        translation_key="remaining_capacity_volume",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.remaining_capacity_volume,
    ),
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_percentage",
        translation_key="remaining_capacity_percentage",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda device: device.remaining_capacity_percentage,
    ),
    GruenbeckCloudEntityDescription(
        key="salt_range",
        translation_key="salt_range",
        native_unit_of_measurement=DEVICE_CLASS_DAYS,
        value_fn=lambda device: device.salt_range,
    ),
    GruenbeckCloudEntityDescription(
        key="salt_consumption",
        translation_key="salt_consumption",
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        device_class=SensorDeviceClass.WEIGHT,
        # TOTAL_INCREASING and WEIGHT is not possible
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.salt_consumption,
    ),
    GruenbeckCloudEntityDescription(
        key="next_service",
        translation_key="next_service",
        native_unit_of_measurement=DEVICE_CLASS_DAYS,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.next_service,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities(
        GruenbeckCloudSensorEntity(coordinator, description)
        for description in SENSORS
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudSensorEntity(GruenbeckCloudEntity, SensorEntity):
    """Define a Grünbeck Cloud Sensor."""

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
    def native_value(self) -> StateType | date | datetime | Decimal:
        """Return the state of our sensor."""
        return self.entity_description.value_fn(self.coordinator.data)
