import tkinter as tk
import bindings

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Ultimate clicker')
    main_frame = bindings.MainFrame(root).pack()
    binding_manager = bindings.BindingManager(main_frame)
    binding_manager.add_binding()
    root.mainloop()
