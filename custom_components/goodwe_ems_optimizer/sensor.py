"""Sensor platform for GoodWe EMS Optimizer integration."""

import logging
from typing import Any, Final

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_LAST_ACTION,
    ATTR_LAST_MODE_SWITCH,
    ATTR_MODE_SWITCH_LOCKED,
    ATTR_OPTIMIZER_ACTIVE,
    DOMAIN,
)
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

    entities = [
        OptimizerActiveSensor(coordinator, entry),
        LastActionSensor(coordinator, entry),
        LastModeSwitchSensor(coordinator, entry),
        ModeSwitchLockedSensor(coordinator, entry),
    ]

    async_add_entities(entities)
    _LOGGER.debug("Added %d sensor entities", len(entities))


class GoodWeEMSOptimizerSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for GoodWe EMS Optimizer sensors."""

    def __init__(
        self,
        coordinator: GoodWeEMSOptimizerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._entry = entry
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "GoodWe EMS Optimizer",
            "model": "Hybrid Inverter Controller",
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID for the sensor."""
        return f"{self._entry.entry_id}_{self.entity_description.key}"


class OptimizerActiveSensor(GoodWeEMSOptimizerSensorBase):
    """Sensor indicating if optimizer is active."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Optimizer Active"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_optimizer_active"

    @property
    def state(self) -> bool:
        """Return the current state."""
        return self.coordinator.data.get(ATTR_OPTIMIZER_ACTIVE, False)

    @property
    def icon(self) -> str:
        """Return icon for the sensor."""
        return "mdi:brain" if self.state else "mdi:brain-off"


class LastActionSensor(GoodWeEMSOptimizerSensorBase):
    """Sensor for the last action taken by the optimizer."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Last Action"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_last_action"

    @property
    def state(self) -> str:
        """Return the current state."""
        return self.coordinator.data.get(ATTR_LAST_ACTION, "unknown")

    @property
    def icon(self) -> str:
        """Return icon for the sensor."""
        return "mdi:history"


class LastModeSwitchSensor(GoodWeEMSOptimizerSensorBase):
    """Sensor for the timestamp of last mode switch."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Last Mode Switch"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_last_mode_switch"

    @property
    def state(self) -> Any:
        """Return the current state."""
        return self.coordinator.data.get(ATTR_LAST_MODE_SWITCH)

    @property
    def icon(self) -> str:
        """Return icon for the sensor."""
        return "mdi:clock-outline"


class ModeSwitchLockedSensor(GoodWeEMSOptimizerSensorBase):
    """Sensor indicating if mode switching is locked."""

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Mode Switch Locked"

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_mode_switch_locked"

    @property
    def state(self) -> bool:
        """Return the current state."""
        return self.coordinator.data.get(ATTR_MODE_SWITCH_LOCKED, False)

    @property
    def icon(self) -> str:
        """Return icon for the sensor."""
        return "mdi:lock" if self.state else "mdi:lock-open"
