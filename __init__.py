# Next attempt at a simple client for Home Assistant for the badge.team badges.

import time, wifi, ujson, nvs, display
from homebadge import hapy

class HomeBadge:
    def __init__(self):
        # Init a Home Assistant client
        self.ha = self.get_ha()

    def get_ha(self):
        # Get the Home Assistant URL from nvs:
        ha_url = nvs.nvs_getstr('homebadge', 'ha_url')
        # Check if we have a long lived token in nvs.
        ha_token = nvs.nvs_getstr("homebadge", "ha_token")
        ha = hapy.HAClient(ha_url, access_token = ha_token)
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
