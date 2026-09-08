"""Select platform for GoodWe EMS Optimizer integration."""

import logging
from typing import Any, Final

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, InverterMode, EMSMode
from .coordinator import GoodWeEMSOptimizerCoordinator

_LOGGER: Final = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select platform."""
    coordinator: GoodWeEMSOptimizerCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    entities = [
        OptimizerModeSelect(coordinator, entry),
    ]

    async_add_entities(entities)
    _LOGGER.debug("Added %d select entities", len(entities))


class GoodWeEMSOptimizerSelectBase(CoordinatorEntity, SelectEntity):
    """Base class for GoodWe EMS Optimizer select entities."""

    def __init__(
        self,
        coordinator: GoodWeEMSOptimizerCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
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
        """Return unique ID for the select entity."""
        return f"{self._entry.entry_id}_optimizer_mode"


class OptimizerModeSelect(GoodWeEMSOptimizerSelectBase):
    """Select entity for optimizer operating mode (future use)."""

    @property
    def name(self) -> str:
        """Return the name of the select entity."""
        return "Optimizer Mode"

    @property
    def options(self) -> list[str]:
        """Return available options."""
        return ["automatic", "manual", "disabled"]

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        # Placeholder for future mode selection
        return "automatic"

    async def async_select_option(self, option: str) -> None:
        """Handle option selection."""
        _LOGGER.info("Optimizer mode changed to: %s", option)
        # TODO: Implement mode switching logic
