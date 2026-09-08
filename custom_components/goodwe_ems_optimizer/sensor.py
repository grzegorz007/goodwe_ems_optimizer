"""Sensor platform for GoodWe EMS Optimizer integration."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

DOMAIN = "goodwe_ems_optimizer"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    _LOGGER.debug("Setting up sensor platform")
    
    entities = [
        StatusSensor(entry),
    ]
    
    async_add_entities(entities)


class StatusSensor(SensorEntity):
    """Basic status sensor."""

    def __init__(self, entry: ConfigEntry):
        """Initialize the sensor."""
        self._entry = entry
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return f"{self._entry.entry_id}_status"

    @property
    def name(self) -> str:
        """Return the name."""
        return "Status"

    @property
    def state(self) -> str:
        """Return the state."""
        return "online"

    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:check-circle"
