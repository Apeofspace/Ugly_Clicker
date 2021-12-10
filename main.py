import bindings

if __name__ == '__main__':
    main_frame = bindings.MainFrame()
    main_frame.resizable(False, False)
    main_frame.title('Ugly AF clicker')
    binding_manager = bindings.BindingManager(master=main_frame)
    binding_manager.load_bindings()
    main_frame.mainloop()
