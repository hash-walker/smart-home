import tkinter as tk
from tkinter import messagebox, simpledialog, font
from smart_home import SmartHome
from smart_devices import SmartPlug, SmartTV, SmartDoor

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home Controller")
        self.root.geometry("600x400")
        self.root.minsize(400, 300)
        
        self.default_font = font.nametofont("TkDefaultFont")
        self.list_font = font.Font(family=self.default_font.cget("family"), size=self.default_font.cget("size"))
        self.button_font = font.Font(family=self.default_font.cget("family"), size=self.default_font.cget("size"))
        
        self.home = SmartHome()
        
        self.home.add_device(SmartPlug(50))
        self.home.add_device(SmartTV(10))
        self.home.add_device(SmartDoor())
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.device_list_frame = tk.Frame(self.main_frame)
        self.device_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.device_listbox = tk.Listbox(
            self.device_list_frame, 
            yscrollcommand=lambda *args: self.scrollbar.set(*args),
            font=self.list_font
        )
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.device_list_frame, orient=tk.VERTICAL, command=self.device_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.limit_label = tk.Label(self.main_frame, text=f"Max limit of devices: {self.home.max_limit}")
        self.limit_label.pack(pady=5)
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.buttons = {}
        self.add_buttons()
        self.update_device_list()
        
        for i in range(4):
            self.button_frame.columnconfigure(i, weight=1)
        
        self.root.bind("<Configure>", self.on_window_resize)
        
        self.last_width = self.root.winfo_width()
        self.last_height = self.root.winfo_height()
    
    def on_window_resize(self, event):
 
        if event.widget == self.root:

            width_change = abs(self.last_width - event.width)
            height_change = abs(self.last_height - event.height)
            
            if width_change > 10 or height_change > 10:
                self.last_width = event.width
                self.last_height = event.height
                
              
                if event.width <= 400:
                    button_size = 8
                    list_size = 9
                
                elif event.width <= 600:
                    button_size = 9
                    list_size = 10
             
                else:
                    button_size = 10
                    list_size = 11
                
             
                self.button_font.configure(size=button_size)
                self.list_font.configure(size=list_size)
                
             
                button_width = event.width // 4 - 10  
                for button in self.buttons.values():
                    button.configure(wraplength=button_width)
    
    def add_buttons(self):
        buttons_info = [
            ("Turn On All", self.turn_on_all),
            ("Turn Off All", self.turn_off_all),
            ("Toggle Selected", self.toggle_selected),
            ("Delete Selected", self.delete_selected),
            ("Add Device", self.add_device),
            ("Edit Device", self.edit_device),
            ("Set Max Limit", self.set_max_limit)
        ]
        
        # Arrange buttons in a grid layout
        for i, (text, command) in enumerate(buttons_info):
            row = i // 4
            col = i % 4
            button = tk.Button(
                self.button_frame, 
                text=text, 
                command=command,
                font=self.button_font,
                wraplength=120  # Initial wrap length
            )
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.buttons[text] = button
    
    def update_device_list(self):
        self.device_listbox.delete(0, tk.END)
        for i, device in enumerate(self.home.devices):
            self.device_listbox.insert(tk.END, f"{i+1}. {device}")
    
    def turn_on_all(self):
        self.home.switch_all_on()
        self.update_device_list()
    
    def turn_off_all(self):
        self.home.switch_all_off()
        self.update_device_list()
    
    def toggle_selected(self):
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No device selected.")
            return
        
        index = selection[0]
        self.home.toggle_device(index)
        self.update_device_list()
    
    def delete_selected(self):
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No device selected.")
            return
        
        index = selection[0]
        del self.home.devices[index]
        self.update_device_list()
    
    def edit_device(self):
        selection = self.device_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Error", "No device selected.")
            return
        
        index = selection[0]
        device_type = self.home.devices[index].__class__.__name__
        
        if type(self.home.devices[index]) == SmartPlug:
            consumption_rate = simpledialog.askinteger("Input", "Enter new consumption rate (0-150W):", minvalue=0, maxvalue=150)
            try:
                self.home.update_option(index, consumption_rate)
                self.update_device_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        elif device_type == "SmartTV":
            channel = simpledialog.askinteger("Input", "Enter channel (1-734):", minvalue=1, maxvalue=734)
            try:
                self.home.update_option(index, channel)
                self.update_device_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        elif device_type == "SmartDoor":
            locked = simpledialog.askstring("Input", "Is the door locked? (yes/no):").lower() == "yes"
            try:
                self.home.update_option(index, locked)
                self.update_device_list()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def add_device(self):
        device_type = simpledialog.askstring("Input", "Enter device type (SmartPlug, SmartTV, SmartDoor):")
        if device_type not in ["SmartPlug", "SmartTV", "SmartDoor"]:
            messagebox.showerror("Error", "Invalid device type.")
            return
        
        if len(self.home.devices) >= self.home.max_limit:
            messagebox.showerror("Error", "Device limit reached.")
            return
        
        if device_type == "SmartPlug":
            consumption_rate = simpledialog.askinteger("Input", "Enter consumption rate (0-150W):", minvalue=0, maxvalue=150)
            device = SmartPlug(consumption_rate)
        elif device_type == "SmartTV":
            channel = simpledialog.askinteger("Input", "Enter channel (1-734):", minvalue=1, maxvalue=734)
            device = SmartTV(channel)
        else:
            locked = simpledialog.askstring("Input", "Is the door locked? (yes/no):").lower() == "yes"
            device = SmartDoor(locked)
        
        try:
            self.home.add_device(device)
            self.update_device_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def set_max_limit(self):
        new_limit = simpledialog.askinteger("Set Max Limit", "Enter new max limit:", minvalue=1)
        if new_limit:
            self.home.max_limit = new_limit
            self.limit_label.config(text=f"Max limit of devices: {self.home.max_limit}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()