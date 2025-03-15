import tkinter as tk
import time
from tkinter import messagebox
from smart_home import SmartHome
from smart_devices import SmartPlug, SmartTV, SmartDoor
from smart_home_app import SmartHomeApp

def test_smart_home_system():
    
    print("STARTING SMART HOME SYSTEM TEST")
    
    print("\n1. Testing SmartHome initialization...")
    home = SmartHome()
    
    home.add_device(SmartPlug(50))
    home.add_device(SmartTV(10))
    home.add_device(SmartDoor())
    
    
    print(f"Initial devices in SmartHome: {len(home.devices)}")
    for i, device in enumerate(home.devices):
        print(f"  Device {i+1}: {device}")
    
    if len(home.devices) != 3:
        print("ERROR: Failed to initialize SmartHome with 3 devices!")
        return False
        
    print("\n2. Creating GUI for testing...")
    root = tk.Tk()
    app = SmartHomeApp(root)
    
    def continue_prompt(message):
        print(f"\n{message}")
        response = input("Did the test pass? (y/n): ")
        if response.lower() != 'y':
            print("Test failed based on user input.")
            return False
        return True
    
    print("\n3. Initial GUI visual inspection...")
    print("Please verify:")
    print("Window opens without errors")
    print("Device list shows 3 devices")
    print(" Buttons are visible and properly aligned")
    print("Text sizes are appropriate")
    

    print("\n4. Testing window resizing...")
    print("Please resize the window and verify:")
    print("Button text adapts to window size")
    print("Button text wraps when window is narrow")
    print(" Listbox text size changes appropriately")
    
  
    def run_interactive_tests():
      
        print("\n5. Testing 'Turn On All' functionality...")
        app.turn_on_all()
        time.sleep(1)
        if not continue_prompt("Verify all devices now show as ON in the list"):
            return
        
      
        print("\n6. Testing 'Turn Off All' functionality...")
        app.turn_off_all()
        time.sleep(1)
        if not continue_prompt("Verify all devices now show as OFF in the list"):
            return
        
      
        print("\n7. Testing 'Toggle Selected' functionality...")
        print("Please select a device in the list, then click 'Toggle Selected'")
        if not continue_prompt("Verify the selected device changed its state"):
            return
        

        print("\n8. Testing 'Edit Device' functionality...")
        print("Please select a device in the list, then click 'Edit Device'")
        print("Enter a new value when prompted")
        if not continue_prompt("Verify the device shows updated details in the list"):
            return
        
    
        print("\n9. Testing 'Add Device' functionality...")
        print("Please click 'Add Device' and follow the prompts to add a new device")
        if not continue_prompt("Verify the new device appears in the list"):
            return
        
      
        print("\n10. Testing 'Delete Selected' functionality...")
        print("Please select a device in the list, then click 'Delete Selected'")
        if not continue_prompt("Verify the device was removed from the list"):
            return
        
        
        print("\n11. Testing 'Set Max Limit' functionality...")
        print("Please click 'Set Max Limit' and enter a new value (enter a higher number like 15)")
        if not continue_prompt("Verify the max limit label was updated"):
            return
        
        print("\n12. Testing with many devices...")
        current_count = len(app.home.devices)
    
        target_count = min(10, app.home.max_limit)
        to_add = target_count - current_count
        
        if to_add > 0:
            print(f"Adding {to_add} more devices to test scrolling and display...")
            try:
                for i in range(to_add):
                    app.home.add_device(SmartPlug(i * 10))
                app.update_device_list()
                time.sleep(1)
            except ValueError as e:
                print(f"Note: {str(e)}. This is expected behavior if max limit is reached.")
                print("Please increase the max limit to continue testing with more devices.")
                print("Click 'Set Max Limit' and enter a higher value.")
                if not continue_prompt("Did you increase the max limit?"):
                    return
                
              
                print("Trying to add more devices after limit increase...")
                try:
                    for i in range(3):
                        app.home.add_device(SmartPlug(i * 15))
                    app.update_device_list()
                except ValueError:
                    print("Still hitting the limit. Continuing with current device count.")
        
        if not continue_prompt("Verify scrolling works and all devices are displayed correctly"):
            return
        
        
        print("\n13. Testing extreme window sizes...")
        print("Please resize the window to be very small, then very large")
        if not continue_prompt("Verify the UI remains usable at all sizes"):
            return
        
        print("\n=== ALL TESTS COMPLETED ===")
        print("Thank you for testing the SmartHomeApp!")
        
     
        root.after(3000, root.destroy)
    
 
    root.after(1000, run_interactive_tests)
    
  
    root.mainloop()
    
    return True

if __name__ == "__main__":
    test_smart_home_system()