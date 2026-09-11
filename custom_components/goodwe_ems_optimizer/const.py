"""Constants for the GoodWe EMS Optimizer integration."""

DOMAIN = "goodwe_ems_optimizer"
TITLE = "GoodWe EMS Optimizer"

# Config Flow Keys
CONF_SCAN_INTERVAL = "scan_interval"
CONF_BATTERY_SOC_SENSOR = "battery_soc_sensor"
CONF_PV_POWER_SENSOR = "pv_power_sensor"
CONF_HOUSE_CONSUMPTION_SENSOR = "house_consumption_sensor"
CONF_GRID_IMPORT_SENSOR = "grid_import_sensor"
CONF_EMHASS_MIN_SOC_SENSOR = "emhass_min_soc_sensor"
CONF_EMHASS_BATT_FORECAST_SENSOR = "emhass_batt_forecast_sensor"
CONF_EMHASS_GRID_FORECAST_SENSOR = "emhass_grid_forecast_sensor"

# Optimizer state attributes
ATTR_OPTIMIZER_ACTIVE = "optimizer_active"
ATTR_OPTIMIZER_MODE = "optimizer_mode"
ATTR_LAST_ACTION = "last_action"
ATTR_BATTERY_SOC = "battery_soc"
ATTR_PV_POWER = "pv_power"
ATTR_HOUSE_CONSUMPTION = "house_consumption"
ATTR_GRID_IMPORT = "grid_import"
ATTR_EMHASS_MIN_SOC = "emhass_min_soc"
ATTR_EMHASS_BATT_FORECAST = "emhass_batt_forecast"
ATTR_EMHASS_GRID_FORECAST = "emhass_grid_forecast"
ATTR_REQUESTED_INVERTER_MODE = "requested_inverter_mode"
ATTR_REQUESTED_EMS_MODE = "requested_ems_mode"
ATTR_REQUESTED_EMS_POWER_LIMIT = "requested_ems_power_limit"
ATTR_REQUESTED_GRID_EXPORT_LIMIT = "requested_grid_export_limit"

# Default Values
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_OPTIMIZER_MODE = "automatic"
DEFAULT_CONTROL_SELECT_OPTION = "none"
DEFAULT_REQUESTED_POWER_LIMIT = 0.0

OPTIMIZER_MODE_OPTIONS = ["automatic", "manual", "disabled"]
INVERTER_MODE_OPTIONS = ["none", "general", "self_use"]
EMS_MODE_OPTIONS = [
    "none",
    "auto",
    "charge_battery",
    "discharge_battery",
    "export_ac",
    "battery_standby",
]
