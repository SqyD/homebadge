# Next attempt at a simple client for Home Assistant for the badge.team badges.

import time, wifi, ujson, nvs, display
from homebadge import hapy
from homebadge import badge_hw

class HapyHardware(hapy.HaPy):
    def __init__(self, config = dict()):
        super().__init__()
        self.config = config

    def entity_get(self, entity_id):
        if self.entity_cache_iscached(entity_id):
            entity_data = self.entity_cache[entity_id]['data']
        else:
            hw_config = self.config[entity_id]
            if entity_id in self.config:
                if "callback" in self.config[entity_id]:
                    callback = getattr(badge_hw, self.config[entity_id]["callback"])
                    entity_data = callback(hw_config)
                    self.entity_cache_set(entity_id, entity_data)
        return entity_data

class HomeBadge:
    def __init__(self):
        self.config = self.get_config()
        # Init a Home Assistant client
        self.ha = self.get_ha()
        # Local hardware
        self.hw = self.get_hw()

    def get_config(self):
        # Read default configuration from file
        config_file = open("/sd/apps/python/homebadge/default-config.json", "r")
        config_json = config_file.read()
        config_file.close()
        return ujson.loads(config_json)

    def get_ha(self):
        # Load the secrets from nvs
        secrets = ujson.loads(nvs.nvs_getstr('homebadge', 'secrets'))
        ha = hapy.HaPyRest(secrets)
        return ha

    def get_hw(self):
        config = self.config["hardware"]
        hw = HapyHardware(config)
        return hw

    def hwtoha(self):
        for entity in self.config['hardware']:
            if self.config['hardware'][entity]['enabled']:
                if 'ha_entity_id' in self.config['hardware'][entity]:
                    entity_data = self.entity_get(entity)
                    response = self.ha.entity_set(self.config['hardware'][entity]['ha_entity_id'], entity_data)


    def entity_get(self, entity_id):
        # Local hardware entities:
        if entity_id.startswith("badge"):
            entity_data = self.hw.entity_get(entity_id)
        else:
            # Home Assistant managed entities:
            entity_data = self.ha.entity_get(entity_id)
        return entity_data

    def entity_get_state(self, entity_id):
        if entity_id.startswith("badge"):
            entity_state = self.hw.entity_get_state(entity_id)
        else:
            # Home Assistant managed entities:
            entity_state = self.ha.entity_get_state(entity_id)
        return entity_state

    def entity_get_attr(self, entity_id, attr):
        if entity_id.startswith("badge"):
            entity_attr = self.hw.entity_get_attr(entity_id, attr)
        else:
            # Home Assistant managed entities:
            entity_attr = self.ha.entity_get_attr(entity_id, attr)
        return entity_attr

    def entity_get_name(self, entity_id):
        friendly_name = self.entity_get_attr(entity_id, 'friendly_name')
        if friendly_name:
            name = friendly_name
        else:
            if entity_id.startswith('badge.'):
                name = entity_id.split(".")[2]
            else:
                name = entity_id.split(".")[1]
            words = name.split("_")
            for i in range(len(words)):
                words[i] = words[i][:1].upper() + words[i][1:].lower()
            name = " ".join(words)
        return name

    def entity_get_icon(self, entity_id):
        # First check if the entity has a specific icon configured.
        entity_icon = self.entity_get_attr(entity_id, "icon")
        # if not entity_icon:
            #entity_domain =
            # entity_icon = entity_get_icon_default(entity_domain, device_class = '')
        if entity_icon.startswith("mdi:"):
            entity_icon = entity_icon[4:]
        return entity_icon

    def draw_icon(self, x, y, name, size, color = 0x000000):
        # print("color: " + hex(color).zfill(6))
        icon_file = self.config['icons']['file'].replace("%color%", str.format('{:06x}', color)) # hex(color)[2:])
        print("icon file: " + icon_file)
        icon_file = icon_file.replace("%size%", str(size))
        icon_file = icon_file.replace("%name%", name)
        icon_file = self.config['icons']['path'] + icon_file
        display.drawPng(x, y, icon_file)

    def draw_entity_icon(self, x, y, entity_id, size, color = 0x000000):
        entity_icon = self.entity_get_icon(entity_id)
        self.draw_icon(x, y, entity_icon, size, color)

    def draw_header(self, card_id):
        header_size = 24
        font_size = 22
        icon_size = 24
        header_fg_color = 0xffffff
        header_bg_color = 0x049cdb
        # draw the header background as a filled rectangle.
        display.drawRect(0,0,display.width(),header_size, True, header_bg_color)
        # display.drawPng(0,0,"/sd/apps/python/homebadge/icons/menu.png")
        self.draw_icon(0,0, "menu", 24, 0xffffff)
        display.drawPng(display.width() - 2 * icon_size, 0, "/sd/apps/python/homebadge/icons/wifi-strength-3.png")
        # display.drawPng(display.width() - icon_size, 0, "/sd/apps/python/homebadge/icons/battery-low.png")
        self.draw_entity_icon(display.width() - icon_size, 0, "badge.sensor.power", 24, color = 0xffffff)

    def draw_card(self, x, y, width, height, card_id):
        card_type = self.config['cards'][card_id]['type']
        callback = getattr(badge, self.config['card_types'][card_type]['draw_callback'])
        navigation = callback(x, y, width, height, card_id)
        # return naviation

    def draw_card_entity(self, x, y, width, height, card_id):
        if 'name' in self.config['cards'][card_id]:
            name = self.config['cards'][card_id]['name']
        else:
            name = self.get_name(self.config['cards'][card_id]['entity'])
        name_color = int(self.config['styles']['default']['secondary-text-color'])
        font_size = self.config['styles']['default']['font-size']
        #fits = false
        # while not fits:
            #text_width = display.getTextWidth(name, self.config['styles']['default']['font'] + self.config['styles']['default']['font-size'])]
            # if text_width +
        display.drawText(
            x + font_size,
            y + font_size,
            name,
            name_color,
            'roboto_regular18'
            # font = self.config['styles']['default']['font'] + "22" # + str(self.config['styles']['default']['font-size'])
            )

        self.draw_entity_icon(
            x + width - font_size - 48,
            y + font_size,
            self.config['cards'][card_id]['entity'],
            48,
            color = 0x000000
        )



    def showcard(self, card_id):
        self.draw_header(card_id)
        self.draw_card(
            0,
            self.config['styles']['default']['header-height'],
            display.width(),
            (display.height() - (2 * self.config['styles']['default']['header-height'])),
            card_id
            )
        # self.draw_body
        # self.draw_footer
        display.flush()


def loop():
    # battery_data = badge.entity_get('badge.sensor.power')
    # response = badge.ha.entity_set('sensor.badge_power', battery_data)
    badge.hwtoha()
    display.drawFill(0xffffff)
    badge.showcard('power')
    time.sleep(60)

# The main application
def main():
    wifi.connect()
    while not wifi.status():
        time.sleep(0.5)
        pass
    wifi.ntp()
    global badge
    badge = HomeBadge()
    display.clearMatrix()
    while True:
        loop()

# Start the main program.
if not __name__ == "homebadge":
   main()
