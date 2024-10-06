"""Platform for Grünbeck Cloud time entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import datetime
import logging

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.time import TimeEntity, TimeEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


# @dataclass(frozen=True, kw_only=True)
@dataclass(kw_only=True)
class GruenbeckCloudEntityDescription(TimeEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], datetime.time | None]
    update_fn: Callable[[Device, datetime.time], dict[str, datetime.time] | None] = (
        lambda device, value: None
    )


TIMES: tuple[GruenbeckCloudEntityDescription, ...] = (
    #################################################################
    #                                                               #
    # Disabled Entities - Need to be activated manually in Frontend #
    #                                                               #
    #################################################################
    # Regeneration mode configuration
    GruenbeckCloudEntityDescription(
        key="regeneration_time_monday_1",
        translation_key="regeneration_time_monday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_monday_1,
        update_fn=lambda device, value: {"regeneration_time_monday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_monday_2",
        translation_key="regeneration_time_monday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_monday_2,
        update_fn=lambda device, value: {"regeneration_time_monday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_monday_3",
        translation_key="regeneration_time_monday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_monday_3,
        update_fn=lambda device, value: {"regeneration_time_monday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_tuesday_1",
        translation_key="regeneration_time_tuesday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_tuesday_1,
        update_fn=lambda device, value: {"regeneration_time_tuesday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_tuesday_2",
        translation_key="regeneration_time_tuesday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_tuesday_2,
        update_fn=lambda device, value: {"regeneration_time_tuesday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_tuesday_3",
        translation_key="regeneration_time_tuesday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_tuesday_3,
        update_fn=lambda device, value: {"regeneration_time_tuesday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_wednesday_1",
        translation_key="regeneration_time_wednesday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_wednesday_1,
        update_fn=lambda device, value: {"regeneration_time_wednesday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_wednesday_2",
        translation_key="regeneration_time_wednesday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_wednesday_2,
        update_fn=lambda device, value: {"regeneration_time_wednesday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_wednesday_3",
        translation_key="regeneration_time_wednesday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_wednesday_3,
        update_fn=lambda device, value: {"regeneration_time_wednesday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_thursday_1",
        translation_key="regeneration_time_thursday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_thursday_1,
        update_fn=lambda device, value: {"regeneration_time_thursday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_thursday_2",
        translation_key="regeneration_time_thursday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_thursday_2,
        update_fn=lambda device, value: {"regeneration_time_thursday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_thursday_3",
        translation_key="regeneration_time_thursday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_thursday_3,
        update_fn=lambda device, value: {"regeneration_time_thursday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_friday_1",
        translation_key="regeneration_time_friday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_friday_1,
        update_fn=lambda device, value: {"regeneration_time_friday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_friday_2",
        translation_key="regeneration_time_friday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_friday_2,
        update_fn=lambda device, value: {"regeneration_time_friday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_friday_3",
        translation_key="regeneration_time_friday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_friday_3,
        update_fn=lambda device, value: {"regeneration_time_friday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_saturday_1",
        translation_key="regeneration_time_saturday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_saturday_1,
        update_fn=lambda device, value: {"regeneration_time_saturday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_saturday_2",
        translation_key="regeneration_time_saturday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_saturday_2,
        update_fn=lambda device, value: {"regeneration_time_saturday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_saturday_3",
        translation_key="regeneration_time_saturday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_saturday_3,
        update_fn=lambda device, value: {"regeneration_time_saturday_3": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_sunday_1",
        translation_key="regeneration_time_sunday_1",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_sunday_1,
        update_fn=lambda device, value: {"regeneration_time_sunday_1": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_sunday_2",
        translation_key="regeneration_time_sunday_2",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_sunday_2,
        update_fn=lambda device, value: {"regeneration_time_sunday_2": value},
    ),
    GruenbeckCloudEntityDescription(
        key="regeneration_time_sunday_3",
        translation_key="regeneration_time_sunday_3",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.regeneration_time_sunday_3,
        update_fn=lambda device, value: {"regeneration_time_sunday_3": value},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities(
        GruenbeckCloudTimeEntity(coordinator, description)
        for description in TIMES
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudTimeEntity(GruenbeckCloudEntity, TimeEntity):
    """Define a Grünbeck Cloud Time entity."""

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
    def native_value(self) -> datetime.time | None:
        """Return the state of our sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_set_value(self, value: datetime.time) -> None:
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
