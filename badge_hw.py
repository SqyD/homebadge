import wifi, nvs, mch22

def entity_get_power_vbat():
    battery_voltage = mch22.read_vbat()
    return battery_voltage

def entity_get_power_pbat(vbat_min = 3.4, vbat_max = 4.1):
    battery_voltage = entity_get_power_vbat()
    battery_percentage = round(((battery_voltage - vbat_min) / (vbat_max - vbat_min)) * 100)
    return battery_percentage

def entity_get_power_vusb():
    usb_voltage = mch22.read_vusb()
    return usb_voltage

def entity_get_power(config):
    entity_data = dict()
    entity_data["attributes"] = dict()
    battery_voltage = entity_get_power_vbat()
    entity_data["attributes"]["Battery Voltage"] = round(battery_voltage, 2)
    battery_percentage = entity_get_power_pbat()
    battery_icon_percentage = round(battery_percentage / 10) * 10
    entity_data["attributes"]["Battery Percentage"] = battery_percentage
    usb_voltage = entity_get_power_vusb()
    entity_data["attributes"]["USB Voltage"] = round(usb_voltage, 2)
    if battery_voltage < 0.1 and usb_voltage > 0.1:
        entity_data["state"] = "USB Powered"
        entity_data["attributes"]["icon"] = "mdi:power-plug"
    elif battery_voltage > 0.1 and usb_voltage > 0.1:
        entity_data["state"] = "Charging"
        entity_data["attributes"]["icon"] = "mdi:battery-charging-" + str(battery_icon_percentage)
    elif battery_voltage > 0.1 and usb_voltage < 0.1:
        entity_data["state"] = "Discharging"
        if battery_icon_percentage == 100:
            entity_data["attributes"]["icon"] = "mdi:battery"
        else:
            entity_data["attributes"]["icon"] = "mdi:battery-" + str(battery_icon_percentage)
    return entity_data

def entity_get_power_battery(config):
    entity_data = entity_get_power(config)
    entity_data["state"] = entity_data["attributes"]["Battery Percentage"]
    entity_data["attributes"]["device_class"] = "battery"
    entity_data["attributes"]["unit_of_measurement"] =  "%"
    entity_data["attributes"]["state_class"] = "measurement"
    return entity_data

def entity_get_wifi(config):
    entity_data = dict()
    entity_data["attributes"] = dict()
    entity_data["attributes"]["device_class"] = "connectivity"
    connected = wifi.status()
    if connected:
        # entity_data["state"] = "Connected to " + wifi._DEFAULT_SSID
        entity_data["state"] = "on"
        entity_data["attributes"]["Wifi Network"] = wifi._DEFAULT_SSID
        signal_strength = wifi._STA_IF.status('rssi')
        entity_data["attributes"]["Signal Strength"] = signal_strength
        ifconfig = wifi.ifconfig()
        entity_data["attributes"]["IP Address"] = ifconfig[0]
        if signal_strength < -80:
            entity_data["attributes"]["icon"] = "mdi:wifi-strength-1"
        elif signal_strength < -60:
            entity_data["attributes"]["icon"] = "mdi:wifi-strength-2"
        elif signal_strength < -40:
            entity_data["attributes"]["icon"] = "mdi:wifi-strength-3"
        else:
            entity_data["attributes"]["icon"] = "mdi:wifi-strength-4"
    else:
        entity_data["state"] = "off"
        entity_data["attributes"]["icon"] = "mdi:wifi-off"
    return entity_data

def entity_get_nickname(config):
    entity_data = dict()
    entity_data["attributes"] = dict()
    nickname = nvs.nvs_getstr("owner", "nickname")
    entity_data["state"] = nickname
    entity_data["attributes"]["icon"] = "mdi:account-details"
    return entity_data
