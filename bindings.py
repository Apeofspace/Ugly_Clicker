import tkinter as tk
import tkinter.ttk as ttk
import keyboard


class UglyIndicator(tk.Canvas):
    def __init__(self, master, color):
        super().__init__(master, width=15, height=15, bg=color)

    def change_color(self, color):
        self.config(bg=color)


class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(fill='x', expand=True, side='top', pady=(5,0))
        self.label_hk = tk.Label(self.controls_frame, text="Hotkey shortcut").pack(side='left', padx=25)
        self.label_hk = tk.Label(self.controls_frame, text="Combination to send").pack(side='left', padx=15)
        self.label_hk = tk.Label(self.controls_frame, text="Delay").pack(side='left', padx=20)


class BindingManager:
    def __init__(self, master):
        self.binding_list = {}
        self.parent_window = master
        self.binding_counter = 0
        keyboard.hook(self.on_key_press_callback)
        self.count_keys_pressed = 0
        self.key_pressed = ''
        self.modifiers_pressed = []

    def add_binding(self, hotkey="", key_to_send="", mode_index=0):
        self.binding_counter += 1
        self.binding_list[self.binding_counter] = Binding(self.parent_window, self, self.binding_counter,
                                                          hotkey, key_to_send, mode_index)

    def remove_binding(self, binding_index):
        if len(self.binding_list) > 1:
            self.binding_list[binding_index].binding_frame.pack_forget()
            del self.binding_list[binding_index]
            self.redraw_binding_frames()

    def redraw_binding_frames(self):
        for binding in self.binding_list.values():
            binding.binding_frame.pack(side='bottom', padx=5, pady=10)

    def load_bindings(self):
        ...
        # todo: load temp_hk etc

    def save_bindings(self):
        ...

    def force_inactive_states(self):
        # make sure there is only one active state across all objects!
        self.count_keys_pressed = 0
        self.key_pressed = ''
        self.modifiers_pressed = []
        for index, binding in self.binding_list.items():
            if binding.state == "ch_hotkey":
                binding.hotkey = binding.binding_frame.temp_hk
                binding.state = None
            elif binding.state == 'ch_key_to_send':
                binding.key_to_send = binding.binding_frame.temp_hk
                binding.state = None
            elif binding.state == 'hooked':
                ...
            else:
                binding.state = None

    def on_key_press_callback(self, keyboard_event):
        for index, binding in self.binding_list.items():
            if binding.state is not None and binding.state != 'hooked':
                if binding.state == "ch_hotkey":
                    set_combination = Binding.hotkey.fset  # a way to get a reference to a property
                if binding.state == "ch_key_to_send":
                    set_combination = Binding.key_to_send.fset  # a way to get a reference to a property
                if keyboard_event.name == "esc":
                    set_combination(binding, binding.binding_frame.temp_hk)
                    binding.state = None
                else:
                    if keyboard_event.event_type == keyboard.KEY_DOWN:
                        if keyboard.is_modifier(keyboard_event.name):
                            if keyboard_event.name not in self.modifiers_pressed:
                                self.modifiers_pressed.append(keyboard_event.name)
                                if len(self.modifiers_pressed) > 2:
                                    self.modifiers_pressed.pop(0)
                                else:
                                    self.count_keys_pressed += 1
                        else:
                            self.count_keys_pressed += 1
                            self.key_pressed = keyboard_event.name

                    elif keyboard_event.event_type == keyboard.KEY_UP:
                        self.count_keys_pressed -= 1

                    current_key_combination = "+".join([*self.modifiers_pressed, self.key_pressed])
                    set_combination(binding, current_key_combination)

                    # tests
                    # print(f'modifiers = {self.modifiers_pressed}, key = {self.key_pressed}')
                    # print(f'current_key_combination = {current_key_combination}')
                    # print(f'count_keys_pressed = {self.count_keys_pressed}\n')

                    if self.count_keys_pressed == 0:
                        final_key_combination = "+".join([*self.modifiers_pressed, self.key_pressed])
                        print(f'final_key_combination = {final_key_combination}')
                        self.modifiers_pressed.clear()
                        self.key_pressed = ''
                        self.count_keys_pressed = 0
                        set_combination(binding, final_key_combination)
                        binding.state = None

                        if binding.hotkey != "" and binding.key_to_send != "":
                            binding.state = 'hooked'


