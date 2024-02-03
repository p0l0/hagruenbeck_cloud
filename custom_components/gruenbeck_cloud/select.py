"""Platform for Grünbeck Cloud select entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from pygruenbeck_cloud.const import OPERATION_MODES
from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.select import SelectEntity, SelectEntityDescription
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
        key="mode",
        translation_key="mode",
        options=list(OPERATION_MODES.values()),
        value_fn=lambda device: OPERATION_MODES[device.parameters.mode],  # type: ignore[index]  # noqa: E501
        update_fn=lambda device, option: {
            "mode": list(OPERATION_MODES.keys())[
                list(OPERATION_MODES.values()).index(option)
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
