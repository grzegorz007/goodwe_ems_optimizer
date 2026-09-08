"""Constants for the GoodWe EMS Optimizer integration."""

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
