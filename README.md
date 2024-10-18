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

| Platform                                                    | Description                                                                                                                                                  | Enabled by default |
|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| __Binary sensor__                                           |                                                                                                                                                              ||
| `binary_sensor.<device_name>_has_error`                     | Binary sensor showing if we have an error or not<br /><br />The `errors` attribute contains error history                                                    | :white_check_mark: |
| __Sensor__                                                  |                                                                                                                                                              ||
| `sensor.<device_name>_next_regeneration`                    | Sensor showing when next regeneration will be                                                                                                                | :white_check_mark: |
| `sensor.<device_name>_next_service`                         | Sensor showing how many days left until next service                                                                                                         | :white_check_mark: |
| `sensor.<device_name>_raw_water`                            | Sensor showing configured raw water value                                                                                                                    | :white_check_mark: |
| `sensor.<device_name>_regeneration_counter`                 | Sensor showing current regeneration counter                                                                                                                  | :white_check_mark: |
| `sensor.<device_name>_current_flow_rate`                    | Sensor showing current flow rate in m³/h                                                                                                                     | :white_check_mark: |
| `sensor.<device_name>_current_flow_rate_2`                  | Sensor showing current flow rate for Exchanger 2 in m³/h                                                                                                     | :no_entry_sign:    |
| `sensor.<device_name>_last_service`                         | Sensor showing when last service was                                                                                                                         | :white_check_mark: |
| `sensor.<device_name>_regeneration_remaining_time`          | Sensor showing the remaining amount / time of current regeneration step”                                                                                     | :white_check_mark: |
| `sensor.<device_name>_regeneration_step`                    | Sensor showing the current regeneration step                                                                                                                 | :white_check_mark: |
| `sensor.<device_name>_remaining_capacity_percentage`        | Sensor showing remaining salt capacity in %                                                                                                                  | :white_check_mark: |
| `sensor.<device_name>_remaining_capacity_percentage_2`      | Sensor showing remaining salt capacity for Exchanger 2 in %                                                                                                  | :no_entry_sign:    |
| `sensor.<device_name>_remaining_capacity_volume`            | Sensor showing remaining salt capacity in m³                                                                                                                 | :white_check_mark: |
| `sensor.<device_name>_remaining_capacity_volume_2`          | Sensor showing remaining salt capacity for Exchanger 2 in m³                                                                                                 | :no_entry_sign:    |
| `sensor.<device_name>_salt_consumption`                     | Sensor showing current salt consumption in kg<br /><br />The `daily_usage` attribute contains the salt usage of the last 3 days                              | :white_check_mark: |
| `sensor.<device_name>_salt_range`                           | Sensor showing how many days left until salt is empty (SD18 does not support it, and returns 999)                                                            | :white_check_mark: |
| `sensor.<device_name>_soft_water`                           | Sensor showing the configured soft water value                                                                                                               | :white_check_mark: |
| `sensor.<device_name>_soft_water_quantity`                  | Sensor showing current soft water quantity in liters<br /><br />The `daily_usage` attribute contains the soft water usage of the last 3 days                 | :white_check_mark: |
| `sensor.<device_name>_soft_water_quantity_2`                | Sensor showing current soft water quantity for Exchanger 2 in liters<br /><br />The `daily_usage` attribute contains the soft water usage of the last 3 days | :no_entry_sign:    |
| `sensor.<device_name>_startup`                              | Sensor showing start-up date                                                                                                                                 | :white_check_mark: |
| `sensor.<device_name>_actual_value_soft_water_hardness`     | Sensor showing the actual value for soft water hardness                                                                                                      | :no_entry_sign:    |
| `sensor.<device_name>_blending_flow_rate`                   | Sensor showing the blending flow rate                                                                                                                        | :no_entry_sign:    |
| `sensor.<device_name>_capacity_figure`                      | Sensor showing the capacity figure                                                                                                                           | :no_entry_sign:    |
| `sensor.<device_name>_current_chlorine`                     | Sensor showing the current chlorine                                                                                                                          | :no_entry_sign:    |
| `sensor.<device_name>_exchanger_peak_value`                 | Sensor showing the Exchanger peak value                                                                                                                      | :no_entry_sign:    |
| `sensor.<device_name>_exchanger_peak_value_2`               | Sensor showing the peak value for Exchanger 2                                                                                                                | :no_entry_sign:    |
| `sensor.<device_name>_exhausted_percentage`                 | Sensor showing the adsorber exhaustion in %                                                                                                                  | :no_entry_sign:    |
| `sensor.<device_name>_flow_rate_peak_value`                 | Sensor showing the flow rate peak value                                                                                                                      | :no_entry_sign:    |
| `sensor.<device_name>_last_regeneration_exchanger`          | Sensor showing the time of last regeneration for the Exchanger                                                                                               | :no_entry_sign:    |
| `sensor.<device_name>_last_regeneration_exchanger_2`        | Sensor showing the time of last regeneration for the Exchanger 2                                                                                             | :no_entry_sign:    |
| `sensor.<device_name>_make_up_water_volume`                 | Sensor showing the make-up water volume                                                                                                                      | :no_entry_sign:    |
| `sensor.<device_name>_regeneration_flow_rate_exchanger`     | Sensor showing the regeneration flow rate for Exchanger                                                                                                      | :no_entry_sign:    |
| `sensor.<device_name>_regeneration_flow_rate_exchanger_2`   | Sensor showing the regeneration flow rate for Exchanger 2                                                                                                    | :no_entry_sign:    |
| `sensor.<device_name>_remaining_amount_of_water`            | Sensor showing the adsorber remaining amount of water                                                                                                        | :no_entry_sign:    |
| `sensor.<device_name>_step_indication_regeneration_valve`   | Sensor showing the step indication regeneration for valve 1                                                                                                  | :no_entry_sign:    |
| `sensor.<device_name>_step_indication_regeneration_valve_2` | Sensor showing the step indication regeneration for valve 2                                                                                                  | :no_entry_sign:    |
| __Switch__                                                  |                                                                                                                                                              ||
| `switch.<device_name>_buzzer`                               | Activate/Deactivate audio signal on error                                                                                                                    | :white_check_mark: |
| `switch.<device_name>_dlst`                                 | Activate/Deactivate daylight saving time                                                                                                                     | :white_check_mark: |
| `switch.<device_name>_email_notification`                   | Activate/Deactivate Email Notifications                                                                                                                      | :white_check_mark: |
| `switch.<device_name>_push_notification`                    | Activate/Deactivate Push Notifications                                                                                                                       | :white_check_mark: |
| `switch.<device_name>_disinfection_monitoring`              | Activate/Deactivate disinfection monitoring<br /><br />__API returns an 500 error when trying to change__                                                    | :no_entry_sign:    |
| `switch.<device_name>_fault_signal_contact`                 | Activate/Deactivate function fault signal contact<br /><br />__API returns an 500 error when trying to change__                                              | :no_entry_sign:    |
| `switch.<device_name>_knx`                                  | Activate/Deactivate KNX connection<br /><br />__API returns an 500 error when trying to change__                                                             | :no_entry_sign:    |
| `switch.<device_name>_led_ring_flash_on_signal`             | Activate/Deactivate illuminated LED ring flashes for pre-alarm salt supply                                                                                   | :no_entry_sign:    |
| `switch.<device_name>_nominal_flow_monitoring`              | Activate/Deactivate monitoring of nominal flow<br /><br />__API returns an 500 error when trying to change__                                                 | :no_entry_sign:    |
| `switch.<device_name>_ntp_sync`                             | Activate/Deactivate getting date/time automatically (NTP)<br /><br />__API returns an 500 error when trying to change__                                      | :no_entry_sign:    |
| __Text__                                                    |                                                                                                                                                              ||
| `text.<device_name>_installer_email`                        | Set the Installer Email<br /><br />__API returns an 500 error when trying to change__                                                                        | :no_entry_sign:    |
| `text.<device_name>_installer_name`                         | Set the Installer Name<br /><br />__API returns an 500 error when trying to change__                                                                         | :no_entry_sign:    |
| `text.<device_name>_installer_phone`                        | Set the Installer Phone<br /><br />__API returns an 500 error when trying to change__                                                                        | :no_entry_sign:    |
| __Time__                                                    |                                                                                                                                                              ||
| `time.<device_name>_regeneration_time_monday_1`             | Set Regeneration Time Monday slot #1                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_monday_2`             | Set Regeneration Time Monday slot #2                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_monday_3`             | Set Regeneration Time Monday slot #3                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_tuesday_1`            | Set Regeneration Time Tuesday slot #1                                                                                                                        | :white_check_mark: |
| `time.<device_name>_regeneration_time_tuesday_2`            | Set Regeneration Time Tuesday slot #2                                                                                                                        | :white_check_mark: |
| `time.<device_name>_regeneration_time_tuesday_3`            | Set Regeneration Time Tuesday slot #3                                                                                                                        | :white_check_mark: |
| `time.<device_name>_regeneration_time_wednesday_1`          | Set Regeneration Time Wednesday slot #1                                                                                                                      | :white_check_mark: |
| `time.<device_name>_regeneration_time_wednesday_2`          | Set Regeneration Time Wednesday slot #2                                                                                                                      | :white_check_mark: |
| `time.<device_name>_regeneration_time_wednesday_3`          | Set Regeneration Time Wednesday slot #3                                                                                                                      | :white_check_mark: |
| `time.<device_name>_regeneration_time_thursday_1`           | Set Regeneration Time Thursday slot #1                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_thursday_2`           | Set Regeneration Time Thursday slot #2                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_thursday_3`           | Set Regeneration Time Thursday slot #3                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_friday_1`             | Set regeneration Time Friday slot #1                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_friday_2`             | Set Regeneration Time Friday slot #2                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_friday_3`             | Set Regeneration Time Friday slot #3                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_saturday_1`           | Set Regeneration Time Saturday slot #1                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_saturday_2`           | Set Regeneration Time Saturday slot #2                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_saturday_3`           | Set Regeneration Time Saturday slot #3                                                                                                                       | :white_check_mark: |
| `time.<device_name>_regeneration_time_sunday_1`             | Set Regeneration Time Sunday slot #1                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_sunday_2`             | Set Regeneration Time Sunday slot #2                                                                                                                         | :white_check_mark: |
| `time.<device_name>_regeneration_time_sunday_3`             | Set Regeneration Time Sunday slot #3                                                                                                                         | :white_check_mark: |
| __Number__                                                  |                                                                                                                                                              ||
| `number.<device_name>_raw_water_hardness`                   | Set the raw water hardness in °dH                                                                                                                            | :white_check_mark: |
| `number.<device_name>_soft_water_hardness`                  | Set the soft water hardness in °dH                                                                                                                           | :white_check_mark: |
| `number.<device_name>_backwash`                             | Set the backwash value in liter<br /><br />__API returns an 500 error when trying to change__                                                                | :no_entry_sign:    |
| `number.<device_name>_blending_water_meter_pulse_rate`      | Set the blending water meter pulse rate in l/Imp<br /><br />__API returns an 500 error when trying to change__                                               | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_monday`               | Set the capacity figure value for Monday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                             | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_tuesday`              | Set the capacity figure value for Tuesday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                            | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_wednesday`            | Set the capacity figure value for Wednesday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                          | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_thursday`             | Set the capacity figure value for Thursday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                           | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_friday`               | Set the capacity figure value for Friday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                             | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_saturday`             | Set the capacity figure value for Saturday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                           | :no_entry_sign:    |
| `number.<device_name>_capacity_figure_sunday`               | Set the capacity figure value for Sunday in m³x°dH<br /><br />__API returns an 500 error when trying to change__                                             | :no_entry_sign:    |
| `number.<device_name>_charge`                               | Set the charge value in mAmin<br /><br />__API returns an 500 error when trying to change__                                                                  | :no_entry_sign:    |
| `number.<device_name>_current_setpoint`                     | Set the current setpoint value in mA<br /><br />__API returns an 500 error when trying to change__                                                           | :no_entry_sign:    |
| `number.<device_name>_end_frequency_blending_valve`         | Set the end frequency blending valve value in Hz<br /><br />__API returns an 500 error when trying to change__                                               | :no_entry_sign:    |
| `number.<device_name>_end_frequency_regeneration_valve`     | Set the end frequency regeneration valve value in Hz<br /><br />__API returns an 500 error when trying to change__                                           | :no_entry_sign:    |
| `number.<device_name>_end_frequency_regeneration_valve_2`   | Set the end frequency regeneration value for valve 2 in Hz<br /><br />__API returns an 500 error when trying to change__                                     | :no_entry_sign:    |
| `number.<device_name>_interval_forced_regeneration`         | Set the interval of forced regeneration in days<br /><br />__API returns an 500 error when trying to change__                                                | :no_entry_sign:    |
| `number.<device_name>_led_ring_brightness`                  | Set the LED ring Brightness in %                                                                                                                             | :no_entry_sign:    |
| `number.<device_name>_longest_switch_on_time_chlorine_cell` | Set the longest switch-on time chlorine cell value in minutes<br /><br />__API returns an 500 error when trying to change__                                  | :no_entry_sign:    |
| `number.<device_name>_maintenance_interval`                 | Set the maintenance interval in days<br /><br />__API returns an 500 error when trying to change__                                                           | :no_entry_sign:    |
| `number.<device_name>_minimum_filling_volume_largest_cap`   | Set the minimum filling volume for largest cap in liter<br /><br />__API returns an 500 error when trying to change__                                        | :no_entry_sign:    |
| `number.<device_name>_maximum_filling_volume_largest_cap`   | Set the maximum filling volume for largest cap in liter<br /><br />__API returns an 500 error when trying to change__                                        | :no_entry_sign:    |
| `number.<device_name>_minimum_filling_volume_smallest_cap`  | Set the minimum filling volume for smallest cap in liter<br /><br />__API returns an 500 error when trying to change__                                       | :no_entry_sign:    |
| `number.<device_name>_maximum_filling_volume_smallest_cap`  | Set the maximum filling volume for smallest cap in liter<br /><br />__API returns an 500 error when trying to change__                                       | :no_entry_sign:    |
| `number.<device_name>_maximum_remaining_time_regeneration`  | Set the maximum remaining time regeneration in minutes<br /><br />__API returns an 500 error when trying to change__                                         | :no_entry_sign:    |
| `number.<device_name>_nominal_flow_rate`                    | Set the nominal flow rate value in m³/h<br /><br />__API returns an 500 error when trying to change__                                                        | :no_entry_sign:    |
| `number.<device_name>_regeneration_monitoring_time`         | Set the regeneration monitoring time in minutes<br /><br />__API returns an 500 error when trying to change__                                                | :no_entry_sign:    |
| `number.<device_name>_regeneration_water_meter_pulse_rate`  | Set the regeneration water meter pulse rate in l/Imp<br /><br />__API returns an 500 error when trying to change__                                           | :no_entry_sign:    |
| `number.<device_name>_residual_capacity_limit`              | Set the residual capacity limit value in %<br /><br />__API returns an 500 error when trying to change__                                                     | :no_entry_sign:    |
| `number.<device_name>_salting_monitoring_time`              | Set the salting monitoring time in minutes<br /><br />__API returns an 500 error when trying to change__                                                     | :no_entry_sign:    |
| `number.<device_name>_slow_rinse`                           | Set the slow rinse value in minutes<br /><br />__API returns an 500 error when trying to change__                                                            | :no_entry_sign:    |
| `number.<device_name>_soft_water_meter_pulse_rate`          | Set the soft water meter pulse rate in l/Imp<br /><br />__API returns an 500 error when trying to change__                                                   | :no_entry_sign:    |
| `number.<device_name>_treatment_volume`                     | Set the treatment volume in m³<br /><br />__API returns an 500 error when trying to change__                                                                 | :no_entry_sign:    |
| `number.<device_name>_washing_out`                          | Set the washing out value in liter<br /><br />__API returns an 500 error when trying to change__                                                             | :no_entry_sign:    |
| __Select__                                                  |                                                                                                                                                              ||
| `select.<device_name>_mode`                                 | Select sensor to change the operation mode                                                                                                                   | :white_check_mark: |
| `select.<device_name>_regeneration_mode`                    | Select sensor to change the regeneration mode                                                                                                                | :white_check_mark: |
| `select.<device_name>_water_hardness_unit`                  | Select sensor to change the water hardness unit                                                                                                              | :white_check_mark: |
| `select.<device_name>_language`                             | Select sensor to change the interface language<br /><br />__API returns an 500 error when trying to change__                                                 | :no_entry_sign:    |
| `select.<device_name>_led_ring_mode`                        | Select sensor to change the LED Ring Mode                                                                                                                    | :no_entry_sign:    |
| `select.<device_name>_mode_individual_monday`               | Select sensor to change the individual operation mode for Monday                                                                                             | :no_entry_sign:    |
| `select.<device_name>_mode_individual_tuesday`              | Select sensor to change the individual operation mode for Tuesday                                                                                            | :no_entry_sign:    |
| `select.<device_name>_mode_individual_wednesday`            | Select sensor to change the individual operation mode for Wednesday                                                                                          | :no_entry_sign:    |
| `select.<device_name>_mode_individual_thursday`             | Select sensor to change the individual operation mode for Thursday                                                                                           | :no_entry_sign:    |
| `select.<device_name>_mode_individual_friday`               | Select sensor to change the individual operation mode for Friday                                                                                             | :no_entry_sign:    |
| `select.<device_name>_mode_individual_saturday`             | Select sensor to change the individual operation mode for Saturday                                                                                           | :no_entry_sign:    |
| `select.<device_name>_mode_individual_sunday`               | Select sensor to change the individual operation mode for Sunday                                                                                             | :no_entry_sign:    |

 > [!NOTE]
 > Entity names are using translation, that means they will have a different name if you are not using english.
 
 > [!CAUTION]
 > Unfortunately some parameters can not be changed via API, it always returns an HTTP Error 500 with the error of type ‘unexpectedException’

**This integration provides following services.**

| Service                       | Description                                                           | Fields                                                                                                                                                                                                                      |
|-------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| change_settings               | Changes the setting for the water softener.                           | `parameter`: The name of the parameter, check [pygruenbeck_cloud](https://github.com/p0l0/pygruenbeck_cloud?tab=readme-ov-file#available-configuration-parameter) for available parameter.<br/>`value`: New value to be set |
| get_device_salt_measurements  | Returns a list with the salt measurement for each day, since startup  | None                                                                                                                                                                                                                        |
| get_device_water_measurements | Returns a list with the water measurement for each day, since startup | None                                                                                                                                                                                                                        |
| regenerate                    | Starts a manual regeneration                                          | None                                                                                                                                                                                                                        |


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
