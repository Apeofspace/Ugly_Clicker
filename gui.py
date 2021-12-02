import tkinter as tk
from tkinter import ttk as ttk
import events


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # todo: add labels much later


class EventFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

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
        self.plus_button = tk.Button(self, text='Add', width=10)

        # button minus
        self.minus_button = tk.Button(self, text='Remove', width=10)

        # pack everything
        self.hk_entry.pack(side='left', padx=(10, 5))
        self.key_to_send_entry.pack(side='left', padx=5)
        self.action_cb.pack(side='left', padx=5)
        self.plus_button.pack(side='left', padx=5)
        self.minus_button.pack(side='left', padx=(5, 10))

    # def pack_self(self, *args, **kwargs):
    #     self.pack(*args, **kwargs, padx=5, pady=7)



