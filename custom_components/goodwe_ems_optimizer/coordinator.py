"""Data coordinator for GoodWe EMS Optimizer integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ATTR_BATTERY_SOC,
    ATTR_EMHASS_BATT_FORECAST,
    ATTR_EMHASS_GRID_FORECAST,
    ATTR_EMHASS_MIN_SOC,
    ATTR_GRID_IMPORT,
    ATTR_HOUSE_CONSUMPTION,
    ATTR_LAST_ACTION,
    ATTR_OPTIMIZER_ACTIVE,
    ATTR_OPTIMIZER_MODE,
    ATTR_PV_POWER,
    ATTR_REQUESTED_EMS_MODE,
    ATTR_REQUESTED_EMS_POWER_LIMIT,
    ATTR_REQUESTED_GRID_EXPORT_LIMIT,
    ATTR_REQUESTED_INVERTER_MODE,
    CONF_BATTERY_SOC_SENSOR,
    CONF_EMHASS_BATT_FORECAST_SENSOR,
    CONF_EMHASS_GRID_FORECAST_SENSOR,
    CONF_EMHASS_MIN_SOC_SENSOR,
    CONF_GRID_IMPORT_SENSOR,
    CONF_HOUSE_CONSUMPTION_SENSOR,
    CONF_PV_POWER_SENSOR,
    CONF_SCAN_INTERVAL,
    DEFAULT_CONTROL_SELECT_OPTION,
    DEFAULT_OPTIMIZER_MODE,
    DEFAULT_REQUESTED_POWER_LIMIT,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER: Final = logging.getLogger(__name__)


class GoodWeEMSOptimizerCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for GoodWe EMS Optimizer."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=config_entry.options.get(
                    CONF_SCAN_INTERVAL,
                    config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                )
            ),
        )
        self.config_entry = config_entry
        self.hass = hass

        self._battery_soc_sensor = self._get_entry_value(CONF_BATTERY_SOC_SENSOR)
        self._pv_power_sensor = self._get_entry_value(CONF_PV_POWER_SENSOR)
        self._house_consumption_sensor = self._get_entry_value(
            CONF_HOUSE_CONSUMPTION_SENSOR
        )
        self._grid_import_sensor = self._get_entry_value(CONF_GRID_IMPORT_SENSOR)
        self._emhass_min_soc_sensor = self._get_entry_value(CONF_EMHASS_MIN_SOC_SENSOR)
        self._emhass_batt_forecast_sensor = self._get_entry_value(
            CONF_EMHASS_BATT_FORECAST_SENSOR
        )
        self._emhass_grid_forecast_sensor = self._get_entry_value(
            CONF_EMHASS_GRID_FORECAST_SENSOR
        )

        self.data = {
            ATTR_OPTIMIZER_ACTIVE: True,
            ATTR_OPTIMIZER_MODE: DEFAULT_OPTIMIZER_MODE,
            ATTR_LAST_ACTION: "initialized",
            ATTR_BATTERY_SOC: None,
            ATTR_PV_POWER: None,
            ATTR_HOUSE_CONSUMPTION: None,
            ATTR_GRID_IMPORT: None,
            ATTR_EMHASS_MIN_SOC: None,
            ATTR_EMHASS_BATT_FORECAST: None,
            ATTR_EMHASS_GRID_FORECAST: None,
            ATTR_REQUESTED_INVERTER_MODE: DEFAULT_CONTROL_SELECT_OPTION,
            ATTR_REQUESTED_EMS_MODE: DEFAULT_CONTROL_SELECT_OPTION,
            ATTR_REQUESTED_EMS_POWER_LIMIT: DEFAULT_REQUESTED_POWER_LIMIT,
            ATTR_REQUESTED_GRID_EXPORT_LIMIT: DEFAULT_REQUESTED_POWER_LIMIT,
        }

    def _get_entry_value(self, key: str, default: str = "") -> str:
        """Return a config entry value, preferring options over stored data."""
        return self.config_entry.options.get(
            key,
            self.config_entry.data.get(key, default),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch and update data from Home Assistant entities."""
        try:
            self.data[ATTR_BATTERY_SOC] = self._get_state_float(self._battery_soc_sensor)
            self.data[ATTR_PV_POWER] = self._get_state_float(self._pv_power_sensor)
            self.data[ATTR_HOUSE_CONSUMPTION] = self._get_state_float(
                self._house_consumption_sensor
            )
            self.data[ATTR_GRID_IMPORT] = self._get_state_float(self._grid_import_sensor)
            self.data[ATTR_EMHASS_MIN_SOC] = self._get_state_float(
                self._emhass_min_soc_sensor
            )
            self.data[ATTR_EMHASS_BATT_FORECAST] = self._get_state_float(
                self._emhass_batt_forecast_sensor
            )
            self.data[ATTR_EMHASS_GRID_FORECAST] = self._get_state_float(
                self._emhass_grid_forecast_sensor
            )

            optimizer_mode = self.data[ATTR_OPTIMIZER_MODE]
            self.data[ATTR_OPTIMIZER_ACTIVE] = optimizer_mode != "disabled"

            if optimizer_mode == "automatic":
                await self._async_optimize()
            elif optimizer_mode == "manual":
                self.data[ATTR_LAST_ACTION] = "manual automation control"
            else:
                self.data[ATTR_LAST_ACTION] = "optimizer disabled"

            return self.data

        except Exception as err:
            _LOGGER.error("Error updating coordinator data: %s", err, exc_info=True)
            raise UpdateFailed(f"Failed to update data: {err}") from err

    def _get_state_float(self, entity_id: str) -> float | None:
        """Get float value from entity state."""
        if not entity_id:
            return None

        state = self.hass.states.get(entity_id)
        if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            _LOGGER.debug("Entity %s is unavailable or unknown", entity_id)
            return None

        try:
            return float(state.state)
        except (ValueError, TypeError):
            _LOGGER.warning(
                "Cannot convert state of %s to float: %s", entity_id, state.state
            )
            return None

    async def _async_optimize(self) -> None:
        """Keep the monitoring loop active without directly actuating the inverter."""
        if self.data[ATTR_BATTERY_SOC] is None:
            self.data[ATTR_LAST_ACTION] = "skipped - no battery data"
            return

        self.data[ATTR_LAST_ACTION] = "monitoring cycle complete"

    @callback
    def get_control_value(self, key: str) -> Any:
        """Return a user-controlled automation value."""
        return self.data[key]

    @callback
    def set_control_value(
        self,
        key: str,
        value: Any,
        *,
        update_listeners: bool = True,
        record_action: bool = True,
    ) -> None:
        """Persist a user-controlled automation value in coordinator state."""
        self.data[key] = value

        if key == ATTR_OPTIMIZER_MODE:
            self.data[ATTR_OPTIMIZER_ACTIVE] = value != "disabled"

        if record_action:
            self.data[ATTR_LAST_ACTION] = f"control intent updated - {key}"

        if update_listeners:
            self.async_update_listeners()

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        _LOGGER.info("Shutting down %s coordinator", DOMAIN)
        self.data[ATTR_OPTIMIZER_ACTIVE] = False
