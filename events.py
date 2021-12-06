import tkinter as tk
import tkinter.ttk as ttk
import keyboard


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # todo: add labels much later


class EventManager:
    def __init__(self, parent_window):
        self.event_list = {}
        self.parent_window = parent_window
        self.event_counter = 0
        keyboard.on_press(self.on_key_press_callback)

    def add_event(self):
        self.event_counter += 1
        self.event_list[self.event_counter] = Event(self.parent_window, self, self.event_counter)

    def remove_event(self, event_index):
        if len(self.event_list) > 1:
            self.event_list[event_index].event_frame.pack_forget()
            del self.event_list[event_index]
            self.redraw_event_frames()

    def redraw_event_frames(self):
        for event in self.event_list.values():
            event.event_frame.pack(padx=5, pady=10)

    def load_events(self):
        ...
        # todo: load temp_hk etc

    def save_event(self):
        ...

    def change_events_state(self, event_index):
        # make sure there is only one active state across all objects!
        for index, event in self.event_list.items():
            if index is not event_index:
                event.state = None

    def on_key_press_callback(self, key):
        #check which object is in an active state
        for index, event in self.event_list.items():
            if event.state is not None:
                if event.state == "ch_hotkey":
                    event.hotkey = key.name
                    event.modified = True
                    event.state = None


class Event:
    class EventFrame(tk.Frame):
        def __init__(self, parent_window, event_manager, event_index, *args, **kwargs):
            tk.Frame.__init__(self, parent_window, *args, **kwargs)

            self.event_manager = event_manager
            self.event_index = event_index
            # possible states: None, "ch_hotkey", "ch_key_to_send"..think of more

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
                                         command=lambda: EventManager.add_event(event_manager))

            # button minus
            self.minus_button = tk.Button(self, text='Remove', width=10,
                                          command=lambda: EventManager.remove_event(event_manager, self.event_index))

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
            event = self.event_manager.event_list[self.event_index]
            if event.state != "ch_hotkey":
                self.temp_hk = self.hk_entry_var.get()
                self.hk_entry_var.set('Change hotkey...')
                event.state = "ch_hotkey"
                self.event_manager.change_events_state(self.event_index)
            else:
                event.state = None

    def __init__(self, parent_window, event_manager, event_index, *args, **kwargs):
        # create a frame
        self.event_frame = self.EventFrame(parent_window, event_manager, event_index, *args, **kwargs)
        self.event_index = event_index
        self.action_type = self.event_frame.action_cb_var
        self.key_to_send = self.event_frame.key_to_send_entry_var
        self.hotkey = self.event_frame.hk_entry_var

        # properties
        self._state = None
        self._modified = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state is None:
            if not self.modified:
                self.event_frame.hk_entry_var.set(self.event_frame.temp_hk)
                # todo: needs to add default field changes for other fields
        self._state = new_state
        self.modified = False

    @property
    def modified(self):
        """This property is only true right after a field changes value"""
        return self._modified

    @modified.setter
    def modified(self, bool):
        self._modified = bool

    @property
    def key_to_send(self):
        return self.event_frame.key_to_send_entry_var

    @key_to_send.setter
    def key_to_send(self, new_key_to_send):
        self.event_frame.key_to_send_entry_var = new_key_to_send

    @property
    def hotkey(self):
        return self.event_frame.hk_entry_var

    @hotkey.setter
    def hotkey(self, new_hotkey):
        print(new_hotkey)
        self.event_frame.hk_entry_var.set(new_hotkey)

    def bind_action_to_hotkey(self):
        ...

    def action(self):
        # aka Call()
        ...



