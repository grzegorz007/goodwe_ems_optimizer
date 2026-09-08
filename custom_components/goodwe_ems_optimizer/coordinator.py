"""Data coordinator for GoodWe EMS Optimizer integration."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Final

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
    ATTR_LAST_MODE_SWITCH,
    ATTR_MODE_SWITCH_LOCKED,
    ATTR_OPTIMIZER_ACTIVE,
    ATTR_PV_POWER,
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
)

_LOGGER: Final = logging.getLogger(__name__)


class GoodWeEMSOptimizerCoordinator(DataUpdateCoordinator):
    """Coordinator for GoodWe EMS Optimizer."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                seconds=config_entry.options.get(
                    CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                )
            ),
        )
        self.config_entry = config_entry
        self.hass = hass

        # Configuration binding
        self._inverter_mode_select: str = config_entry.data.get(
            CONF_INVERTER_MODE_SELECT, ""
        )
        self._ems_mode_select: str = config_entry.data.get(CONF_EMS_MODE_SELECT, "")
        self._ems_power_limit: str = config_entry.data.get(CONF_EMS_POWER_LIMIT, "")
        self._grid_export_limit: str = config_entry.data.get(
            CONF_GRID_EXPORT_LIMIT, ""
        )
        self._battery_soc_sensor: str = config_entry.data.get(
            CONF_BATTERY_SOC_SENSOR, ""
        )
        self._pv_power_sensor: str = config_entry.data.get(CONF_PV_POWER_SENSOR, "")
        self._house_consumption_sensor: str = config_entry.data.get(
            CONF_HOUSE_CONSUMPTION_SENSOR, ""
        )
        self._grid_import_sensor: str = config_entry.data.get(
            CONF_GRID_IMPORT_SENSOR, ""
        )
        self._emhass_min_soc_sensor: str = config_entry.data.get(
            CONF_EMHASS_MIN_SOC_SENSOR, ""
        )
        self._emhass_batt_forecast_sensor: str = config_entry.data.get(
            CONF_EMHASS_BATT_FORECAST_SENSOR, ""
        )
        self._emhass_grid_forecast_sensor: str = config_entry.data.get(
            CONF_EMHASS_GRID_FORECAST_SENSOR, ""
        )

        # Anti-tattering configuration
        self._enable_anti_tattering: bool = config_entry.data.get(
            CONF_ENABLE_ANTI_TATTERING, DEFAULT_ENABLE_ANTI_TATTERING
        )
        self._min_mode_switch_interval: int = config_entry.data.get(
            CONF_MIN_MODE_SWITCH_INTERVAL, DEFAULT_MIN_MODE_SWITCH_INTERVAL
        )

        # State tracking
        self._last_mode_switch: Optional[datetime] = None
        self._mode_switch_locked: bool = False
        self._last_action: str = "initialized"
        self._optimizer_active: bool = True

        # Data snapshot
        self.data: Dict[str, Any] = {
            ATTR_OPTIMIZER_ACTIVE: self._optimizer_active,
            ATTR_LAST_MODE_SWITCH: None,
            ATTR_MODE_SWITCH_LOCKED: self._mode_switch_locked,
            ATTR_LAST_ACTION: self._last_action,
            ATTR_BATTERY_SOC: None,
            ATTR_PV_POWER: None,
            ATTR_HOUSE_CONSUMPTION: None,
            ATTR_GRID_IMPORT: None,
            ATTR_EMHASS_MIN_SOC: None,
            ATTR_EMHASS_BATT_FORECAST: None,
            ATTR_EMHASS_GRID_FORECAST: None,
        }

        _LOGGER.debug("GoodWeEMSOptimizerCoordinator initialized")

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch and update data from Home Assistant entities."""
        try:
            # Collect current entity states
            battery_soc = self._get_state_float(self._battery_soc_sensor)
            pv_power = self._get_state_float(self._pv_power_sensor)
            house_consumption = self._get_state_float(self._house_consumption_sensor)
            grid_import = self._get_state_float(self._grid_import_sensor)
            emhass_min_soc = self._get_state_float(self._emhass_min_soc_sensor)
            emhass_batt_forecast = self._get_state_float(
                self._emhass_batt_forecast_sensor
            )
            emhass_grid_forecast = self._get_state_float(
                self._emhass_grid_forecast_sensor
            )

            _LOGGER.debug(
                "Current state - SoC: %.1f%%, PV: %s W, Load: %s W, Grid: %s W",
                battery_soc if battery_soc is not None else 0,
                pv_power,
                house_consumption,
                grid_import,
            )

            # Update data snapshot
            self.data[ATTR_BATTERY_SOC] = battery_soc
            self.data[ATTR_PV_POWER] = pv_power
            self.data[ATTR_HOUSE_CONSUMPTION] = house_consumption
            self.data[ATTR_GRID_IMPORT] = grid_import
            self.data[ATTR_EMHASS_MIN_SOC] = emhass_min_soc
            self.data[ATTR_EMHASS_BATT_FORECAST] = emhass_batt_forecast
            self.data[ATTR_EMHASS_GRID_FORECAST] = emhass_grid_forecast

            # Check and update mode switch lock state
            self._update_mode_switch_lock()
            self.data[ATTR_MODE_SWITCH_LOCKED] = self._mode_switch_locked
            self.data[ATTR_LAST_MODE_SWITCH] = self._last_mode_switch

            # Run optimization logic
            if self._optimizer_active:
                await self._async_optimize()

            self.data[ATTR_OPTIMIZER_ACTIVE] = self._optimizer_active
            self.data[ATTR_LAST_ACTION] = self._last_action

            return self.data

        except Exception as err:
            _LOGGER.error("Error updating coordinator data: %s", err, exc_info=True)
            raise UpdateFailed(f"Failed to update data: {err}") from err

    def _get_state_float(self, entity_id: str) -> Optional[float]:
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

    def _get_state_str(self, entity_id: str) -> Optional[str]:
        """Get string value from entity state."""
        if not entity_id:
            return None

        state = self.hass.states.get(entity_id)
        if state is None or state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            _LOGGER.debug("Entity %s is unavailable or unknown", entity_id)
            return None

        return state.state

    def _update_mode_switch_lock(self) -> None:
        """Update the mode switch lock state based on time elapsed."""
        if not self._enable_anti_tattering:
            self._mode_switch_locked = False
            return

        if self._last_mode_switch is None:
            self._mode_switch_locked = False
            return

        elapsed = (datetime.now() - self._last_mode_switch).total_seconds()
        self._mode_switch_locked = elapsed < self._min_mode_switch_interval

        if self._mode_switch_locked:
            remaining = self._min_mode_switch_interval - elapsed
            _LOGGER.debug(
                "Mode switch locked for %.1f more seconds", remaining
            )

    async def _async_optimize(self) -> None:
        """
        Main optimization logic (placeholder).
        
        This is where the black-box optimization algorithm runs.
        It reads current state and applies decisions to inverter controls.
        """
        try:
            if self.data[ATTR_BATTERY_SOC] is None:
                _LOGGER.debug("Skipping optimization: battery SoC unavailable")
                self._last_action = "skipped - no battery data"
                return

            # Placeholder for optimization logic
            # TODO: Implement EMS optimization algorithm
            self._last_action = "optimization_cycle_complete"

            _LOGGER.debug("Optimization cycle completed: %s", self._last_action)

        except Exception as err:
            _LOGGER.error("Error during optimization: %s", err, exc_info=True)
            self._last_action = f"error - {err}"

    async def async_set_inverter_mode(self, mode: str) -> bool:
        """
        Set the inverter working mode with anti-tattering protection.
        
        Args:
            mode: Target mode (e.g., "general", "self_use")
            
        Returns:
            True if mode was set, False if locked.
        """
        if self._mode_switch_locked:
            _LOGGER.warning(
                "Mode switch locked (%.1f seconds remaining)",
                self._min_mode_switch_interval
                - (datetime.now() - self._last_mode_switch).total_seconds(),
            )
            self._last_action = "mode_change_rejected_locked"
            return False

        try:
            current_mode = self._get_state_str(self._inverter_mode_select)
            if current_mode == mode:
                _LOGGER.debug("Inverter already in mode: %s", mode)
                self._last_action = f"mode_already_set - {mode}"
                return True

            _LOGGER.info("Setting inverter mode to: %s", mode)
            await self.hass.services.async_call(
                "select",
                "select_option",
                {
                    "entity_id": self._inverter_mode_select,
                    "option": mode,
                },
            )

            self._last_mode_switch = datetime.now()
            self._last_action = f"inverter_mode_changed - {mode}"
            _LOGGER.info("Inverter mode changed to: %s", mode)
            return True

        except Exception as err:
            _LOGGER.error("Error setting inverter mode: %s", err, exc_info=True)
            self._last_action = f"mode_change_error - {err}"
            return False

    async def async_set_ems_mode(self, mode: str) -> bool:
        """
        Set the EMS mode.
        
        Args:
            mode: Target EMS mode (e.g., "auto", "charge_battery")
            
        Returns:
            True if mode was set, False otherwise.
        """
        try:
            current_mode = self._get_state_str(self._ems_mode_select)
            if current_mode == mode:
                _LOGGER.debug("EMS already in mode: %s", mode)
                self._last_action = f"ems_mode_already_set - {mode}"
                return True

            _LOGGER.info("Setting EMS mode to: %s", mode)
            await self.hass.services.async_call(
                "select",
                "select_option",
                {
                    "entity_id": self._ems_mode_select,
                    "option": mode,
                },
            )

            self._last_action = f"ems_mode_changed - {mode}"
            _LOGGER.info("EMS mode changed to: %s", mode)
            return True

        except Exception as err:
            _LOGGER.error("Error setting EMS mode: %s", err, exc_info=True)
            self._last_action = f"ems_mode_change_error - {err}"
            return False

    async def async_set_power_limit(self, power: float) -> bool:
        """
        Set the EMS power limit.
        
        Args:
            power: Power limit in watts
            
        Returns:
            True if power limit was set, False otherwise.
        """
        try:
            _LOGGER.info("Setting EMS power limit to: %.1f W", power)
            await self.hass.services.async_call(
                "number",
                "set_value",
                {
                    "entity_id": self._ems_power_limit,
                    "value": power,
                },
            )

            self._last_action = f"power_limit_set - {power:.1f}W"
            _LOGGER.info("EMS power limit set to: %.1f W", power)
            return True

        except Exception as err:
            _LOGGER.error("Error setting power limit: %s", err, exc_info=True)
            self._last_action = f"power_limit_error - {err}"
            return False

    async def async_set_export_limit(self, power: float) -> bool:
        """
        Set the grid export limit.
        
        Args:
            power: Export limit in watts
            
        Returns:
            True if export limit was set, False otherwise.
        """
        try:
            _LOGGER.info("Setting grid export limit to: %.1f W", power)
            await self.hass.services.async_call(
                "number",
                "set_value",
                {
                    "entity_id": self._grid_export_limit,
                    "value": power,
                },
            )

            self._last_action = f"export_limit_set - {power:.1f}W"
            _LOGGER.info("Grid export limit set to: %.1f W", power)
            return True

        except Exception as err:
            _LOGGER.error("Error setting export limit: %s", err, exc_info=True)
            self._last_action = f"export_limit_error - {err}"
            return False

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        _LOGGER.info("Shutting down %s coordinator", DOMAIN)
        self._optimizer_active = False
        self.data[ATTR_OPTIMIZER_ACTIVE] = False
