"""Platform for Grünbeck Cloud select entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from pygruenbeck_cloud.const import (
    PARAMETER_LED_MODES,
    PARAMETER_OPERATION_MODES,
    PARAMETER_REGENERATION_MODES,
    PARAMETER_WATER_UNITS,
)
from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


# @dataclass(frozen=True, kw_only=True)
@dataclass(kw_only=True)
class GruenbeckCloudEntityDescription(SelectEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], str | None]
    update_fn: Callable[[Device, str], dict[str, int]]


SELECTS: tuple[GruenbeckCloudEntityDescription, ...] = (
    GruenbeckCloudEntityDescription(
        key="regeneration_mode",
        translation_key="regeneration_mode",
        options=list(PARAMETER_REGENERATION_MODES.values()),
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda device: PARAMETER_REGENERATION_MODES[
            device.parameters.regeneration_mode  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "regeneration_mode": list(PARAMETER_REGENERATION_MODES.keys())[
                list(PARAMETER_REGENERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="water_hardness_unit",
        translation_key="water_hardness_unit",
        options=list(PARAMETER_WATER_UNITS.values()),
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda device: PARAMETER_WATER_UNITS[
            device.parameters.water_hardness_unit  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "water_hardness_unit": list(PARAMETER_WATER_UNITS.keys())[
                list(PARAMETER_WATER_UNITS.values()).index(option)
            ]
        },
    ),
    # We get a 500 error from API if we try to change it
    # GruenbeckCloudEntityDescription(
    #     key="language",
    #     translation_key="language",
    #     options=list(PARAMETER_LANGUAGES.values()),
    #     entity_category=EntityCategory.CONFIG,
    #     value_fn=lambda device: PARAMETER_LANGUAGES[device.parameters.language],  # type: ignore[index]  # noqa: E501
    #     update_fn=lambda device, option: {
    #         "language": list(PARAMETER_LANGUAGES.keys())[
    #             list(PARAMETER_LANGUAGES.values()).index(option)
    #         ]
    #     },
    # ),
    GruenbeckCloudEntityDescription(
        key="mode",
        translation_key="mode",
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[device.parameters.mode],  # type: ignore[index]  # noqa: E501
        update_fn=lambda device, option: {
            "mode": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    # Disabled Entities
    GruenbeckCloudEntityDescription(
        key="led_ring_mode",
        translation_key="led_ring_mode",
        options=list(PARAMETER_LED_MODES.values()),
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: PARAMETER_LED_MODES[device.parameters.led_ring_mode],  # type: ignore[index]  # noqa: E501
        update_fn=lambda device, option: {
            "led_ring_mode": list(PARAMETER_LED_MODES.keys())[
                list(PARAMETER_LED_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_monday",
        translation_key="mode_individual_monday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_monday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_monday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_tuesday",
        translation_key="mode_individual_tuesday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_tuesday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_tuesday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_wednesday",
        translation_key="mode_individual_wednesday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_wednesday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_wednesday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_thursday",
        translation_key="mode_individual_thursday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_thursday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_thursday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_friday",
        translation_key="mode_individual_friday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_friday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_friday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_saturday",
        translation_key="mode_individual_saturday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_saturday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_saturday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
    ),
    GruenbeckCloudEntityDescription(
        key="mode_individual_sunday",
        translation_key="mode_individual_sunday",
        entity_registry_enabled_default=False,
        options=list(PARAMETER_OPERATION_MODES.values()),
        value_fn=lambda device: PARAMETER_OPERATION_MODES[
            device.parameters.mode_individual_sunday  # type: ignore[index]
        ],
        update_fn=lambda device, option: {
            "mode_individual_sunday": list(PARAMETER_OPERATION_MODES.keys())[
                list(PARAMETER_OPERATION_MODES.values()).index(option)
            ]
        },
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
        GruenbeckCloudSelectEntity(coordinator, description)
        for description in SELECTS
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudSelectEntity(GruenbeckCloudEntity, SelectEntity):
    """Define a Grünbeck Cloud Select entity."""

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
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_select_option(self, option: str) -> None:
        """Update the current selected option."""
        await self.coordinator.update_device_infos_parameters(
            self.entity_description.update_fn(self.coordinator.data, option)
        )
        self.async_write_ha_state()
