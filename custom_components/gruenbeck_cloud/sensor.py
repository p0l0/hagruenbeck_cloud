"""Platform for Grünbeck Cloud sensor."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
import logging
from typing import Any

from pygruenbeck_cloud.const import PARAMETER_REGENERATION_STEP
from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfMass,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
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
    extra_attr_fn: Callable[[Device], Mapping[str, Any] | None] = lambda _: None
    value_fn: Callable[[Device], datetime | StateType]


#
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
    # Soft water exchanger 1 [l]
    GruenbeckCloudEntityDescription(
        key="soft_water_quantity",
        translation_key="soft_water_quantity",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.realtime.soft_water_quantity,
        extra_attr_fn=lambda device: {
            "daily_usage": [daily.to_dict() for daily in device.water]  # type: ignore[union-attr]  # noqa: E501
        },
    ),
    # Soft water exchanger 2 [l]
    GruenbeckCloudEntityDescription(
        key="soft_water_quantity_2",
        translation_key="soft_water_quantity_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda device: device.realtime.soft_water_quantity_2,
    ),
    # Regeneration counter
    GruenbeckCloudEntityDescription(
        key="regeneration_counter",
        translation_key="regeneration_counter",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.realtime.regeneration_counter,
    ),
    # Flow rate exchanger 1 [m³/h]
    GruenbeckCloudEntityDescription(
        key="current_flow_rate",
        translation_key="current_flow_rate",
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.current_flow_rate,
    ),
    # Flow rate exchanger 2 [m³/h]
    GruenbeckCloudEntityDescription(
        key="current_flow_rate_2",
        translation_key="current_flow_rate_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOU,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.current_flow_rate_2,
    ),
    # Soft water Exchanger 1 [m³]
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_volume",
        translation_key="remaining_capacity_volume",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.remaining_capacity_volume,
    ),
    # Soft water Exchanger 2 [m³]
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_volume_2",
        translation_key="remaining_capacity_volume_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.remaining_capacity_volume_2,
    ),
    # Residual capacity Exchanger 1 [%]
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_percentage",
        translation_key="remaining_capacity_percentage",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda device: device.realtime.remaining_capacity_percentage,
    ),
    # Residual capacity Exchanger 2 [%]
    GruenbeckCloudEntityDescription(
        key="remaining_capacity_percentage_2",
        translation_key="remaining_capacity_percentage_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda device: device.realtime.remaining_capacity_percentage_2,
    ),
    # Salt-reach [days]
    GruenbeckCloudEntityDescription(
        key="salt_range",
        translation_key="salt_range",
        native_unit_of_measurement=DEVICE_CLASS_DAYS,
        value_fn=lambda device: device.realtime.salt_range,
    ),
    # Salt consumption [kg]
    GruenbeckCloudEntityDescription(
        key="salt_consumption",
        translation_key="salt_consumption",
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        device_class=SensorDeviceClass.WEIGHT,
        # TOTAL_INCREASING and WEIGHT is not possible
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda device: device.realtime.salt_consumption,
        extra_attr_fn=lambda device: {
            "daily_usage": [daily.to_dict() for daily in device.salt]  # type: ignore[union-attr]  # noqa: E501
        },
    ),
    # Perform maintenance in [days]
    GruenbeckCloudEntityDescription(
        key="next_service",
        translation_key="next_service",
        native_unit_of_measurement=DEVICE_CLASS_DAYS,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.realtime.next_service,
    ),
    # Remaining amount / time of current regeneration step
    GruenbeckCloudEntityDescription(
        key="regeneration_remaining_time",
        translation_key="regeneration_remaining_time",
        value_fn=lambda device: device.realtime.regeneration_remaining_time,
    ),
    # Regeneration step
    GruenbeckCloudEntityDescription(
        key="regeneration_step",
        translation_key="regeneration_step",
        value_fn=lambda device: PARAMETER_REGENERATION_STEP[
            device.realtime.regeneration_step
        ]
        if device.realtime.regeneration_step in PARAMETER_REGENERATION_STEP
        else device.realtime.regeneration_step,
    ),
    # Make-up water volume [l]
    GruenbeckCloudEntityDescription(
        key="make_up_water_volume",
        translation_key="make_up_water_volume",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.make_up_water_volume,
    ),
    # Adsorber exhausted percentage [%]
    GruenbeckCloudEntityDescription(
        key="exhausted_percentage",
        translation_key="exhausted_percentage",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda device: device.realtime.exhausted_percentage,
    ),
    # Actual value soft water hardness [°dh]
    GruenbeckCloudEntityDescription(
        key="actual_value_soft_water_hardness",
        translation_key="actual_value_soft_water_hardness",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=DEVICE_CLASS_DH,
        value_fn=lambda device: device.realtime.actual_value_soft_water_hardness,
    ),
    # Capacity figure [m³x°dH]
    GruenbeckCloudEntityDescription(
        key="capacity_figure",
        translation_key="capacity_figure",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="m³x°dH",
        value_fn=lambda device: device.realtime.capacity_figure,
    ),
    # Flow rate peak value [m³/h]
    GruenbeckCloudEntityDescription(
        key="flow_rate_peak_value",
        translation_key="flow_rate_peak_value",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.flow_rate_peak_value,
    ),
    # Exchanger 1 peak value [m³/h]
    GruenbeckCloudEntityDescription(
        key="exchanger_peak_value",
        translation_key="exchanger_peak_value",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.exchanger_peak_value,
    ),
    # Exchanger 2 peak value [m³/h]
    GruenbeckCloudEntityDescription(
        key="exchanger_peak_value_2",
        translation_key="exchanger_peak_value_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.exchanger_peak_value_2,
    ),
    # Last regeneration Exchanger 1 [hh:mm]
    GruenbeckCloudEntityDescription(
        key="last_regeneration_exchanger",
        translation_key="last_regeneration_exchanger",
        entity_registry_enabled_default=False,
        value_fn=lambda device: str(device.realtime.last_regeneration_exchanger),
    ),
    # Last regeneration Exchanger 2 [hh:mm]
    GruenbeckCloudEntityDescription(
        key="last_regeneration_exchanger_2",
        translation_key="last_regeneration_exchanger_2",
        entity_registry_enabled_default=False,
        value_fn=lambda device: str(device.realtime.last_regeneration_exchanger_2),
    ),
    # Regeneration flow rate Exchanger 1 [l/h]
    GruenbeckCloudEntityDescription(
        key="regeneration_flow_rate_exchanger",
        translation_key="regeneration_flow_rate_exchanger",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="l/h",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.regeneration_flow_rate_exchanger,
    ),
    # Regeneration flow rate Exchanger 2 [l/h]
    GruenbeckCloudEntityDescription(
        key="regeneration_flow_rate_exchanger_2",
        translation_key="regeneration_flow_rate_exchanger_2",
        entity_registry_enabled_default=False,
        native_unit_of_measurement="l/h",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.regeneration_flow_rate_exchanger_2,
    ),
    # Blending flow rate [m³/h]
    GruenbeckCloudEntityDescription(
        key="blending_flow_rate",
        translation_key="blending_flow_rate",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        value_fn=lambda device: device.realtime.blending_flow_rate,
    ),
    # Step indication regeneration valve 1
    GruenbeckCloudEntityDescription(
        key="step_indication_regeneration_valve",
        translation_key="step_indication_regeneration_valve",
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.realtime.step_indication_regeneration_valve,
    ),
    # Step indication regeneration valve 2
    GruenbeckCloudEntityDescription(
        key="step_indication_regeneration_valve_2",
        translation_key="step_indication_regeneration_valve_2",
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.realtime.step_indication_regeneration_valve_2,
    ),
    # Current chlorine [mA]
    GruenbeckCloudEntityDescription(
        key="current_chlorine",
        translation_key="current_chlorine",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        device_class=SensorDeviceClass.CURRENT,
        value_fn=lambda device: device.realtime.current_chlorine,
    ),
    # Adsorber remaining amount of water [m³] - float?
    GruenbeckCloudEntityDescription(
        key="remaining_amount_of_water",
        translation_key="remaining_amount_of_water",
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.VOLUME,
        value_fn=lambda device: device.realtime.remaining_amount_of_water,
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

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.entity_description.extra_attr_fn(self.coordinator.data)
