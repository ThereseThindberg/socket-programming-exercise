class SmartTV:
    def __init__(self):
        self.is_on = False
        self.channels = 10
        self.current_channel = 1

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def get_status(self):
        return "ON" if self.is_on else "OFF"

    def get_channel(self):
        return self.current_channel

    def get_channels(self):
        return self.channels

    def set_channel(self, number):
        if 1 <= number <= self.channels:
            self.current_channel = number
            return True
        return False

    def get_menu(self):
        return (
            "Supported commands:\n"
            "- version\n"
            "- turn_on\n"
            "- turn_off\n"
            "- status\n"
            "- get_channel\n"
            "- get_channels\n"
            "- set_channel <number>\n"
            "- help\n"
        )
