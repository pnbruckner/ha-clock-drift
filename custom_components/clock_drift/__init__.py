"""File Permissions."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
import time

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, UnitOfTime
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.event import async_call_later, async_track_time_interval
from homeassistant.helpers.typing import ConfigType

INTERVAL = timedelta(minutes=5)
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration."""
    time_func = time.time
    loop_time_func = hass.loop.time
    start_time = 0.0
    start_loop_time = 0.0

    def get_times() -> tuple[float, float]:
        """Get time from both clocks."""
        return time_func(), loop_time_func()

    @callback
    def capture_start_times(now: datetime) -> None:
        """Capture clock values."""
        nonlocal start_time, start_loop_time

        start_time, start_loop_time = get_times()

    @callback
    def update(now: datetime) -> None:
        """Create thread to update files."""
        now_time, now_loop_time = get_times()
        time_delta = now_time - start_time
        loop_time_delta = now_loop_time - start_loop_time
        drift = loop_time_delta - time_delta
        hass.states.async_set(
            "sensor.clock_drift",
            f"{drift * 1e3:0.6f}",
            {"unit_of_measurement": UnitOfTime.MILLISECONDS},
            force_update=True,
        )
        _LOGGER.info(
            "time_delta = %0.9f, loop_time_delta = %0.9f, drift = %0.9f",
            time_delta,
            loop_time_delta,
            drift,
        )

    @callback
    def first_update(now: datetime) -> None:
        """Perform first update and schedule periodic updates."""
        update(now)
        async_track_time_interval(hass, update, INTERVAL)

    @callback
    def startup(event: Event) -> None:
        """Start up sensor."""
        async_call_later(hass, 10, capture_start_times)
        async_call_later(hass, 20, capture_start_times)
        async_call_later(hass, 30, first_update)

    hass.bus.async_listen(EVENT_HOMEASSISTANT_STARTED, startup, run_immediately=True)
    return True
