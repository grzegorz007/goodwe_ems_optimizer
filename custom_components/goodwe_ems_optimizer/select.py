"""Select platform for GoodWe EMS Optimizer integration."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_OPTIMIZER_MODE,
    ATTR_REQUESTED_EMS_MODE,
    ATTR_REQUESTED_INVERTER_MODE,
    DOMAIN,
    EMS_MODE_OPTIONS,
    INVERTER_MODE_OPTIONS,
    OPTIMIZER_MODE_OPTIONS,
)
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

    async_add_entities(
        [
            GoodWeEMSOptimizerSelect(
                coordinator,
                entry,
                ATTR_OPTIMIZER_MODE,
                "Optimizer Mode",
                OPTIMIZER_MODE_OPTIONS,
            ),
            GoodWeEMSOptimizerSelect(
                coordinator,
                entry,
                ATTR_REQUESTED_INVERTER_MODE,
                "Requested Inverter Mode",
                INVERTER_MODE_OPTIONS,
            ),
            GoodWeEMSOptimizerSelect(
                coordinator,
                entry,
                ATTR_REQUESTED_EMS_MODE,
                "Requested EMS Mode",
                EMS_MODE_OPTIONS,
            ),
        ]
    )


class GoodWeEMSOptimizerSelect(
    CoordinatorEntity[GoodWeEMSOptimizerCoordinator], SelectEntity, RestoreEntity
):
    """Stateful select entity used as an automation control input."""

    def __init__(
        self,
        coordinator: GoodWeEMSOptimizerCoordinator,
        entry: ConfigEntry,
        control_key: str,
        name: str,
        options: list[str],
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._control_key = control_key
        self._attr_name = name
        self._attr_options = options
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "GoodWe EMS Optimizer",
            "model": "Automation Control Surface",
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID for the select entity."""
        return f"{self._entry.entry_id}_{self._control_key}"

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        return self.coordinator.get_control_value(self._control_key)

    async def async_added_to_hass(self) -> None:
        """Restore the last selected option."""
        await super().async_added_to_hass()
        if last_state := await self.async_get_last_state():
            if last_state.state in self.options:
                self.coordinator.set_control_value(
                    self._control_key,
                    last_state.state,
                    record_action=False,
                )
                self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Store the selected option as user automation intent."""
        if option not in self.options:
            raise ValueError(f"Invalid option for {self.entity_id}: {option}")

        self.coordinator.set_control_value(self._control_key, option)
        self.async_write_ha_state()
        _LOGGER.debug("%s updated to %s", self.entity_id, option)
