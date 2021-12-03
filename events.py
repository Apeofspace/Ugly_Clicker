import tkinter as tk
import tkinter.ttk as ttk


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # todo: add labels much later


class EventManager:
    def __init__(self, parent_window):
        self.event_list = []
        self.parent_window = parent_window
        self.event_counter = 0

    def add_event(self):
        self.event_counter += 1
        self.event_list.append(EventFrame(self.parent_window, self, self.event_counter))

    def remove_event(self, event_index):
        self.event_list[event_index].pack_forget()
        del self.event_list[event_index]
        self.redraw_event_frames()

    def redraw_event_frames(self):
        for event_frame in self.event_list:
            event_frame.pack(padx=5, pady=10)


class EventFrame(tk.Frame):
    def __init__(self, parent_window, event_manager, event_index, *args, **kwargs):
        tk.Frame.__init__(self, parent_window, *args, **kwargs)

        self.event_index = event_index

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

        # pack everything
        self.hk_entry.pack(side='left', padx=(10, 5))
        self.key_to_send_entry.pack(side='left', padx=5)
        self.action_cb.pack(side='left', padx=5)
        self.plus_button.pack(side='left', padx=5)
        self.minus_button.pack(side='left', padx=(5, 10))
        self.pack(padx=5, pady=10)
