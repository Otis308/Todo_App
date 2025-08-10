        for F in (HomeFrame, EditorFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew")
        
        create_menu(self, self.frames, self.show_frame)

        self.show_frame(HomeFrame)