class Binding:
    class BindingFrame(tk.Frame):
        def __init__(self, master, binding_manager, binding_index, *args, **kwargs):
            super().__init__(master=master, *args, **kwargs)
            self.binding_manager = binding_manager
            self.binding_index = binding_index
            # possible states: None, "ch_hotkey", "ch_key_to_send", "hooked"

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

            #ugly ass indicator
            self.ugly_indicator = UglyIndicator(self, 'red')

            # button plus
            self.plus_button = tk.Button(self, text='Add', width=10,
                                         command=lambda: BindingManager.add_binding(binding_manager))

            # button minus
            self.minus_button = tk.Button(self, text='Remove', width=10,
                                          command=lambda: BindingManager.remove_binding(binding_manager,
                                                                                        self.binding_index))

            # CALLBACKS
            self.hk_entry.bind('<Button-1>', self.hk_entry_focus_callback)
            self.key_to_send_entry.bind('<Button-1>', self.key_to_send_entry_focus_callback)

            # pack everything
            self.hk_entry.pack(side='left', padx=(10, 5))
            self.key_to_send_entry.pack(side='left', padx=5)
            self.action_cb.pack(side='left', padx=5)
            self.ugly_indicator.pack(side='left', padx=5)
            self.plus_button.pack(side='left', padx=5)
            self.minus_button.pack(side='left', padx=(5, 10))
            self.pack(side=tk.BOTTOM, padx=5, pady=10, anchor=tk.S)

        def hk_entry_focus_callback(self, mouse_pointer):
            binding = self.binding_manager.binding_list[self.binding_index]
            self.binding_manager.force_inactive_states()
            if binding.state != "ch_hotkey":
                binding.state = None
                binding.unhook()
                self.temp_hk = binding.hotkey
                binding.hotkey = '<ESC to cancel>'
                binding.state = "ch_hotkey"
            # else: # todo: here can be problems when i add mouse binding
            #     binding.state = None

        def key_to_send_entry_focus_callback(self, mouse_pointer):
            binding = self.binding_manager.binding_list[self.binding_index]
            self.binding_manager.force_inactive_states()
            if binding.state != "ch_key_to_send":
                binding.state = None
                binding.unhook()
                self.temp_hk = binding.hotkey
                binding.key_to_send = '<ESC to cancel>'
                binding.state = "ch_key_to_send"
            # else: # todo: here can be problems when i add mouse binding
            #     binding.state = None

    def __init__(self, parent_window, binding_manager, binding_index, hotkey, key_to_send, mode_index, *args, **kwargs):
        # create a frame
        self.binding_frame = self.BindingFrame(parent_window, binding_manager, binding_index, *args, **kwargs)
        self.event_index = binding_index

        # properties
        self._state = None
        self._pressed = False

        # initial values
        self.hotkey = hotkey
        self.key_to_send = key_to_send
        self.delay_mode = mode_index

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
        if new_state != 'hooked':
            self.binding_frame.ugly_indicator.change_color('red')
            self.unhook()
        if new_state == 'hooked':
            self.binding_frame.ugly_indicator.change_color('green')
            self.hook()

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
        # print(f'set hotkey to {new_hotkey}')
        self.binding_frame.hk_entry_var.set(new_hotkey)

    @property
    def delay_mode(self, by_index=False):
        if by_index:
            try:
                return self.binding_frame.action_cb.current()
            except:
                return 0
        return self.binding_frame.action_cb_var.get()

    @delay_mode.setter
    def delay_mode(self, mode):
        if isinstance(mode, int):  # if set by index
            self.binding_frame.action_cb.current(mode)
        else:  # if set by value
            self.binding_frame.action_cb_var.set(mode)

    @property
    def hotkey_active(self):
        return self._pressed

    @hotkey_active.setter
    def hotkey_active(self, value):
        """Can be True, False or 'Flip' """
        if value == 'Flip':
            self._pressed = not self._pressed
        else:
            self._pressed=value

    def hook(self):
        print(f'Hooking : {self.hotkey} to {self.key_to_send}')
        keyboard.add_hotkey(self.hotkey, self.hotkey_pressed_callback)

    def unhook(self):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except KeyError:
            print('Failed to unhook')

    def hotkey_pressed_callback(self):
        # aka Call()
        self.hotkey_active = 'Flip'
        if self.delay_mode == 'Continuous':
            if self.hotkey_active:
                print('ACTION!')
                print(self.key_to_send)
                keyboard.press(self.key_to_send)
            else:
                keyboard.release(self.key_to_send)



