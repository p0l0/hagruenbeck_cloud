"""Config flow for Grünbeck Cloud integration."""
from __future__ import annotations

import logging
from typing import Any

from pygruenbeck_cloud import PyGruenbeckCloud
from pygruenbeck_cloud.models import Device
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelectorMode,
    selector,
)

from .const import CONF_DEVICE_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Grünbeck Cloud."""

    VERSION = 1
    config_data: dict[str, Any] = {}
    devices: list[Device] = []
    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self.devices = await self.get_devices(user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except CannotConnectTimeout:
                errors["base"] = "cannot_connect_timeout"
            except NoDevicesFound:
                errors["base"] = "no_devices"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                self.config_data = user_input
                if len(self.devices) > 1:
                    return await self.async_step_select_device()

                return await self._async_create_device_entry(self.devices[0])

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the device selection."""
        errors: dict[str, str] = {}
        if user_input is not None:
            device = self.devices[int(user_input[CONF_DEVICE_ID])]
            return await self._async_create_device_entry(device)

        device_options: list[SelectOptionDict] = []
        for i, device in enumerate(self.devices):
            device_options.append(
                SelectOptionDict(
                    value=str(i),
                    label=device.id,
                )
            )

        data_schema = {
            vol.Required(CONF_DEVICE_ID): selector(
                {
                    "select": {
                        "options": device_options,
                        "mode": SelectSelectorMode.DROPDOWN,
                        "sort": True,
                    }
                }
            )
        }

        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema(data_schema),
            errors=errors,
        )

    async def async_step_reauth(
        self, entry_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle reauthentication."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauthentication with new credentials."""
        errors: dict[str, str] = {}

        if user_input is not None and self._reauth_entry is not None:
            data = {
                CONF_USERNAME: user_input[CONF_USERNAME],
                CONF_PASSWORD: user_input[CONF_PASSWORD],
                CONF_DEVICE_ID: self._reauth_entry.data[CONF_DEVICE_ID],
            }
            try:
                await self.get_devices(data)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except CannotConnectTimeout:
                errors["base"] = "cannot_connect_timeout"
            except NoDevicesFound:
                errors["base"] = "no_devices"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during reauth")
                errors["base"] = "unknown"
            else:
                return self.async_update_reload_and_abort(
                    self._reauth_entry,
                    data_updates={
                        CONF_USERNAME: user_input[CONF_USERNAME],
                        CONF_PASSWORD: user_input[CONF_PASSWORD],
                    },
                )

        username = ""
        if self._reauth_entry is not None:
            username = self._reauth_entry.data.get(CONF_USERNAME, "")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=username): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def _async_create_device_entry(self, device: Device) -> ConfigFlowResult:
        """Create a config entry for the selected device."""
        await self.async_set_unique_id(device.serial_number)
        self._abort_if_unique_id_configured()

        config_data = {**self.config_data, CONF_DEVICE_ID: device.id}
        return self.async_create_entry(title=device.id, data=config_data)

    async def get_devices(self, data: dict[str, Any]) -> list[Device]:
        """Validate the user input if we are able to connect."""
        try:
            api = PyGruenbeckCloud(
                username=data[CONF_USERNAME],
                password=data[CONF_PASSWORD],
            )

            # Test Login credentials
            if not await api.login():
                msg = "Unable to login to Grünbeck Cloud"
                raise InvalidAuth(msg)

            devices = await api.get_devices()
            _LOGGER.debug("Got %d Devices", len(devices))
            if len(devices) == 0:
                msg = "Unable to find devices"
                raise NoDevicesFound(msg)

        except TimeoutError as err:
            _LOGGER.warning(err)
            raise CannotConnectTimeout from err
        except (IndexError, KeyError) as err:
            _LOGGER.warning(err)
            raise CannotConnect from err
        except ConnectionRefusedError as err:
            _LOGGER.warning(err)
            raise CannotConnect from err

        # Return info that you want to store in the config entry.
        return devices


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class CannotConnectTimeout(HomeAssistantError):
    """Error to indicate we cannot connect due to timeout."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate invalid authentication."""


class NoDevicesFound(HomeAssistantError):
    """Error when no devices where found."""
