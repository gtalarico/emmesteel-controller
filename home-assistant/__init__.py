"""Emmesteel Integration."""

from pyemmesteel import EmmesteelApi

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_PROXY, DOMAIN

PLATFORMS: list[Platform] = [Platform.NUMBER, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up emmesteel from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    conf_proxy = entry.data[CONF_PROXY]
    api = EmmesteelApi(conf_proxy)

    hass.data[DOMAIN][entry.entry_id] = api
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
