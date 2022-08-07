# Next attempt at a simple client for Home Assistant for the badge.team badges.

import time, wifi, ujson, nvs, display
from homebadge import hapy

class HomeBadge:
    def __init__(self):
        self.config = self.get_config()
        # Init a Home Assistant client
        self.ha = self.get_ha()

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

    def draw_header(self, card_id):
        header_size = 24
        font_size = 22
        icon_size = 24
        header_fg_color = 0xffffff
        header_bg_color = 0x049cdb
        # draw the header background as a filled rectangle.
        display.drawRect(0,0,display.width(),header_size, True, header_bg_color)
        display.drawPng(0,0,"/sd/apps/python/homebadge/icons/menu.png")
        display.drawPng(display.width() - 2 * icon_size, 0, "/sd/apps/python/homebadge/icons/wifi-strength-3.png")
        display.drawPng(display.width() - icon_size, 0, "/sd/apps/python/homebadge/icons/battery-low.png")

    def showcard(self, card_id):
        self.draw_header(card_id)
        # self.draw_body
        # self.draw_footer
        display.flush()


def loop():
    time.sleep(1)

# The main application
def main():
    wifi.connect()
    while not wifi.status():
        time.sleep(0.5)
        pass
    wifi.ntp()
    badge = HomeBadge()
    display.clearMatrix()
    display.drawFill(0xffffff)
    badge.showcard('home')
    while True:
        loop()

# Start the main program.
if not __name__ == "homebadge":
   main()
