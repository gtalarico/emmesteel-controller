"""The emmesteel integration.

Configuration:
    ...
    switch:
    - platform: emmesteel
        proxy: 192.168.50.100

"""

import emmesteel


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# async def async_setup(hass, config):
#     """Set up the emmesteel integration."""
#     hass.data.setdefault(DOMAIN, {})
#     return True

# Config Flow
PLATFORMS: list[Platform] = [Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up emmesteel from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
