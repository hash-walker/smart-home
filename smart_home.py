from smart_devices import SmartPlug, SmartTV, SmartDoor

class SmartHome:
    def __init__(self, max_limit = 5):
        self.devices = []
        self.max_limit = max_limit

    
    def add_device(self, device: object):
        if len(self.devices) < self.max_limit:
            self.devices.append(device)
        else:
            raise ValueError("Max limit reached, cannot add more devices")

    def get_device(self, index: int):

        if 0 <= index < len(self.devices):
            return self.devices[index]
        else:
            raise IndexError("Cannot get device. Index out of bound")

    def toggle_device(self, index: int):
        self.devices[index].toggle_switch()
    
    def remove_device(self, index: int):
        if 0 <= index < len(self.devices):
            del self.devices[index]
        else:
            raise IndexError("Cannot remove device. Index out of bound")
        
    def switch_all_on(self):
        for device in self.devices:
            if not device.switch_on:
                device.toggle_switch()
    
    def switch_all_off(self):
        for device in self.devices:
            if device.switch_on:
                device.toggle_switch()

    def update_option(self, index: int, value):
            device = self.get_device(index)
        
            if type(device) == SmartPlug:
                device.consumption_rate = value
            elif type(device) == SmartDoor:
                device.locked = value
            elif type(device) == SmartTV:
                device.channel = value
            else:
                raise ValueError("No such type available")
        
    
    def __str__(self):
        
        summary = [f"SmartHome with {len(self.devices)} device(s):"]

        for i, device in enumerate(self.devices):
            summary.append(f"{i+1}- {device}")

        return "\n".join(summary)
    
def test_smart_home():

    print(f"        Smart Home      \n")

    smart_plug = SmartPlug(120)
    smart_tv = SmartTV(5)
    smart_door = SmartDoor()

    home = SmartHome(max_limit = 3)

    print("\n       Adding devices to the Smart Home.....       ")

    home.add_device(smart_plug)
    home.add_device(smart_tv)
    home.add_device(smart_door)


    print("\n       Smart Home initial      ")
    print(home)

    print("\n       Device Retrieving.....      ")
    
    for i in range(0, len(home.devices)):
        print(home.get_device(i))

    print("\n       Toggle Devices individually     ")

    for i in range(0, len(home.devices)):
        home.toggle_device(i)
    
    print("\n       Check the updated Smart Home after individual toggling      ")
    print(home)

    print("\n       Switching off all the devices        ")
    home.switch_all_off()
    print(home)

    print("\n       Switching on all the devices        ")
    home.switch_all_on()
    print(home)


    print("\n       Test Max limit constraint")

    try: 
        additional_device = SmartPlug(90)
        home.add_device(additional_device)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n       Testing update function with valid values       ")
    home.update_option(0, 150)
    home.update_option(1, 10)
    home.update_option(2, False)

    print("\n       After updating devices attributes")
    print(home)

    print("\n Updating with invalid inputs      ")

    try:
        home.update_option(0, -60)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        home.update_option(1, -60)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        home.update_option(2, "yes")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n       Removing a device.....       ")
    home.remove_device(0)

    print("\n       Smart Home after device removal     ")
    print(home)

    print("\n       Invalid Removals        ")

    try:
        home.remove_device(10)
    except IndexError as i:
        print(f"Error: {i}")

    print("\n       Final State of Smart Home       ")
    print(home)

if __name__ == "__main__":
    test_smart_home()

    





     


