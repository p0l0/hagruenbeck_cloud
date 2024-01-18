"""Models for the Grünbeck Cloud integration."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import GruenbeckCloudCoordinator


class GruenbeckCloudEntity(CoordinatorEntity[GruenbeckCloudCoordinator]):
    """Base Grünbeck Cloud Entity class."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for our Grünbeck Device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.id)},
            name=self.coordinator.data.id,
            manufacturer=MANUFACTURER,
            serial_number=self.coordinator.data.serial_number,
            model=self.coordinator.data.series,
            hw_version=self.coordinator.data.hardware_version,
            sw_version=self.coordinator.data.software_version,
        )
