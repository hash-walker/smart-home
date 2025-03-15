class SmartDeviceBase:
    def __init__(self, option):
        if option not in self._valid_range():
            raise ValueError(f"The {self._option_label()} is {option}, which is not valid {self._valid_range_str()}")
        
        self.switch_on = False
        self.option = option

    @property
    def option(self):
        return self._option
    
    @option.setter
    def option(self, value):
        if value not in self._valid_range():
            raise ValueError(f"The {self._option_label()} is {value}, which is not valid {self._valid_range_str()}")
        
        self._option = value

    def toggle_switch(self):
        self.switch_on = not self.switch_on
    
    def __str__(self):
        device_status = "on" if self.switch_on else "off"

        return f"{self.__class__.__name__} is {device_status} with {self._option_label()} {self.option}"
    
    
    def _valid_range(self):
        raise NotImplementedError

    def _valid_range_str(self):
        raise NotImplementedError
    
    def _option_label(self):
        raise NotImplementedError

class SmartPlug(SmartDeviceBase):
    def __init__(self, consumption_rate: int):
        super().__init__(consumption_rate)
    
    @property 
    def consumption_rate(self):
        return self.option
    
    @consumption_rate.setter
    def consumption_rate(self, value):
        self.option = value

    def _valid_range(self):
        return range(0, 151)

    def _valid_range_str(self):
        return f"(0 - 150)"
    
    def _option_label(self):
        return "consumption rate"
        
            

def test_smart_plug():
    
    try:

        print("\n Testing the Smart Plug")
        
        smart_plug = SmartPlug(45)
        print(smart_plug)

        smart_plug.toggle_switch()
        print(smart_plug)

        smart_plug.consumption_rate = 75
        print(smart_plug)

        smart_plug.toggle_switch()
        print(smart_plug)

        print("\nTest Invalid Inputs")

        try:
            smart_plug.consumption_rate = -10
        except Exception as e:
            print(f"Invalid Input: {str(e)}")
        
        try:
            smart_plug.consumption_rate = 200
        except Exception as e:
            print(f"Invalid Input: {str(e)}")
        
        print("\nPrinting the SmartPlug object to show that consumption rate is not being changed")
        print(smart_plug)

        print("\nTest Invalid init")

        try:
            SmartPlug(-5)
        except Exception as e:
            print(f"Invalid init : {str(e)}")
        
        try:
            SmartPlug(160)
        except Exception as e:
            print(f"Invalid init: {str(e)}")

    
    except Exception as e:
        print(f"Test failed: {str(e)}")

class SmartTV(SmartDeviceBase):
    def __init__(self, channel : int = 1):
        super().__init__(channel)

    @property
    def channel(self):
        return self.option
    
    @channel.setter
    def channel(self, value):
        self.option = value
    
    def _valid_range(self):
        return range(1, 735)
    
    def _valid_range_str(self):
        return f"(1 - 734)"
    
    def _option_label(self):
        return "channel"
    
class SmartDoor(SmartDeviceBase):
    def __init__(self, locked : bool = True):
        super().__init__(locked)

    @property
    def locked(self):
        return self.option
    
    @locked.setter
    def locked(self, value):
        self.option = value
    
    def _valid_range(self):
        return [True, False]
    
    def _valid_range_str(self):
        return f"True or False"
    
    def _option_label(self):
        return "locked"

def test_custom_device():
    
    try:

        print("\n Testing the SmartTV and SmartDoor classes")
        
        smart_tv = SmartTV(45)
        smart_door = SmartDoor(False)
        print(smart_tv)
        print(smart_door)

        smart_tv.toggle_switch()
        smart_door.toggle_switch()
        print(smart_tv)
        print(smart_door)

        smart_tv.channel = 75
        smart_door.locked = True
        print(smart_tv)
        print(smart_door)

        smart_tv.toggle_switch()
        smart_door.toggle_switch()
        print(smart_tv)
        print(smart_door)

        print("\nTest Invalid Inputs")

        try:
            smart_tv.channel = -10
            smart_door.locked = "yes"
        except Exception as e:
            print(f"Invalid Input: {str(e)}")

        try:
            smart_door.locked = "yes"
        except Exception as e:
            print(f"Invalid Input: {str(e)}")
        
        try:
            smart_tv.channel = 750
            smart_door.door = "no"
        except Exception as e:
            print(f"Invalid Input: {str(e)}")

        try:
            smart_door.door = "no"
        except Exception as e:
            print(f"Invalid Input: {str(e)}")
        
        print("\nObject not changed")
        print(smart_tv)

        print("\nObject not changed")
        print(smart_door)

        print("\nTest Invalid init")

        try:
            SmartTV(-5)
        except Exception as e:
            print(f"Invalid init : {str(e)}")
        
        try:
            SmartTV(735)
        except Exception as e:
            print(f"Invalid init: {str(e)}")

        try:
            SmartDoor(-5)
        except Exception as e:
            print(f"Invalid init : {str(e)}")
        
        try:
            SmartDoor(735)
        except Exception as e:
            print(f"Invalid init: {str(e)}")

    
    except Exception as e:
        print(f"Test failed: {str(e)}")


if __name__ == "__main__":
    test_smart_plug()
    test_custom_device()







        
