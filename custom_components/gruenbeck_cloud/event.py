"""Event platform for Grünbeck Cloud."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.components.event import EventEntity, EventEntityDescription
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, EVENT_TYPE_DEVICE_ALERT
from .coordinator import GruenbeckCloudCoordinator
from .models import GruenbeckCloudEntity

EVENT_DESCRIPTION = EventEntityDescription(
    key="device_alert",
    translation_key="device_alert",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the event platform."""
    coordinator: GruenbeckCloudCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    add_entities([GruenbeckCloudEventEntity(coordinator, EVENT_DESCRIPTION)])


class GruenbeckCloudEventEntity(GruenbeckCloudEntity, EventEntity):
    """Emit events for new device alerts."""

    _attr_event_types = [EVENT_TYPE_DEVICE_ALERT]
    entity_description: EventEntityDescription

    def __init__(
        self,
        coordinator: GruenbeckCloudCoordinator,
        description: EventEntityDescription,
    ) -> None:
        """Initialize event entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.data.serial_number}_{description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for error in self.coordinator.consume_pending_alerts():
            self._trigger_event(
                EVENT_TYPE_DEVICE_ALERT,
                {
                    "error_code": error.error_code,
                    "type": error.type,
                    "message": error.message,
                    "description": error.description,
                    "date": error.date.isoformat(),
                },
            )
        super()._handle_coordinator_update()
