"""GoodWe EMS Optimizer Integration."""

import asyncio
import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, SETUP_DELAY
from .coordinator import GoodWeEMSOptimizerCoordinator

_LOGGER: Final = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "select"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the GoodWe EMS Optimizer component from YAML (legacy support)."""
    _LOGGER.debug("Setting up %s from YAML config", DOMAIN)
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GoodWe EMS Optimizer from a config entry."""
    _LOGGER.debug("Setting up %s config entry: %s", DOMAIN, entry.entry_id)

    # Initialize domain data
    hass.data.setdefault(DOMAIN, {})

    # Create and start the coordinator
    coordinator = GoodWeEMSOptimizerCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator in hass.data
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    # Forward setup to platforms with a slight delay to ensure entity registry is ready
    await asyncio.sleep(SETUP_DELAY)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_update_entry))

    _LOGGER.info("Successfully set up %s (entry_id: %s)", DOMAIN, entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading %s config entry: %s", DOMAIN, entry.entry_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        coordinator: GoodWeEMSOptimizerCoordinator = hass.data[DOMAIN][entry.entry_id][
            "coordinator"
        ]
        await coordinator.async_shutdown()
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Successfully unloaded %s (entry_id: %s)", DOMAIN, entry.entry_id)

    return unload_ok


async def async_update_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle config entry updates."""
    _LOGGER.debug("Updating config entry: %s", entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)
