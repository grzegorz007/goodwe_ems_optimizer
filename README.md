# GoodWe EMS Optimizer

A Home Assistant custom integration for monitoring GoodWe / EMS-related inputs and exposing optimizer control intent as Home Assistant entities. The integration no longer sends inverter commands directly from Python; instead, users can wire the exposed entities into their own Home Assistant automations.

## Features

- 📊 **Monitoring-first flow**: Reads battery, PV, load, grid, and optional EMHASS sensors
- 🎛️ **Automation control entities**: Exposes select/number entities that users can use as automation inputs or triggers
- 🔍 **Transparent behavior**: Optimizer state and latest action are visible in Home Assistant
- 🧩 **Config Flow UI**: Graphical setup for monitoring entity bindings without YAML editing
- 🏠 **Private pre-release friendly**: Ready to test on a branch before publishing a release

## Installation

### Via HACS (private testing)

1. Open HACS in Home Assistant
2. Add this repository as a **Custom repository**
3. Choose the **Integration** category
4. Install the integration and restart Home Assistant

### Manual

1. Copy `custom_components/goodwe_ems_optimizer/` to your Home Assistant `custom_components/` directory
2. Restart Home Assistant
3. Go to **Settings** → **Devices & Services** → **Create Integration**
4. Search for "GoodWe EMS Optimizer" and follow the Config Flow

## Configuration

All configuration is handled through the Home Assistant UI:

1. **Name**: Integration instance name
2. **Monitoring entity bindings**:
   - Battery SoC Sensor
   - PV Power Sensor
   - House Consumption Sensor
   - Grid Import Sensor
   - EMHASS Min SoC Sensor (optional)
   - EMHASS Battery Forecast Sensor (optional)
   - EMHASS Grid Forecast Sensor (optional)
3. **Advanced settings**:
   - **Scan Interval**: Update frequency in seconds (default: 60)

Direct inverter-control bindings were intentionally removed from the options flow. Use the entities created by this integration in your own automations to call the actual inverter entities or services exposed elsewhere in Home Assistant.

## Entities Created

### Diagnostic sensor

- `sensor.<name>_status`
  - State: `automatic`, `manual`, or `disabled`
  - Attributes: latest action, monitored input snapshot, and current control intent values

### Automation control entities

- `select.<name>_optimizer_mode`
- `select.<name>_requested_inverter_mode`
- `select.<name>_requested_ems_mode`
- `number.<name>_requested_ems_power_limit`
- `number.<name>_requested_grid_export_limit`

These entities are intended to be referenced by Home Assistant automations. Example pattern:

```yaml
automation:
  - alias: Apply requested inverter mode
    trigger:
      - platform: state
        entity_id: select.goodwe_ems_optimizer_requested_inverter_mode
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state != 'none' }}"
    action:
      - service: select.select_option
        target:
          entity_id: select.my_actual_goodwe_inverter_mode
        data:
          option: "{{ trigger.to_state.state }}"
```

## Architecture

- **Config Flow** (`config_flow.py`): GUI for monitoring entity bindings and scan interval
- **Coordinator** (`coordinator.py`): Reads Home Assistant state and keeps optimizer/control intent state
- **Sensors** (`sensor.py`): Diagnostic status view
- **Select / Number** (`select.py`, `number.py`): User-controlled automation inputs

The integration keeps relevant monitoring logic in Python, but inverter actuation is left to user-owned Home Assistant automations.

## Development

### Project Structure

```
custom_components/goodwe_ems_optimizer/
├── manifest.json
├── const.py
├── __init__.py
├── config_flow.py
├── coordinator.py
├── sensor.py
├── select.py
└── number.py
```

## Support

For issues, feature requests, or contributions, please visit:
[GitHub Issues](https://github.com/grzegorz007/goodwe_ems_optimizer/issues)

## License

MIT License - See LICENSE file for details
