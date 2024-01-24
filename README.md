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

| Platform                                     | Description                                                                                  |
|----------------------------------------------|----------------------------------------------------------------------------------------------|
| `sensor.<device_name>_current_flow_rate`     | Sensor showing current flow rate in m³                                                       |
| `sensor.<device_name>_last_service`          | Sensor showing when last service was                                                         |
| `sensor.<device_name>_next_regeneration`     | Sensor showing when next regeneration will be                                                |
| `sensor.<device_name>_next_service`          | Sensor showing how many days left until next service                                         |
| `sensor.<device_name>_raw_water`             | Sensor showing configured raw water value                                                    |
| `sensor.<device_name>_regeneration_counter`  | Sensor showing current regeneration counter                                                  |
| `sensor.<device_name>_remaining_capacity`    | Sensor showing remaining salt capacity in %                                                  |
| `sensor.<device_name>_remaining_capacity_m3` | Sensor showing remaining salt capacity in m³                                                 |
| `sensor.<device_name>_salt_consumption`      | Sensor showing current salt consumption in kg                                                |
| `sensor.<device_name>_salt_range`            | Sensor showing how many days left until salt is empty (SD18 does not support it, and returns 999) |
| `sensor.<device_name>_soft_water_quantity`   | Sensor showing current soft water quantity in liters                                         |
| `sensor.<device_name>_startup`               | Sensor showing start-up date                                                                 |

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
      - name: "Total Water Usage"
        unit_of_measurement: L
        state_class: total_increasing
        device_class: water
        state: >
          {%- set soft_water = states('sensor.<device_name>_soft_water')|float(0) -%}
          {%- set raw_water = states('sensor.<device_name>_raw_water')|float(0) -%}
          {%- set soft_water_quantity = states('sensor.<device_name>_soft_water_quantity')|float(0) -%}
          {%- if (is_number(soft_water_quantity) and (soft_water_quantity > 1)) and (is_number(raw_water) and (raw_water > 1)) and (is_number(soft_water) and (soft_water > 1)) -%}
            {%- set water_usage = ((soft_water*soft_water_quantity)/(raw_water-soft_water)+soft_water_quantity)|round(4) | float(unavailable) -%}
          {%- endif -%}
          {%- if is_number(water_usage) -%}
              {{water_usage}}
          {%- endif -%}

```

The sensor `sensor.<device_name>_soft_water_quantity` is not being pushed regularly via WebSocket, and to avoid overloading the Grünbeck Cloud API, this sensor will only be updated every 360 seconds.

If you get an error about missing statistics, it's because the entity needs to collect some data, it will be gone after a while.

# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [Grünbeck](https://www.gruenbeck.com/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.
