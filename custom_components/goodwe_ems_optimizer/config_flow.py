"""Config flow for GoodWe EMS Optimizer integration."""

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_BATTERY_SOC_SENSOR,
    CONF_EMHASS_BATT_FORECAST_SENSOR,
    CONF_EMHASS_GRID_FORECAST_SENSOR,
    CONF_EMHASS_MIN_SOC_SENSOR,
    CONF_GRID_IMPORT_SENSOR,
    CONF_HOUSE_CONSUMPTION_SENSOR,
    CONF_PV_POWER_SENSOR,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    TITLE,
)

_LOGGER = logging.getLogger(__name__)


class GoodWeEMSOptimizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for GoodWe EMS Optimizer."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        if user_input is not None:
            name = user_input.get(CONF_NAME, TITLE)
            await self.async_set_unique_id(name)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=name, data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=TITLE): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return GoodWeEMSOptimizerOptionsFlow(config_entry)


class GoodWeEMSOptimizerOptionsFlow(config_entries.OptionsFlow):
    """Options flow for GoodWe EMS Optimizer."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage the options."""
        try:
            if user_input is not None:
                return self.async_create_entry(title="", data=user_input)

            options = self.config_entry.options

            schema = {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
                vol.Optional(
                    CONF_BATTERY_SOC_SENSOR,
                    default=options.get(CONF_BATTERY_SOC_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_PV_POWER_SENSOR,
                    default=options.get(CONF_PV_POWER_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_HOUSE_CONSUMPTION_SENSOR,
                    default=options.get(CONF_HOUSE_CONSUMPTION_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_GRID_IMPORT_SENSOR,
                    default=options.get(CONF_GRID_IMPORT_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_EMHASS_MIN_SOC_SENSOR,
                    default=options.get(CONF_EMHASS_MIN_SOC_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_EMHASS_BATT_FORECAST_SENSOR,
                    default=options.get(CONF_EMHASS_BATT_FORECAST_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
                vol.Optional(
                    CONF_EMHASS_GRID_FORECAST_SENSOR,
                    default=options.get(CONF_EMHASS_GRID_FORECAST_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor", multiple=False)
                ),
            }

            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(schema),
            )
        except Exception as err:
            _LOGGER.error("Error in options flow: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")
