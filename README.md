# Grünbeck Cloud Homeassistant Component

<p align="center">
    <a href="https://www.gruenbeck.com/" target="_blank"><img src="https://www.gruenbeck.com/typo3conf/ext/sitepackage_gruenbeck/Resources/Public/Images/gruenbeck-logo.svg" alt="Gruenbeck" /></a>
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/p0l0/hagruenbeck_cloud)](https://github.com/p0l0/hagruenbeck_cloud/releases)
![Build Pipeline](https://img.shields.io/github/actions/workflow/status/p0l0/hagruenbeck_cloud/validate.yaml)
![License](https://img.shields.io/github/license/p0l0/hagruenbeck_cloud)

![Project maintenance](https://img.shields.io/badge/maintainer-%40p0l0-blue.svg)
[![BuyMeCoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg)](https://www.buymeacoffee.com/p0l0)

Custom Component to integrate Grünbeck Cloud based Water softeners into [Home Assistant](https://www.home-assistant.io/).

**This integration will set up the following entities.**

| Platform                                     | Description                                                                                                                                  |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `sensor.<device_name>_current_flow_rate`     | Sensor showing current flow rate in m³                                                                                                       |
| `sensor.<device_name>_last_service`          | Sensor showing when last service was                                                                                                         |
| `sensor.<device_name>_next_regeneration`     | Sensor showing when next regeneration will be                                                                                                |
| `sensor.<device_name>_next_service`          | Sensor showing how many days left until next service                                                                                         |
| `sensor.<device_name>_raw_water`             | Sensor showing configured raw water value                                                                                                    |
| `sensor.<device_name>_regeneration_counter`  | Sensor showing current regeneration counter                                                                                                  |
| `sensor.<device_name>_remaining_capacity`    | Sensor showing remaining salt capacity in %                                                                                                  |
| `sensor.<device_name>_remaining_capacity_m3` | Sensor showing remaining salt capacity in m³                                                                                                 |
| `sensor.<device_name>_salt_consumption`      | Sensor showing current salt consumption in kg<br /><br />The `daily_usage` attribute contains the salt usage of the last 3 days              |
| `sensor.<device_name>_salt_range`            | Sensor showing how many days left until salt is empty (SD18 does not support it, and returns 999)                                            |
| `sensor.<device_name>_soft_water_quantity`   | Sensor showing current soft water quantity in liters<br /><br />The `daily_usage` attribute contains the soft water usage of the last 3 days |
| `sensor.<device_name>_startup`               | Sensor showing start-up date                                                                                                                 |
| `binary_sensor.<device_name>_has_error`      | Binary sensor showing if we have an error or not<br /><br />The `errors` attribute contains error history                                    |
| `select.<device_name>_operation_mode`        | Select sensor to change the operation mode                                                                                                   |

 _(*) Entity names are using translation, that means they will have a different name if you are not using english._

**This integration provides following services.**

| Service                       | Description                                                           | Fields                                                                                                    |
|-------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| change_settings               | Changes the setting for the water softener.                           | `parameter`: The name of the parameter, see xxx for available parameter.<br/>`value`: New value to be set |
| get_device_salt_measurements  | Returns a list with the salt measurement for each day, since startup  | None                                                                                                      |
| get_device_water_measurements | Returns a list with the water measurement for each day, since startup | None                                                                                                      |
| regenerate                    | Starts a manual regeneration                                          | None                                                                                                      |


# Installation
## HACS (Recommended)
This is currently not an official HACS integration and repository needs to be added to HACS.

Assuming you have already installed and configured HACS, follow these steps:

1. Navigate to the HACS integrations page
2. Choose Integrations under HACS
3. Click on the three small dots in the upper right corner and select `Custom repositories` and add this URL:
```bash
https://github.com/p0l0/hagruenbeck_cloud/
```
4. Click the '+' button on the bottom of the page
5. Search for "Grünbeck Cloud", choose it, and click install in HACS
6. Ready! Now continue with the configuration.

# Configuration

## Through the interface
1. Navigate to `Settings > Devices & Services` and then click `Add Integration`
2. Search for `Grünbeck Cloud`
4. Enter your credentials for the Grünbeck Cloud

## Energy/Water Dashboard

To get the real water consumption (at least for most people in Germany), you need to create a template sensor with following calculation (you need to change the sensors with your entity names):

```yaml
template:
  - sensor:
      - name: "Current Water Usage"
        unit_of_measurement: L
        icon: mdi:water-pump
        state_class: total_increasing
        device_class: water
        state: >
          {%- set soft_water = states('sensor.<device_name>_soft_water') | float(0) -%}
          {%- set raw_water = states('sensor.<device_name>_raw_water') | float(0) -%}
          {%- set soft_water_quantity = states('sensor.<device_name>_soft_water_quantity') | float(0) -%}
          {%- if (is_number(soft_water_quantity) and (soft_water_quantity > 1)) and (is_number(raw_water) and (raw_water > 1)) and (is_number(soft_water) and (soft_water > 1)) -%}
            {%- set water_usage = ((soft_water*soft_water_quantity)/(raw_water-soft_water)+soft_water_quantity) | round(4) | float(unavailable) -%}
            {%- if is_number(water_usage) -%}
              {{water_usage}}
            {%- endif -%}
          {%- endif -%}
```

The sensor `sensor.<device_name>_soft_water_quantity` is not being pushed regularly via WebSocket, and to avoid overloading the Grünbeck Cloud API, this sensor will only be updated every 360 seconds.

If you get an error about missing statistics, it's because the entity needs to collect some data, it will be gone after a while.

__REMEMBER__: _Entity names are using translation, that means they will have a different name if you are not using english._

# LED Ring

If you have a Grünbeck model with LED Ring, the communication between integration and Grünbeck cloud is considered as "operation by user". You should change the configuration of the ring, to only be active _in case of failure_, to avoid permanent light on.

# Known Issues

If you change the operation mode and nothing changes, check if the App shows the message _"The mode of operation will be changed after next regeneration"_ when you try to change the operation mode there. I currently was not able to find out how to identify this state.

Water hardness unit is currently hardcoded to be shown in HA as °dH, but it's only a suffix nothing is being recalculated if you have a different unit in your installation. 

# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [Grünbeck](https://www.gruenbeck.com/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.
