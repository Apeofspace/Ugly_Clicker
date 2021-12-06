import tkinter as tk
import tkinter.ttk as ttk
import keyboard


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # todo: add labels much later


class BindingManager:
    def __init__(self, parent_window):
        self.binding_list = {}
        self.parent_window = parent_window
        self.binding_counter = 0
        keyboard.on_press(self.on_key_press_callback)

    def add_binding(self):
        self.binding_counter += 1
        self.binding_list[self.binding_counter] = Binding(self.parent_window, self, self.binding_counter)

    def remove_binding(self, binding_index):
        if len(self.binding_list) > 1:
            self.binding_list[binding_index].binding_frame.pack_forget()
            del self.binding_list[binding_index]
            self.redraw_binding_frames()

    def redraw_binding_frames(self):
        for binding in self.binding_list.values():
            binding.binding_frame.pack(padx=5, pady=10)

    def load_bindings(self):
        ...
        # todo: load temp_hk etc

    def save_event(self):
        ...

    def force_inactive_states(self):
        # make sure there is only one active state across all objects!
        for index, binding in self.binding_list.items():
            if binding.state == "ch_hotkey":
                binding.hotkey = binding.temp_hk
            else:
                binding.state = None

    def on_key_press_callback(self, key):
        # check which object is in an active state
        for index, binding in self.binding_list.items():
            if binding.state is not None:
                if binding.state == "ch_hotkey":
                    print(f"key name = {key.name}")
                    if key.name == "esc":
                        binding.hotkey = binding.binding_frame.temp_hk
                        binding.state = None
                    else:
                        binding.hotkey = key.name
                        # binding.state = "modified"
                        binding.state = None


class Binding:
    class BindingFrame(tk.Frame):
        def __init__(self, parent_window, binding_manager, binding_index, *args, **kwargs):
            tk.Frame.__init__(self, parent_window, *args, **kwargs)

            self.binding_manager = binding_manager
            self.binding_index = binding_index
            # possible states: None, "ch_hotkey", "ch_key_to_send", "modified..think of more

            # defaults
            self.temp_hk = ''

            # entry hotkey
            self.hk_entry_var = tk.StringVar()
            self.hk_entry = tk.Entry(self, textvariable=self.hk_entry_var)
            self.hk_entry['state'] = 'readonly'

            # entry key to send
            self.key_to_send_entry_var = tk.StringVar()
            self.key_to_send_entry = tk.Entry(self, textvariable=self.key_to_send_entry_var)
            self.key_to_send_entry['state'] = 'readonly'

            # combobox to choose action
            self.action_cb_var = tk.StringVar()
            self.action_cb = ttk.Combobox(self, textvariable=self.action_cb_var)
            self.action_cb['values'] = ["Continuous", "1 sec delay", "2 sec delay"]
            self.action_cb['state'] = 'readonly'
            self.action_cb.set(self.action_cb['values'][0])

            # button plus
            self.plus_button = tk.Button(self, text='Add', width=10,
                                         command=lambda: BindingManager.add_binding(binding_manager))

            # button minus
            self.minus_button = tk.Button(self, text='Remove', width=10,
                                          command=lambda: BindingManager.remove_binding(binding_manager,
                                                                                        self.binding_index))

            # CALLBACKS
            self.hk_entry.bind('<Button-1>', self.hk_entry_focus_callback)


            # pack everything
            self.hk_entry.pack(side='left', padx=(10, 5))
            self.key_to_send_entry.pack(side='left', padx=5)
            self.action_cb.pack(side='left', padx=5)
            self.plus_button.pack(side='left', padx=5)
            self.minus_button.pack(side='left', padx=(5, 10))
            self.pack(padx=5, pady=10)

        def hk_entry_focus_callback(self, mouse_pointer):
            binding = self.binding_manager.binding_list[self.binding_index]
            print(f'Gain focis callback. state = {binding.state}')
            if binding.state != "ch_hotkey":
                # self.temp_hk = self.hk_entry_var.get()
                self.temp_hk = binding.hotkey
                # self.hk_entry_var.set('<ESC to cancel>')
                self.binding_manager.force_inactive_states()
                binding.hotkey = '<ESC to cancel>'
                binding.state = "ch_hotkey"

            # else: # todo: here can be problems when i add mouse binding
            #     binding.state = None

    def __init__(self, parent_window, binding_manager, binding_index, *args, **kwargs):
        # create a frame
        self.binding_frame = self.BindingFrame(parent_window, binding_manager, binding_index, *args, **kwargs)
        self.event_index = binding_index
        self.action_type = self.binding_frame.action_cb_var.get()
        self.key_to_send = self.binding_frame.key_to_send_entry_var.get()
        self.hotkey = self.binding_frame.hk_entry_var.get()

        # properties
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        # if new_state is None:
        #     if not self.modified:
        #         self.event_frame.hk_entry_var.set(self.event_frame.temp_hk)
        #         # todo: needs to add default field changes for other fields
        self._state = new_state

    @property
    def key_to_send(self):
        return self.binding_frame.key_to_send_entry_var.get()

    @key_to_send.setter
    def key_to_send(self, new_key_to_send):
        self.binding_frame.key_to_send_entry_var.set(new_key_to_send)

    @property
    def hotkey(self):
        return self.binding_frame.hk_entry_var.get()

    @hotkey.setter
    def hotkey(self, new_hotkey):
        print(f'set hotkey to {new_hotkey}')
        self.binding_frame.hk_entry_var.set(new_hotkey)

    def bind_action_to_hotkey(self):
        ...

    def action(self):
        # aka Call()
        ...
