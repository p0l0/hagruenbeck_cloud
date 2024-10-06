"""Platform for Grünbeck Cloud switch entity."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from pygruenbeck_cloud.models import Device

from homeassistant import config_entries
from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

_LOGGER = logging.getLogger(__name__)


# @dataclass(frozen=True, kw_only=True)
@dataclass(kw_only=True)
class GruenbeckCloudEntityDescription(SwitchEntityDescription):
    """Describes a Grünbeck Cloud entity."""

    exists_fn: Callable[[Device], bool] = lambda _: True
    value_fn: Callable[[Device], bool | None]
    update_fn: Callable[[Device, bool], dict[str, bool] | None] = (
        lambda device, value: None
    )


SWITCHES: tuple[GruenbeckCloudEntityDescription, ...] = (
    # Daylight saving time
    GruenbeckCloudEntityDescription(
        key="dlst",
        translation_key="dlst",
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.dlst,
        update_fn=lambda device, value: {"dlst": value},
    ),
    # Audio signal on error
    GruenbeckCloudEntityDescription(
        key="buzzer",
        translation_key="buzzer",
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.buzzer,
        update_fn=lambda device, value: {"buzzer": value},
    ),
    # Push Notifications
    GruenbeckCloudEntityDescription(
        key="push_notification",
        translation_key="push_notification",
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.push_notification,
        update_fn=lambda device, value: {"push_notification": value},
    ),
    # Email Notifications
    GruenbeckCloudEntityDescription(
        key="email_notification",
        translation_key="email_notification",
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.email_notification,
        update_fn=lambda device, value: {"email_notification": value},
    ),
    #################################################################
    #                                                               #
    # Disabled Entities - Need to be activated manually in Frontend #
    #                                                               #
    #################################################################
    # Illuminated LED ring flashes for pre-alarm salt supply
    GruenbeckCloudEntityDescription(
        key="led_ring_flash_on_signal",
        translation_key="led_ring_flash_on_signal",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.led_ring_flash_on_signal,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"led_ring_flash_on_signal": value},
    ),
    # Get date/time automatically (NTP)
    GruenbeckCloudEntityDescription(
        key="ntp_sync",
        translation_key="ntp_sync",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.ntp_sync,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"ntp_sync": value},
    ),
    # Function fault signal contact
    GruenbeckCloudEntityDescription(
        key="fault_signal_contact",
        translation_key="fault_signal_contact",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.fault_signal_contact,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"fault_signal_contact": value},
    ),
    # KNX connection
    GruenbeckCloudEntityDescription(
        key="knx",
        translation_key="knx",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.knx,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"knx": value},
    ),
    # Monitoring of nominal flow
    GruenbeckCloudEntityDescription(
        key="nominal_flow_monitoring",
        translation_key="nominal_flow_monitoring",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.nominal_flow_monitoring,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"nominal_flow_monitoring": value},
    ),
    # Disinfection monitoring
    GruenbeckCloudEntityDescription(
        key="disinfection_monitoring",
        translation_key="disinfection_monitoring",
        entity_registry_enabled_default=False,
        entity_category=EntityCategory.CONFIG,
        device_class=SwitchDeviceClass.SWITCH,
        value_fn=lambda device: device.parameters.disinfection_monitoring,
        # We get currently a 500 error from API if we try to change it
        update_fn=lambda device, value: {"disinfection_monitoring": value},
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
        GruenbeckCloudSwitchEntity(coordinator, description)
        for description in SWITCHES
        if description.exists_fn(coordinator.data)
    )


class GruenbeckCloudSwitchEntity(GruenbeckCloudEntity, SwitchEntity):
    """Define a Grünbeck Cloud Switch entity."""

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
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.async_set_value(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.async_set_value(False)

    async def async_set_value(self, value: bool) -> None:
        """Toggle the entity."""
        new_value = self.entity_description.update_fn(self.coordinator.data, value)
        if new_value is None:
            _LOGGER.warning(
                "Entity %s can currently not be updated through the integration",
                self.entity_id,
            )
            return
        await self.coordinator.update_device_infos_parameters(new_value)
        self.async_write_ha_state()
