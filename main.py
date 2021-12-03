import keyboard
import threading
import tkinter as tk
import events
from time import sleep


# TODO:
# 1) decorator to register events. list with events
# 2) show events on form. def update_events
# 3) buttons on form to delete and add events
# 4) modifier (also default modifier like ctrl) to start event
# 5) possibly record macro thing
# 6) each event is a class with a method
# 7) GUI is a class with a method to register events
# 8) Save events as functions using partial, or as classes with method Call. Should be class because then I can change
#           parameters easy at an time
# 9) Each EventFrame is an object of a class, that can draw itself and self replicate with a decorator
# 10) Each EventFrame belongs to Event and is created when Event is created




if __name__ == '__main__':
    root = tk.Tk()
    main_frame = events.MainFrame(root).pack()
    event_manager = events.EventManager(main_frame)
    event_manager.add_event()
    event_manager.add_event()
    sleep(1)
    event_manager.redraw_event_frames()
    root.mainloop()
