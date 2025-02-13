"""Platform for Grünbeck Cloud text entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.text import TextEntity, TextEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class GruenbeckCloudEntityDescription(TextEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], str | None]
    update_fn: Callable[[Device, str], dict[str, str] | None] = (
        lambda device, value: None
    )


TEXTS: tuple[GruenbeckCloudEntityDescription, ...] = (
    #################################################################
    #                                                               #
    # Disabled Entities - Need to be activated manually in Frontend #
    #                                                               #
    #################################################################
    # Installer information
    GruenbeckCloudEntityDescription(
        key="installer_name",
        translation_key="installer_name",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.installer_name,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"installer_name": value},
    ),
    GruenbeckCloudEntityDescription(
        key="installer_phone",
        translation_key="installer_phone",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.installer_phone,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"installer_phone": value},
    ),
    GruenbeckCloudEntityDescription(
        key="installer_email",
        translation_key="installer_email",
        entity_category=EntityCategory.CONFIG,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.parameters.installer_email,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"installer_email": value},
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
        GruenbeckCloudTextEntity(coordinator, description)
        for description in TEXTS
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudTextEntity(GruenbeckCloudEntity, TextEntity):
    """Define a Grünbeck Cloud Text entity."""

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
    def native_value(self) -> str | None:
        """Return the state of our sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_set_native_value(self, value: str) -> None:
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
