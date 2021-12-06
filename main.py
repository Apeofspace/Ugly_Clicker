import tkinter as tk
import events

#todo: rename Event and EventFrame to something more suitable

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Ultimate clicker')
    main_frame = events.MainFrame(root).pack()
    event_manager = events.EventManager(main_frame)
    event_manager.add_event()
    root.mainloop()
