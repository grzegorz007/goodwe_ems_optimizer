"""Config flow for GoodWe EMS Optimizer integration."""

import logging
from typing import Any, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector

_LOGGER = logging.getLogger(__name__)

DOMAIN = "goodwe_ems_optimizer"
TITLE = "GoodWe EMS Optimizer"

# Config Flow Keys
CONF_SCAN_INTERVAL = "scan_interval"
CONF_INVERTER_MODE_SELECT = "inverter_mode_select"
CONF_EMS_MODE_SELECT = "ems_mode_select"
CONF_EMS_POWER_LIMIT = "ems_power_limit"
CONF_GRID_EXPORT_LIMIT = "grid_export_limit"
CONF_BATTERY_SOC_SENSOR = "battery_soc_sensor"
CONF_PV_POWER_SENSOR = "pv_power_sensor"
CONF_HOUSE_CONSUMPTION_SENSOR = "house_consumption_sensor"
CONF_GRID_IMPORT_SENSOR = "grid_import_sensor"
CONF_EMHASS_MIN_SOC_SENSOR = "emhass_min_soc_sensor"
CONF_EMHASS_BATT_FORECAST_SENSOR = "emhass_batt_forecast_sensor"
CONF_EMHASS_GRID_FORECAST_SENSOR = "emhass_grid_forecast_sensor"
CONF_ENABLE_ANTI_TATTERING = "enable_anti_tattering"
CONF_MIN_MODE_SWITCH_INTERVAL = "min_mode_switch_interval"

# Default Values
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_MIN_MODE_SWITCH_INTERVAL = 60
DEFAULT_ENABLE_ANTI_TATTERING = True


class GoodWeEMSOptimizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for GoodWe EMS Optimizer."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[dict[str, Any]] = None):
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

    async def async_step_init(self, user_input: Optional[dict[str, Any]] = None):
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
                    CONF_INVERTER_MODE_SELECT,
                    default=options.get(CONF_INVERTER_MODE_SELECT, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="select",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_EMS_MODE_SELECT,
                    default=options.get(CONF_EMS_MODE_SELECT, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="select",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_EMS_POWER_LIMIT,
                    default=options.get(CONF_EMS_POWER_LIMIT, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="number",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_GRID_EXPORT_LIMIT,
                    default=options.get(CONF_GRID_EXPORT_LIMIT, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="number",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_BATTERY_SOC_SENSOR,
                    default=options.get(CONF_BATTERY_SOC_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_PV_POWER_SENSOR,
                    default=options.get(CONF_PV_POWER_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_HOUSE_CONSUMPTION_SENSOR,
                    default=options.get(CONF_HOUSE_CONSUMPTION_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_GRID_IMPORT_SENSOR,
                    default=options.get(CONF_GRID_IMPORT_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_EMHASS_MIN_SOC_SENSOR,
                    default=options.get(CONF_EMHASS_MIN_SOC_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_EMHASS_BATT_FORECAST_SENSOR,
                    default=options.get(CONF_EMHASS_BATT_FORECAST_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_EMHASS_GRID_FORECAST_SENSOR,
                    default=options.get(CONF_EMHASS_GRID_FORECAST_SENSOR, ""),
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        multiple=False,
                    )
                ),
                vol.Optional(
                    CONF_ENABLE_ANTI_TATTERING,
                    default=options.get(
                        CONF_ENABLE_ANTI_TATTERING,
                        DEFAULT_ENABLE_ANTI_TATTERING,
                    ),
                ): bool,
                vol.Optional(
                    CONF_MIN_MODE_SWITCH_INTERVAL,
                    default=options.get(
                        CONF_MIN_MODE_SWITCH_INTERVAL,
                        DEFAULT_MIN_MODE_SWITCH_INTERVAL,
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=600)),
            }

            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(schema),
            )
        except Exception as err:
            _LOGGER.error("Error in options flow: %s", err, exc_info=True)
            return self.async_abort(reason="unknown_error")
