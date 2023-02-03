# Clock Drift Sensor

This integration creates a `sensor` entity that indicates any drift between the system's
real-time clock (i.e., `time.time()`, which is used by `now()`) and Home Assistant's
timebase (i.e., `hass.loop.time()`, which is normally `time.monotonic()`) that is used
to schedule time-based events (such as `time` triggers.)

Follow the [installation](#installation) instructions below.
Then, after restarting Home Assistant, add the desired configuration and restart Home Assistant once more. Here is an example of a typical configuration:

```yaml
clock_drift:
```

## Installation
### Manual

Place a copy of:

[`__init__.py`](custom_components/clock_drift/__init__.py) at `<config>/custom_components/clock_drift/__init__.py`  
[`manifest.json`](custom_components/clock_drift/manifest.json) at `<config>/custom_components/clock_drift/manifest.json`

where `<config>` is your Home Assistant configuration directory.

>__NOTE__: Do not download the file by using the link above directly. Rather, click on it, then on the page that comes up use the `Raw` button.
