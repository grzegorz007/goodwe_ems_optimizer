"""Config flow for GoodWe EMS Optimizer integration."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_BATTERY_SOC_SENSOR,
    CONF_EMS_MODE_SELECT,
    CONF_EMS_POWER_LIMIT,
    CONF_EMHASS_BATT_FORECAST_SENSOR,
    CONF_EMHASS_GRID_FORECAST_SENSOR,
    CONF_EMHASS_MIN_SOC_SENSOR,
    CONF_ENABLE_ANTI_TATTERING,
    CONF_GRID_EXPORT_LIMIT,
    CONF_GRID_IMPORT_SENSOR,
    CONF_HOUSE_CONSUMPTION_SENSOR,
    CONF_INVERTER_MODE_SELECT,
    CONF_MIN_MODE_SWITCH_INTERVAL,
    CONF_PV_POWER_SENSOR,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_ANTI_TATTERING,
    DEFAULT_MIN_MODE_SWITCH_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    TITLE,
)

_LOGGER = logging.getLogger(__name__)


class GoodWeEMSOptimizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for GoodWe EMS Optimizer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_NAME])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

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
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return GoodWeEMSOptimizerOptionsFlow(config_entry)


class GoodWeEMSOptimizerOptionsFlow(config_entries.OptionsFlow):
    """Options flow for GoodWe EMS Optimizer."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data = self.config_entry.data

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
                    vol.Required(
                        CONF_INVERTER_MODE_SELECT,
                        default=data.get(CONF_INVERTER_MODE_SELECT, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="select",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_EMS_MODE_SELECT,
                        default=data.get(CONF_EMS_MODE_SELECT, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="select",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_EMS_POWER_LIMIT,
                        default=data.get(CONF_EMS_POWER_LIMIT, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="number",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_GRID_EXPORT_LIMIT,
                        default=data.get(CONF_GRID_EXPORT_LIMIT, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="number",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_BATTERY_SOC_SENSOR,
                        default=data.get(CONF_BATTERY_SOC_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_PV_POWER_SENSOR,
                        default=data.get(CONF_PV_POWER_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_HOUSE_CONSUMPTION_SENSOR,
                        default=data.get(CONF_HOUSE_CONSUMPTION_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_GRID_IMPORT_SENSOR,
                        default=data.get(CONF_GRID_IMPORT_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Optional(
                        CONF_EMHASS_MIN_SOC_SENSOR,
                        default=data.get(CONF_EMHASS_MIN_SOC_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Optional(
                        CONF_EMHASS_BATT_FORECAST_SENSOR,
                        default=data.get(CONF_EMHASS_BATT_FORECAST_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Optional(
                        CONF_EMHASS_GRID_FORECAST_SENSOR,
                        default=data.get(CONF_EMHASS_GRID_FORECAST_SENSOR, ""),
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain="sensor",
                            multiple=False,
                        )
                    ),
                    vol.Required(
                        CONF_ENABLE_ANTI_TATTERING,
                        default=data.get(
                            CONF_ENABLE_ANTI_TATTERING,
                            DEFAULT_ENABLE_ANTI_TATTERING,
                        ),
                    ): bool,
                    vol.Required(
                        CONF_MIN_MODE_SWITCH_INTERVAL,
                        default=data.get(
                            CONF_MIN_MODE_SWITCH_INTERVAL,
                            DEFAULT_MIN_MODE_SWITCH_INTERVAL,
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=10, max=600)),
                }
            ),
            description_placeholders={
                "info": "Configure entity bindings and optimization parameters. "
                "All settings are managed through this interface."
            },
        )
