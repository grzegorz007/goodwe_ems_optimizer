"""Constants for the GoodWe EMS Optimizer integration."""

from enum import Enum

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
DEFAULT_SCAN_INTERVAL = 60  # seconds
DEFAULT_MIN_MODE_SWITCH_INTERVAL = 60  # seconds
DEFAULT_ENABLE_ANTI_TATTERING = True

# Entity State Keys
ATTR_LAST_MODE_SWITCH = "last_mode_switch"
ATTR_MODE_SWITCH_LOCKED = "mode_switch_locked"
ATTR_LAST_ACTION = "last_action"
ATTR_OPTIMIZER_ACTIVE = "optimizer_active"
ATTR_BATTERY_SOC = "battery_soc"
ATTR_PV_POWER = "pv_power"
ATTR_HOUSE_CONSUMPTION = "house_consumption"
ATTR_GRID_IMPORT = "grid_import"
ATTR_EMHASS_MIN_SOC = "emhass_min_soc"
ATTR_EMHASS_BATT_FORECAST = "emhass_batt_forecast"
ATTR_EMHASS_GRID_FORECAST = "emhass_grid_forecast"

# Platform Setup Delay
SETUP_DELAY = 2  # seconds


class InverterMode(str, Enum):
    """Supported inverter working modes."""

    GENERAL = "general"
    SELF_USE = "self_use"


class EMSMode(str, Enum):
    """Supported EMS modes."""

    AUTO = "auto"
    CHARGE_BATTERY = "charge_battery"
    DISCHARGE_BATTERY = "discharge_battery"
    EXPORT_AC = "export_ac"
    BATTERY_STANDBY = "battery_standby"


# Logging
_LOGGER_NAME = f"homeassistant.components.{DOMAIN}"
