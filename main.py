import tkinter as tk
import bindings

if __name__ == '__main__':
    main_frame = bindings.MainFrame()
    main_frame.resizable(False, False)
    main_frame.title('Ultimate clicker')
    binding_manager = bindings.BindingManager(master=main_frame)
    binding_manager.add_binding()
    main_frame.mainloop()
