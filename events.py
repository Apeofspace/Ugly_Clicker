from gui import EventFrame


class EventManager:
    def __init__(self, parent_window):
        self.event_list = {}
        self.parent_window = parent_window
        self.event_counter = 0

    def add_event(self):
        self.event_counter += 1
        # self.event_list.append((Event(self.parent_window), self.event_counter))
        self.event_list[self.event_counter] = Event(self.parent_window)

    def remove_event(self, event_index):
        del self.event_list[event_index]
        self.redraw_event_frames()

    def redraw_event_frames(self):
        for event in self.event_list:
            event.event_frame.pack_forget()
        for event in self.event_list:
            event.event_frame.pack(padx=5, pady=10)


class Event:
    def __init__(self, parent_window):
        self.event_frame = EventFrame(parent_window)
        self.event_frame.pack(padx=5, pady=10)
