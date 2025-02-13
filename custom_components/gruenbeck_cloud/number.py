"""Platform for Grünbeck Cloud number entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfFrequency,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, UNIT_OF_DH, UNIT_OF_L_IMP, UNIT_OF_M3_X_DH, UNIT_OF_MA_MIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class GruenbeckCloudEntityDescription(NumberEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], float | None]
    update_fn: Callable[[Device, float], dict[str, float] | None] = (
        lambda device, value: None
    )


NUMBERS: tuple[GruenbeckCloudEntityDescription, ...] = (
    # Water settings
    GruenbeckCloudEntityDescription(
        key="raw_water_hardness",
        translation_key="raw_water_hardness",
        entity_category=EntityCategory.CONFIG,
        mode=NumberMode.BOX,
        native_unit_of_measurement=UNIT_OF_DH,
        value_fn=lambda device: device.parameters.raw_water_hardness,
        update_fn=lambda device, value: {"raw_water_hardness": value},
    ),
    GruenbeckCloudEntityDescription(
        key="soft_water_hardness",
        translation_key="soft_water_hardness",
        entity_category=EntityCategory.CONFIG,
        mode=NumberMode.BOX,
        native_unit_of_measurement=UNIT_OF_DH,
        value_fn=lambda device: device.parameters.soft_water_hardness,
        update_fn=lambda device, value: {"soft_water_hardness": value},
    ),
    #################################################################
    #                                                               #
    # Disabled Entities - Need to be activated manually in Frontend #
    #                                                               #
    #################################################################
    # Maintenance information [days]
    GruenbeckCloudEntityDescription(
        key="maintenance_interval",
        translation_key="maintenance_interval",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        mode=NumberMode.SLIDER,
        native_min_value=1,
        native_max_value=365,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.DAYS,
        # device_class=SensorDeviceClass.DURATION,
        value_fn=lambda device: device.parameters.maintenance_interval,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"maintenance_interval": value},
    ),
    # LED ring Brightness [%]
    GruenbeckCloudEntityDescription(
        key="led_ring_brightness",
        translation_key="led_ring_brightness",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        mode=NumberMode.SLIDER,
        native_unit_of_measurement=PERCENTAGE,
        native_min_value=1,
        native_max_value=100,
        native_step=1,
        value_fn=lambda device: device.parameters.led_ring_brightness,
        update_fn=lambda device, value: {"led_ring_brightness": value},
    ),
    # Residual capacity limit value [%]
    GruenbeckCloudEntityDescription(
        key="residual_capacity_limit",
        translation_key="residual_capacity_limit",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        mode=NumberMode.SLIDER,
        native_min_value=1,
        native_max_value=100,
        native_unit_of_measurement=PERCENTAGE,
        native_step=1,
        value_fn=lambda device: device.parameters.residual_capacity_limit,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"residual_capacity_limit": value},
    ),
    # Current setpoint [mA]
    GruenbeckCloudEntityDescription(
        key="current_setpoint",
        translation_key="current_setpoint",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.current_setpoint,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"current_setpoint": value},
    ),
    # Charge [mAmin]
    GruenbeckCloudEntityDescription(
        key="charge",
        translation_key="charge",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        mode=NumberMode.BOX,
        native_unit_of_measurement=UNIT_OF_MA_MIN,
        value_fn=lambda device: device.parameters.charge,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"charge": value},
    ),
    # Interval of forced regeneration [days]
    GruenbeckCloudEntityDescription(
        key="interval_forced_regeneration",
        translation_key="interval_forced_regeneration",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        mode=NumberMode.SLIDER,
        native_min_value=1,
        native_max_value=365,
        native_step=1,
        native_unit_of_measurement=UnitOfTime.DAYS,
        # device_class=SensorDeviceClass.DURATION,
        value_fn=lambda device: device.parameters.interval_forced_regeneration,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"interval_forced_regeneration": value},
    ),
    # End frequency regeneration valve 1 [Hz]
    GruenbeckCloudEntityDescription(
        key="end_frequency_regeneration_valve",
        translation_key="end_frequency_regeneration_valve",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.end_frequency_regeneration_valve,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"end_frequency_regeneration_valve": value},
    ),
    # End frequency regeneration valve 2 [Hz]
    GruenbeckCloudEntityDescription(
        key="end_frequency_regeneration_valve_2",
        translation_key="end_frequency_regeneration_valve_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.end_frequency_regeneration_valve_2,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"end_frequency_regeneration_valve_2": value},
    ),
    # End frequency blending valve [Hz]
    GruenbeckCloudEntityDescription(
        key="end_frequency_blending_valve",
        translation_key="end_frequency_blending_valve",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.FREQUENCY,
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.end_frequency_blending_valve,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"end_frequency_blending_valve": value},
    ),
    # Treatment volume [m³]
    GruenbeckCloudEntityDescription(
        key="treatment_volume",
        translation_key="treatment_volume",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.WATER,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.treatment_volume,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"treatment_volume": value},
    ),
    # Soft water meter pulse rate [l/Imp]
    GruenbeckCloudEntityDescription(
        key="soft_water_meter_pulse_rate",
        translation_key="soft_water_meter_pulse_rate",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_L_IMP,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.soft_water_meter_pulse_rate,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"soft_water_meter_pulse_rate": value},
    ),
    # Blending water meter pulse rate [l/Imp]
    GruenbeckCloudEntityDescription(
        key="blending_water_meter_pulse_rate",
        translation_key="blending_water_meter_pulse_rate",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_L_IMP,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.blending_water_meter_pulse_rate,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"blending_water_meter_pulse_rate": value},
    ),
    # Regeneration water meter pulse rate [l/Imp]
    GruenbeckCloudEntityDescription(
        key="regeneration_water_meter_pulse_rate",
        translation_key="regeneration_water_meter_pulse_rate",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_L_IMP,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.regeneration_water_meter_pulse_rate,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"regeneration_water_meter_pulse_rate": value},
    ),
    # Capacity figure [m³x°dH]
    GruenbeckCloudEntityDescription(
        key="capacity_figure_monday",
        translation_key="capacity_figure_monday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_monday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_monday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_tuesday",
        translation_key="capacity_figure_tuesday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_tuesday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_tuesday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_wednesday",
        translation_key="capacity_figure_wednesday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_wednesday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_wednesday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_thursday",
        translation_key="capacity_figure_thursday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_thursday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_thursday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_friday",
        translation_key="capacity_figure_friday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_friday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_friday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_saturday",
        translation_key="capacity_figure_saturday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_saturday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_saturday": value},
    ),
    GruenbeckCloudEntityDescription(
        key="capacity_figure_sunday",
        translation_key="capacity_figure_sunday",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UNIT_OF_M3_X_DH,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.capacity_figure_sunday,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"capacity_figure_sunday": value},
    ),
    # Nominal flow rate [m³/h]
    GruenbeckCloudEntityDescription(
        key="nominal_flow_rate",
        translation_key="nominal_flow_rate",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.VOLUME_FLOW_RATE,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.nominal_flow_rate,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"nominal_flow_rate": value},
    ),
    # Regeneration monitoring time [min]
    GruenbeckCloudEntityDescription(
        key="regeneration_monitoring_time",
        translation_key="regeneration_monitoring_time",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        # device_class=SensorDeviceClass.DURATION,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.regeneration_monitoring_time,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"regeneration_monitoring_time": value},
    ),
    # Salting monitoring time [min]
    GruenbeckCloudEntityDescription(
        key="salting_monitoring_time",
        translation_key="salting_monitoring_time",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        # device_class=SensorDeviceClass.DURATION,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.salting_monitoring_time,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"salting_monitoring_time": value},
    ),
    # Slow rinse [min]
    GruenbeckCloudEntityDescription(
        key="slow_rinse",
        translation_key="slow_rinse",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        # device_class=SensorDeviceClass.DURATION,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.slow_rinse,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"slow_rinse": value},
    ),
    # Backwash [l]
    GruenbeckCloudEntityDescription(
        key="backwash",
        translation_key="backwash",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.backwash,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"backwash": value},
    ),
    # Washing out [l]
    GruenbeckCloudEntityDescription(
        key="washing_out",
        translation_key="washing_out",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.washing_out,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"washing_out": value},
    ),
    # Minimum filling volume smallest cap [l]
    GruenbeckCloudEntityDescription(
        key="minimum_filling_volume_smallest_cap",
        translation_key="minimum_filling_volume_smallest_cap",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.minimum_filling_volume_smallest_cap,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"minimum_filling_volume_smallest_cap": value},
    ),
    # Maximum filling volume smallest cap [l]
    GruenbeckCloudEntityDescription(
        key="maximum_filling_volume_smallest_cap",
        translation_key="maximum_filling_volume_smallest_cap",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.maximum_filling_volume_smallest_cap,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"maximum_filling_volume_smallest_cap": value},
    ),
    # Minimum filling volume largest cap [l]
    GruenbeckCloudEntityDescription(
        key="minimum_filling_volume_largest_cap",
        translation_key="minimum_filling_volume_largest_cap",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.minimum_filling_volume_largest_cap,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"minimum_filling_volume_largest_cap": value},
    ),
    # Maximum filling volume largest cap [l]
    GruenbeckCloudEntityDescription(
        key="maximum_filling_volume_largest_cap",
        translation_key="maximum_filling_volume_largest_cap",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        device_class=NumberDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.LITERS,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.maximum_filling_volume_largest_cap,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"maximum_filling_volume_largest_cap": value},
    ),
    # Longest switch-on time chlorine cell [min]
    GruenbeckCloudEntityDescription(
        key="longest_switch_on_time_chlorine_cell",
        translation_key="longest_switch_on_time_chlorine_cell",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        # device_class=SensorDeviceClass.DURATION,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.longest_switch_on_time_chlorine_cell,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"longest_switch_on_time_chlorine_cell": value},
    ),
    # Maximum remaining time regeneration [min]
    GruenbeckCloudEntityDescription(
        key="maximum_remaining_time_regeneration",
        translation_key="maximum_remaining_time_regeneration",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        # device_class=SensorDeviceClass.DURATION,
        mode=NumberMode.BOX,
        value_fn=lambda device: device.parameters.maximum_remaining_time_regeneration,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"maximum_remaining_time_regeneration": value},
    ),
)
# # Programmable output function
# programmable_output_function: int | None = field(
#     default=None,
#     metadata=json_config(field_name="pprogout"),
# )
# # Programmable input function
# programmable_input_function: int | None = field(
#     default=None,
#     metadata=json_config(field_name="pprogin"),
# )
#
# # Reaction to power failure > 5 min
# reaction_to_power_failure: int | None = field(
#     default=None,
#     metadata=json_config(field_name="ppowerfail"),
# )
#
# # Activate/deactivate chlorine cell
# chlorine_cell_mode: int | None = field(
#     default=None,
#     metadata=json_config(field_name="pmodedesinf"),
# )
#
# # Blending monitoring
# blending_monitoring: int | None = field(
#     default=None,
#     metadata=json_config(field_name="pmonblend"),
# )
#
# # System overloaded
# system_overloaded: int | None = field(
#     default=None,
#     metadata=json_config(field_name="poverload"),
# )
# # Unknown Parameter
# ppressurereg: int | None = field(
#     default=None,
#     metadata=json_config(field_name="ppressurereg"),
# )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities(
        GruenbeckCloudNumberEntity(coordinator, description)
        for description in NUMBERS
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudNumberEntity(GruenbeckCloudEntity, NumberEntity):
    """Define a Grünbeck Cloud Number entity."""

    entity_description: GruenbeckCloudEntityDescription

    def __init__(
        self,
        coordinator: GruenbeckCloudCoordinator,
        description: GruenbeckCloudEntityDescription,
    ) -> None:
        """Initialize our Grünbeck entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.serial_number}_{description.key}"

    @property
    def native_value(self) -> float | None:
        """Return the state of our sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        new_value = self.entity_description.update_fn(self.coordinator.data, value)
        if new_value is None:
            _LOGGER.warning(
                "Entity %s can currently not be updated through the integration",
                self.entity_id,
            )
            return
        await self.coordinator.update_device_infos_parameters(new_value)
        self.async_write_ha_state()
