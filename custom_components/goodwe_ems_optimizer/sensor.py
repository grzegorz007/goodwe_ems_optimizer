"""Sensor platform for GoodWe EMS Optimizer integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_OPTIMIZER_MODE, DOMAIN
from .coordinator import GoodWeEMSOptimizerCoordinator

_LOGGER: Final = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator: GoodWeEMSOptimizerCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    async_add_entities([GoodWeEMSOptimizerStatusSensor(coordinator, entry)])
    _LOGGER.debug("Added status sensor for %s", entry.title)


class GoodWeEMSOptimizerStatusSensor(
    CoordinatorEntity[GoodWeEMSOptimizerCoordinator], SensorEntity
):
    """Diagnostic sensor summarizing optimizer status and telemetry."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_name = "Status"
    _attr_icon = "mdi:transmission-tower-export"

    def __init__(
        self, coordinator: GoodWeEMSOptimizerCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "GoodWe EMS Optimizer",
            "model": "Automation Control Surface",
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_status"

    @property
    def native_value(self) -> str:
        """Return the current optimizer mode."""
        return str(self.coordinator.data[ATTR_OPTIMIZER_MODE])

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        """Expose the current monitoring snapshot and control intent."""
        return dict(self.coordinator.data)
