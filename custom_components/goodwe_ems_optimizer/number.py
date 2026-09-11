"""Number platform for GoodWe EMS Optimizer integration."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_REQUESTED_EMS_POWER_LIMIT,
    ATTR_REQUESTED_GRID_EXPORT_LIMIT,
    DOMAIN,
)
from .coordinator import GoodWeEMSOptimizerCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    coordinator: GoodWeEMSOptimizerCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    async_add_entities(
        [
            GoodWeEMSOptimizerNumber(
                coordinator,
                entry,
                ATTR_REQUESTED_EMS_POWER_LIMIT,
                "Requested EMS Power Limit",
            ),
            GoodWeEMSOptimizerNumber(
                coordinator,
                entry,
                ATTR_REQUESTED_GRID_EXPORT_LIMIT,
                "Requested Grid Export Limit",
            ),
        ]
    )


class GoodWeEMSOptimizerNumber(
    CoordinatorEntity[GoodWeEMSOptimizerCoordinator], NumberEntity, RestoreEntity
):
    """Stateful number entity used as an automation control input."""

    _attr_native_min_value = 0
    _attr_native_max_value = 50000
    _attr_native_step = 100
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_mode = NumberMode.BOX

    def __init__(
        self,
        coordinator: GoodWeEMSOptimizerCoordinator,
        entry: ConfigEntry,
        control_key: str,
        name: str,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._control_key = control_key
        self._attr_name = name
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "GoodWe EMS Optimizer",
            "model": "Automation Control Surface",
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_{self._control_key}"

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return float(self.coordinator.get_control_value(self._control_key))

    async def async_added_to_hass(self) -> None:
        """Restore the last configured number value."""
        await super().async_added_to_hass()
        if last_state := await self.async_get_last_state():
            try:
                restored_value = float(last_state.state)
            except (TypeError, ValueError):
                return

            self.coordinator.set_control_value(
                self._control_key,
                restored_value,
                record_action=False,
            )

    async def async_set_native_value(self, value: float) -> None:
        """Store the selected value as user automation intent."""
        min_value = float(self.native_min_value)
        max_value = float(self.native_max_value)
        step = float(self.native_step)
        clamped_value = min(max(float(value), min_value), max_value)
        normalized_steps = round((clamped_value - min_value) / step)
        normalized_value = min_value + (normalized_steps * step)

        self.coordinator.set_control_value(self._control_key, normalized_value)
        self.async_write_ha_state()
