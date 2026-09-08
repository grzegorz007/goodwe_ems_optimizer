# GoodWe EMS Optimizer

A black-box Energy Management System (EMS) optimizer integration for Home Assistant that controls GoodWe hybrid inverters based on optimized forecasts, dynamic pricing, and energy management strategies.

## Features

- 🔌 **Inverter Mode Control**: Automatic switching between `general` and `self_use` modes
- ⚡ **EMS Mode Management**: Control `auto`, `charge_battery`, `discharge_battery`, `export_ac`, and `battery_standby` modes
- 🔋 **Battery Optimization**: Battery SoC-aware decision making
- 📊 **EMHASS Integration**: Support for EMHASS forecasts and optimization outputs
- 💰 **Dynamic Pricing**: Pricing-aware charging/discharging strategies
- 🛡️ **Anti-Tattering**: Hard-coded hysteresis filter to prevent inverter mode oscillations
- 🎛️ **Config Flow UI**: Graphical entity binding without YAML editing
- 📈 **Diagnostic Sensors**: Real-time monitoring of optimizer state and actions

## Installation

### Via HACS

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click **+ Create Integration** → Search for "GoodWe EMS Optimizer"
4. Install and restart Home Assistant

### Manual

1. Copy `custom_components/goodwe_ems_optimizer/` to your Home Assistant `custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services** → **Create Integration**
4. Search for "GoodWe EMS Optimizer" and follow the Config Flow

## Configuration

All configuration is handled through the Home Assistant UI:

1. **Name**: Integration instance name
2. **Entity Bindings**:
   - Inverter Working Mode Select
   - EMS Mode Select
   - EMS Power Limit (number)
   - Grid Export Limit (number)
   - Battery SoC Sensor
   - PV Power Sensor
   - House Consumption Sensor
   - Grid Import Sensor
   - EMHASS Min SoC Sensor (optional)
   - EMHASS Battery Forecast Sensor (optional)
   - EMHASS Grid Forecast Sensor (optional)

3. **Advanced Settings**:
   - **Scan Interval**: Update frequency in seconds (default: 60)
   - **Enable Anti-Tattering**: Prevent rapid mode switches (default: enabled)
   - **Min Mode Switch Interval**: Minimum seconds between mode changes (default: 60)

## Architecture

### Core Components

- **Config Flow** (`config_flow.py`): GUI for entity binding and parameter setup
- **Coordinator** (`coordinator.py`): Core optimization logic, state management, and inverter control
- **Sensors** (`sensor.py`): Diagnostic output showing optimizer state
- **Select** (`select.py`): Optional mode selectors for manual override

### Black-Box Design

All optimization decisions are made internally in Python without exposing automations or complex logic to the user interface. The integration handles:

- State machine transitions
- Hysteresis filtering
- Power calculations
- Forecast evaluation
- Pricing-based decisions

## Entities Created

### Sensors (Diagnostic)

- `sensor.<name>_optimizer_active`: Whether the optimizer is running
- `sensor.<name>_last_action`: Description of the last action taken
- `sensor.<name>_last_mode_switch`: Timestamp of last inverter mode change
- `sensor.<name>_mode_switch_locked`: Whether mode switching is currently locked

### Select (Optional)

- `select.<name>_optimizer_mode`: Manual mode override (automatic/manual/disabled)

## Anti-Tattering Protection

The integration includes a hard-coded anti-tattering mechanism that prevents rapid oscillations of inverter modes:

- **Lockout Duration**: Configurable 10-600 seconds (default: 60)
- **Applies To**: Inverter mode changes only
- **Benefit**: Reduces wear on inverter hardware and prevents command spam

## Logging

Enable debug logging to monitor optimizer behavior:

```yaml
logger:
  logs:
    homeassistant.components.goodwe_ems_optimizer: debug
```

## Development

### Project Structure

```
custom_components/goodwe_ems_optimizer/
├── manifest.json           # HACS metadata
├── const.py                # Constants and enums
├── __init__.py             # Component initialization
├── config_flow.py          # UI configuration
├── coordinator.py          # Core optimization logic
├── sensor.py               # Diagnostic sensors
└── select.py               # Optional selectors
```

### Future Enhancements

- [ ] Advanced optimization algorithm using EMHASS compute
- [ ] Machine learning-based forecasting
- [ ] Multi-tariff pricing support
- [ ] Grid services integration
- [ ] Predictive battery management
- [ ] Web dashboard for monitoring

## Support

For issues, feature requests, or contributions, please visit:
[GitHub Issues](https://github.com/grzegorz007/goodwe_ems_optimizer/issues)

## License

MIT License - See LICENSE file for details

## Disclaimer

This integration is provided as-is. Use at your own risk. Always test thoroughly before deploying to a production environment. The developer is not responsible for any damage or data loss caused by using this integration.
