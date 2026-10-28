"""Coordinator for Grünbeck Cloud integration."""
from __future__ import annotations

import logging
from typing import Any

from pygruenbeck_cloud import PyGruenbeckCloud
from pygruenbeck_cloud.exceptions import (
    PyGruenbeckCloudConnectionClosedError,
    PyGruenbeckCloudConnectionError,
    PyGruenbeckCloudError,
    PyGruenbeckCloudMissingAuthTokenError,
    PyGruenbeckCloudResponseStatusError,
    PyGruenbeckCloudUpdateParameterError,
)
from pygruenbeck_cloud.models import Device, DeviceError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    callback,
)
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_DEVICE_ID,
    DOMAIN,
    EVENT_DEVICE_ALERT,
    SERVICE_PARAM_PARAMETER,
    SERVICE_PARAM_VALUE,
    UPDATE_INTERVAL,
    UPDATE_INTERVAL_RETRY,
)
from .helpers import alert_key, unresolved_errors

_LOGGER = logging.getLogger(__name__)


class GruenbeckCloudCoordinator(DataUpdateCoordinator[Device]):
    """Grünbeck Cloud Coordinator."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize Coordinator."""
        self.config_entry = config_entry
        self.api = self._create_api()
        self._device_id = config_entry.data[CONF_DEVICE_ID]

        self.unsub: CALLBACK_TYPE | None = None
        self._known_alert_keys: set[tuple[int, str, str]] = set()
        self._pending_alerts: list[DeviceError] = []
        self._alerts_initialized = False
        self._listen_task_running = False
        self._ws_generation = 0
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    def _create_api(self) -> PyGruenbeckCloud:
        """Create API client from config entry credentials."""
        api = PyGruenbeckCloud(
            username=self.config_entry.data[CONF_USERNAME],
            password=self.config_entry.data[CONF_PASSWORD],
        )
        api.logger = _LOGGER
        return api

    async def disconnect(self) -> None:
        """Disconnect from API."""
        await self.api.disconnect()

    async def _reset_websocket(self, *, recreate_client: bool = True) -> None:
        """Drop websocket state so the next update reconnects cleanly."""
        self._ws_generation += 1

        if self.unsub:
            self.unsub()
            self.unsub = None

        self._listen_task_running = False
        self.update_interval = UPDATE_INTERVAL_RETRY

        old_api = self.api
        old_device = old_api.device

        try:
            await old_api.disconnect()
        except Exception:  # noqa: BLE001
            _LOGGER.debug("Disconnect during websocket reset failed", exc_info=True)

        if recreate_client:
            # Recreate client: library disconnect() no-ops when the socket is already
            # closed but the session can remain stuck, freezing updates (#199).
            self.api = self._create_api()
            if old_device is not None:
                self.api.device = old_device

    @callback
    def consume_pending_alerts(self) -> list[DeviceError]:
        """Return and clear alerts that should be emitted as events."""
        alerts = self._pending_alerts
        self._pending_alerts = []
        return alerts

    def _process_device_alerts(self, device: Device) -> None:
        """Detect new unresolved alerts and notify Home Assistant."""
        unresolved = unresolved_errors(device)
        current_keys = {alert_key(error) for error in unresolved}

        # Seed on first update so reloads don't re-fire existing alerts.
        if not self._alerts_initialized:
            self._known_alert_keys = current_keys
            self._alerts_initialized = True
            return

        new_errors = [
            error
            for error in unresolved
            if alert_key(error) not in self._known_alert_keys
        ]

        for error in new_errors:
            event_data = {
                "device_id": device.id,
                "serial_number": device.serial_number,
                "error_code": error.error_code,
                "type": error.type,
                "message": error.message,
                "description": error.description,
                "date": error.date.isoformat(),
            }
            self.hass.bus.async_fire(EVENT_DEVICE_ALERT, event_data)
            self._pending_alerts.append(error)

        self._known_alert_keys = current_keys

    @callback
    def _listen_websocket(self) -> None:
        """Listen to WebSocket updates."""
        if self._listen_task_running:
            return

        self._listen_task_running = True
        listen_generation = self._ws_generation

        async def listen() -> None:
            """Listen for state changes."""
            try:
                try:
                    await self.api.connect()
                except (
                    PyGruenbeckCloudError,
                    PyGruenbeckCloudResponseStatusError,
                ) as err:
                    self.logger.warning("WebSocket connect failed: %s", err)
                    return

                try:
                    await self.api.listen(callback=self.async_set_updated_data)
                except (
                    PyGruenbeckCloudConnectionError,
                    PyGruenbeckCloudConnectionClosedError,
                    PyGruenbeckCloudResponseStatusError,
                ) as err:
                    self.last_update_success = False
                    self.logger.warning("WebSocket listen failed: %s", err)
                except PyGruenbeckCloudError as err:
                    self.last_update_success = False
                    self.async_update_listeners()
                    self.logger.warning("WebSocket error: %s", err)
            finally:
                # Only the active listen generation may reset shared state.
                if listen_generation == self._ws_generation:
                    await self._reset_websocket()

        async def close_websocket(_: Event) -> None:
            """Close WebSocket connection."""
            self.unsub = None
            await self.api.disconnect()

        # Clean disconnect WebSocket on Home Assistant shutdown
        self.unsub = self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STOP, close_websocket
        )

        # Start listener
        self.config_entry.async_create_background_task(
            self.hass, listen(), "gruenbeck-cloud-listen"
        )

    async def service_get_device_salt_measurements(
        self, call: ServiceCall
    ) -> ServiceResponse:
        """Service to get Salt measurements."""
        device = await self.api.get_device_salt_measurements()
        if device.salt is None:
            return {"entries": []}

        return {
            "entries": [
                {
                    "date": item.date.isoformat(),
                    "value": item.value,
                }
                for item in device.salt
            ],
        }

    async def service_get_device_water_measurements(
        self, call: ServiceCall
    ) -> ServiceResponse:
        """Service to get Water measurements."""
        device = await self.api.get_device_water_measurements()
        if device.water is None:
            return {"entries": []}

        return {
            "entries": [
                {
                    "date": item.date.isoformat(),
                    "value": item.value,
                }
                for item in device.water
            ],
        }

    async def service_regenerate(self, call: ServiceCall) -> None:
        """Service to start manual regeneration."""
        await self.api.regenerate()

    async def service_change_settings(self, call: ServiceCall) -> None:
        """Service for update device settings."""
        data = {
            call.data[SERVICE_PARAM_PARAMETER]: call.data[SERVICE_PARAM_VALUE],
        }

        await self.update_device_infos_parameters(data)

    async def update_device_infos_parameters(self, data: dict[str, Any]) -> None:
        """Update Device parameters."""
        try:
            self.data = await self.api.update_device_infos_parameters(data)
        except PyGruenbeckCloudUpdateParameterError as err:
            raise HomeAssistantError(err) from err

    @callback
    def async_set_updated_data(self, data: Device) -> None:
        """Manually update data from WebSocket, avoid stopping refresh interval."""
        self.data = data
        self.last_update_success = True
        self.update_interval = UPDATE_INTERVAL
        self._process_device_alerts(data)

        self.logger.debug(
            "Manually updated %s data",
            self.name,
        )
        self.async_update_listeners()

    async def _async_update_data(self) -> Device:
        """Update regularly data from API."""
        self.logger.debug(
            "Regularly updated %s data",
            self.name,
        )

        try:
            if not self.api.device:
                await self.api.set_device_from_id(self._device_id)
            await self.api.get_device_infos()
            device = await self.api.get_device_infos_parameters()

            try:
                await self.api.get_device_water_measurements()
                await self.api.get_device_salt_measurements()
                if self.api.device is not None:
                    device = self.api.device
            except PyGruenbeckCloudError as err:
                self.logger.debug("Daily measurements unavailable: %s", err)

            # Start listening to websocket at first time / after reset
            if not self.api.connected and not self.unsub:
                self._listen_websocket()
            else:
                try:
                    await self.api.enter_sd()
                    await self.api.refresh_sd()
                except (
                    PyGruenbeckCloudResponseStatusError,
                    PyGruenbeckCloudConnectionError,
                    PyGruenbeckCloudConnectionClosedError,
                ) as err:
                    self.logger.warning(
                        "Realtime refresh failed, scheduling reconnect: %s", err
                    )
                    await self._reset_websocket()

            self._process_device_alerts(device)
            self.update_interval = UPDATE_INTERVAL
            return device
        except PyGruenbeckCloudMissingAuthTokenError as err:
            raise ConfigEntryAuthFailed(
                "Authentication with Grünbeck Cloud failed"
            ) from err
        except (
            IndexError,
            KeyError,
            PyGruenbeckCloudResponseStatusError,
            PyGruenbeckCloudConnectionError,
            PyGruenbeckCloudError,
        ) as err:
            await self._reset_websocket()
            raise UpdateFailed(f"Unable to get data from API: {err}") from err
        except Exception as err:
            await self._reset_websocket()
            raise UpdateFailed(f"Unable to get data from API: {err}") from err
