"""Emmesteel Switch Entity."""

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import CMD_ON_OFF, CMD_POWER_DN, CMD_POWER_UP, CONF_PROXY, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Emmesteel switch."""
    async_add_entities([EmmesteelSwitch(hass, entry)], True)


class EmmesteelSwitch(SwitchEntity):
    """Representation of an Emmesteel towel warmer switch."""

    _attr_icon = "mdi:radiator-disabled"
    _attr_should_poll = True
    _attr_supported_features = None
    _attr_preset_modes = []

    def __init__(self, hass, entry) -> None:
        """Initialize the power level."""

        self.hass = hass

        self._api = hass.data[DOMAIN][entry.entry_id]
        self._proxy = entry.data[CONF_PROXY]

        self._name = "Emmesteel Towel Warmer Switch"
        self._attr_unique_id = f"emmesteel-switch-proxy-{self._proxy}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._proxy)},
            name=self._name,
            manufacturer="Emmesteel",
        )

        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self._is_on

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        return {"proxy": self._proxy}

    async def async_set_native_value(self, value: float) -> None:
        """Set a new power level via the UI."""
        desired_value = int(value)

        delta = desired_value - (self._native_value or 0)
        cmd = CMD_POWER_UP if delta > 0 else CMD_POWER_DN
        _LOGGER.debug(
            "Setting Emmesteel power level to: %s (current= %s)",
            desired_value,
            self._native_value,
        )

        for _ in range(abs(delta)):
            state = await self._api.send_cmd(cmd)

        self._native_value = state.level
        self.async_write_ha_state()

    async def async_power_up(self, **kwargs):
        """Increase Power."""
        _LOGGER.debug(f"Increasing power (value={self._native_value})")
        updated_state = await self._api.send_cmd(CMD_POWER_UP)
        self._is_on = updated_state.is_on
        self._native_value = updated_state.level
        self.async_write_ha_state()

    async def async_power_down(self, **kwargs):
        """Decrease Power."""
        _LOGGER.debug(f"Decreasing power (value={self._native_value})")
        updated_state = await self._api.send_cmd(CMD_POWER_DN)
        self._is_on = updated_state.is_on
        self._native_value = updated_state.level
        self.async_write_ha_state()

    async def async_toggle(self, **kwargs):
        """Toggle Towel Warmer Power."""
        _LOGGER.debug(f"Toggling power (is_on={self._is_on})")
        updated_state = await self._api.send_cmd(CMD_ON_OFF)
        self._is_on = updated_state.is_on
        self._native_value = updated_state.level
        self.async_write_ha_state()

    async def async_update(self):
        """Fetch new state data for the switch."""
        # Retrieve the current state from the device
        state = await self._api.get_state()
        self._is_on = state.is_on or False
        self._native_value = state.level or 0
        _LOGGER.info("Emmesteel towel warmer state updated: %s", state)
        _LOGGER.debug("Emmesteel towel warmer state updated: %s", state)

    async def async_turn_on(self, **kwargs):
        """Turn the towel warmer on.

        Since the API only supports toggling, we only send a toggle command if
        the current state is off.
        """
        if not self._is_on:
            _LOGGER.debug(
                "Turning on: toggling Emmesteel towel warmer because it is currently off"
            )
            await self.async_toggle(**kwargs)
        else:
            _LOGGER.debug("Requested turn on but device is already on.")

    async def async_turn_off(self, **kwargs):
        """Turn the towel warmer off.

        Since the API only supports toggling, we only send a toggle command if
        the current state is on.
        """
        if self._is_on:
            _LOGGER.debug(
                "Turning off: toggling Emmesteel towel warmer because it is currently on"
            )
            await self.async_toggle(**kwargs)
        else:
            _LOGGER.debug("Requested turn off but device is already off.")

    async def async_update(self):
        """Fetch new state data for the switch."""
        state = await self._api.get_state()
        self._is_on = state.is_on or False
        _LOGGER.debug("Emmesteel towel warmer state updated: %s", state)
