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

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                self.devices = await self.get_devices(user_input)
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
                if (
                    len(self.devices) > 0
                ):  # @TODO - change to > 1, so that we skip this step if we have only 1 device
                    self.config_data = user_input
                    return await self.async_step_select_device()

                device = self.devices[0]
                user_input[CONF_DEVICE_ID] = device.id
                return self.async_create_entry(title=device.name, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the device selection."""
        errors: dict[str, str] = {}
        if user_input is not None:
            # Make sure device was not added before
            device = self.devices[int(user_input[CONF_DEVICE_ID])]
            await self.async_set_unique_id(device.serial_number)
            self._abort_if_unique_id_configured()

            config_data = self.config_data
            config_data[CONF_DEVICE_ID] = device.id

            return self.async_create_entry(title=device.id, data=config_data)

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
                raise CannotConnect(msg)

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


class NoDevicesFound(HomeAssistantError):
    """Error when no devices where found."""
