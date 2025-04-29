import customtkinter as ctk

class CreateEventPage(ctk.CTkFrame):
    def __init__(self, master, manage_page):
        # -- Dimiourgia tou vasikou frame gia ti selida dimiourgias event -- #
        super().__init__(master, fg_color="transparent")
        self.manage_page = manage_page
        self.current_step = 0
        
        # -- Lista me ta vimata tis formas -- #
        self.steps = [
            "Basic Details",      # Title, Description, Date/Time
            "Location & Type",    # Location, Public/Private
            "Capacity & Cost",    # Max participants, Free/Paid
            "Additional Info",    # Images and Documents
            "Notifications",      # Notification settings
            "Review & Save"       # Final review
        ]
        
        # -- Apothikeusi stoixeion tis formas -- #
        self.form_data = {
            "title": "",
            "description": "",
            "date": "",
            "time": "",
            "location": "",
            "event_type": "public",
            "max_participants": "",
            "is_paid": False,
            "price": "0",
            "payment_methods": [],
            "uploaded_files": [],
            "notification_settings": {
                "target": "all",
                "timing": ["on_registration"]
            }
        }
        
        # -- Top Frame gia tin mpara proodou -- #
        self.setup_progress_bar()
        
        # -- Content Frame gia ta pedia tis formas me scroll -- #
        self.content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=(20, 100))
        
        # -- Bottom Frame gia ta  navigation buttons-- #
        self.setup_navigation()
        
        # -- Arxikopoiisi tou protou vimatos -- #
        self.show_current_step()
        
    def setup_progress_bar(self):
        """
        # -- Dimiourgia tis mparas proodou -- #
        # -- Deixnei se poio vima vriskomaste -- #
        """
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(fill="x", padx=20, pady=20)
        
        # -- Progress indicator frames -- #
        self.step_frames = []
        for i, step in enumerate(self.steps):
            step_frame = ctk.CTkFrame(
                self.progress_frame,
                fg_color="#C8A165" if i == 0 else "#E5E5E5",
                width=30,
                height=30,
                corner_radius=15
            )
            step_frame.pack(side="left", padx=(0 if i == 0 else 10, 10), pady=10)
            step_frame.pack_propagate(False)
            
            # -- Noumero vimatos -- #
            step_label = ctk.CTkLabel(
                step_frame,
                text=str(i + 1),
                text_color="black",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            step_label.place(relx=0.5, rely=0.5, anchor="center")
            
            self.step_frames.append((step_frame, step_label))
            
            # -- Grammi sindesis metaxi vimaton (ektos apo to teleutaio) -- #
            if i < len(self.steps) - 1:
                connector = ctk.CTkFrame(
                    self.progress_frame,
                    fg_color="#E5E5E5",
                    width=50,
                    height=2
                )
                connector.pack(side="left", padx=0, pady=10)
    
    def setup_navigation(self):
        """
        # -- Dimiourgia koumpion gia tin pligoisi metaxi ton vimaton -- #
        """
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=40, pady=(0, 20), side="bottom")
        
        # -- Koumpi Cancel -- #
        self.cancel_btn = ctk.CTkButton(
            self.nav_frame,
            text="Cancel",
            fg_color="transparent",
            text_color="black",
            border_color="#C8A165",
            border_width=1,
            hover_color="#E5E5E5",
            width=100,
            command=self.cancel_creation
        )
        self.cancel_btn.pack(side="left", padx=5)
        
        # -- Koumpi Previous -- #
        self.prev_btn = ctk.CTkButton(
            self.nav_frame,
            text="← Previous",
            fg_color="transparent",
            text_color="black",
            border_color="#C8A165",
            border_width=1,
            hover_color="#E5E5E5",
            width=100,
            command=self.prev_step,
            state="disabled"
        )
        self.prev_btn.pack(side="left", padx=5)
        
        # -- Koumpi Next/Finish -- #
        self.next_btn = ctk.CTkButton(
            self.nav_frame,
            text="Next →",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            width=100,
            command=self.next_step
        )
        self.next_btn.pack(side="right", padx=5)
    
    def show_current_step(self):
        """
        # -- Emfanisi tou trexontos vimatos tis formas -- #
        """
        # -- Katharismos tou content frame -- #
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # -- Titlos vimatos -- #
        step_title = ctk.CTkLabel(
            self.content_frame,
            text=self.steps[self.current_step],
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="black"
        )
        step_title.pack(pady=(0, 30))
        
        # -- Emfanisi ton pedion analoga me to vima -- #
        if self.current_step == 0:
            self.show_basic_details()
        elif self.current_step == 1:
            self.show_location_type()
        elif self.current_step == 2:
            self.show_capacity_cost()
        elif self.current_step == 3:
            self.show_additional_info()
        elif self.current_step == 4:
            self.show_notifications()
        else:
            self.show_review()
        
        # -- Enimersoi UI -- #
        self.update_navigation()
        self.update_progress_indicators()
        
    def show_basic_details(self):
        """
        # -- Pedia gia ta vasika stoixeia tis ekdilosis -- #
        """
        # -- Event Title -- #
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Event Title",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        title_label.pack(anchor="w", pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter event title",
            width=400,
            height=35
        )
        self.title_entry.pack(anchor="w", pady=(0, 20))
        self.title_entry.insert(0, self.form_data["title"])
        
        # -- Event Description -- #
        desc_label = ctk.CTkLabel(
            self.content_frame,
            text="Description",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="black"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        self.desc_text = ctk.CTkTextbox(
            self.content_frame,
            width=400,
            height=100,
            border_width=1,
            border_color="#E5E5E5",
            fg_color="white"
        )
        self.desc_text.pack(anchor="w", pady=(0, 20))
        self.desc_text.insert("1.0", self.form_data["description"])
        
        # -- Date & Time frame -- #
        datetime_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        datetime_frame.pack(fill="x", pady=(0, 20))
        
        # -- Date -- #
        date_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        date_frame.pack(side="left", padx=(0, 20))
        
        date_label = ctk.CTkLabel(
            date_frame,
            text="Date",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        date_label.pack(anchor="w", pady=(0, 5))
        
        self.date_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="Click to select date",
            width=200,
            height=35,
            border_width=1,
            border_color="#E5E5E5",
            fg_color="white",
            state="readonly"
        )
        self.date_entry.pack(anchor="w")
        self.date_entry.insert(0, self.form_data["date"])
        self.date_entry.bind("<Button-1>", self.show_date_picker)
        
        # -- Time -- #
        time_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        time_frame.pack(side="left")
        
        time_label = ctk.CTkLabel(
            time_frame,
            text="Time",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        time_label.pack(anchor="w", pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(
            time_frame,
            placeholder_text="Click to select time",
            width=200,
            height=35,
            border_width=1,
            border_color="#E5E5E5",
            fg_color="white",
            state="readonly"
        )
        self.time_entry.pack(anchor="w")
        self.time_entry.insert(0, self.form_data["time"])
        self.time_entry.bind("<Button-1>", self.show_time_picker)
    
    def show_location_type(self):
        """
        # -- Pedia gia tin topothesia kai ton tipo tis ekdilosis -- #
        """
        # -- Location -- #
        location_label = ctk.CTkLabel(
            self.content_frame,
            text="Event Location",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        location_label.pack(anchor="w", pady=(0, 5))
        
        self.location_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter event location",
            width=400,
            height=35
        )
        self.location_entry.pack(anchor="w", pady=(0, 30))
        self.location_entry.insert(0, self.form_data["location"])
        
        # -- Event Type -- #
        type_label = ctk.CTkLabel(
            self.content_frame,
            text="Event Type",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        type_label.pack(anchor="w", pady=(0, 10))
        
        self.event_type_var = ctk.StringVar(value=self.form_data["event_type"])
        
        public_radio = ctk.CTkRadioButton(
            self.content_frame,
            text="Public Event",
            font=ctk.CTkFont(size=14),
            variable=self.event_type_var,
            value="public"
        )
        public_radio.pack(anchor="w", pady=(0, 5))
        
        private_radio = ctk.CTkRadioButton(
            self.content_frame,
            text="Private Event",
            font=ctk.CTkFont(size=14),
            variable=self.event_type_var,
            value="private"
        )
        private_radio.pack(anchor="w")
    
    def show_capacity_cost(self):
        """
        # -- Pedia gia tin xwritikotita kai to kostos tis ekdilosis -- #
        """
        # -- Maximum Participants -- #
        capacity_label = ctk.CTkLabel(
            self.content_frame,
            text="Maximum Participants",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        capacity_label.pack(anchor="w", pady=(0, 5))
        
        self.capacity_entry = ctk.CTkEntry(
            self.content_frame,
            placeholder_text="Enter maximum number of participants",
            width=400,
            height=35,
            border_width=1,
            border_color="#E5E5E5",
            fg_color="white"
        )
        self.capacity_entry.pack(anchor="w", pady=(0, 30))
        self.capacity_entry.insert(0, self.form_data["max_participants"])
        
        # -- Cost Type -- #
        cost_label = ctk.CTkLabel(
            self.content_frame,
            text="Event Cost",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        cost_label.pack(anchor="w", pady=(0, 10))
        
        # -- Frame gia ta pedia kostous -- #
        cost_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        cost_frame.pack(fill="x")
        
        self.is_paid_var = ctk.BooleanVar(value=self.form_data["is_paid"])
        
        free_radio = ctk.CTkRadioButton(
            cost_frame,
            text="Free Event",
            font=ctk.CTkFont(size=14),
            variable=self.is_paid_var,
            value=False,
            command=self.toggle_price_field
        )
        free_radio.pack(side="left", padx=(0, 20))
        
        paid_radio = ctk.CTkRadioButton(
            cost_frame,
            text="Paid Event",
            font=ctk.CTkFont(size=14),
            variable=self.is_paid_var,
            value=True,
            command=self.toggle_price_field
        )
        paid_radio.pack(side="left")
        
        # -- Price Entry -- #
        self.price_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.price_frame.pack(fill="x", pady=(20, 0))
        
        price_label = ctk.CTkLabel(
            self.price_frame,
            text="Price (€)",
            font=ctk.CTkFont(size=16),
            text_color="black"
        )
        price_label.pack(side="left", padx=(0, 10))
        
        self.price_entry = ctk.CTkEntry(
            self.price_frame,
            placeholder_text="0.00",
            width=100,
            height=35,
            border_width=1,
            border_color="#E5E5E5",
            fg_color="white"
        )
        self.price_entry.pack(side="left")
        self.price_entry.insert(0, self.form_data["price"])
        
        # -- Enable/Disable price field based on selection -- #
        self.toggle_price_field()

    def update_payment_methods(self):
        """
        # -- Enimerwsi epilegmenon methodon pliromis -- #
        """
        self.form_data["payment_methods"] = [
            method for method, var in self.payment_methods_vars.items()
            if var.get()
        ]
    
    def toggle_price_field(self):
        """
        # -- Energopoiisi/Apenergopoiisi tou pediou timis -- #
        """
        if self.is_paid_var.get():
            self.price_entry.configure(state="normal")
            self.price_frame.pack(fill="x", pady=(20, 0))
            
            # -- Payment Methods Section -- #
            #  frame gia payment methods section
            self.payment_methods_frame = ctk.CTkFrame(
                self.content_frame, 
                fg_color="transparent"
            )
            self.payment_methods_frame.pack(fill="x", pady=20, after=self.price_frame)
            
            
            separator = ctk.CTkFrame(
                self.payment_methods_frame, 
                height=2, 
                fg_color="#E5E5E5"
            )
            separator.pack(fill="x", pady=(0, 20))
            
            # Payment methods title
            methods_label = ctk.CTkLabel(
                self.payment_methods_frame,
                text="Payment Methods",
                font=ctk.CTkFont(family="Roboto", size=16),
                text_color="black"
            )
            methods_label.pack(anchor="w", pady=(0, 15))
            
            # Frame for payment method checkboxes 
            self.checkboxes_frame = ctk.CTkFrame(
                self.payment_methods_frame,
                fg_color="white",
                border_width=1,
                border_color="#E5E5E5",
                corner_radius=8
            )
            self.checkboxes_frame.pack(fill="x", padx=5)
            
            # Payment methods options
            methods = ["Credit Card", "Bank Transfer", "Cryptocurrency"]
            self.payment_methods_vars = {}
            
            methods_frame = ctk.CTkFrame(self.checkboxes_frame, fg_color="transparent")
            methods_frame.pack(fill="x", padx=10, pady=10)
            
            for method in methods:
                var = ctk.BooleanVar(value=method in self.form_data["payment_methods"])
                checkbox = ctk.CTkCheckBox(
                    methods_frame,
                    text=method,
                    font=ctk.CTkFont(family="Roboto", size=14),
                    variable=var,
                    fg_color="#C8A165",
                    hover_color="#b38e58",
                    command=self.update_payment_methods
                )
                checkbox.pack(anchor="w", pady=(0, 5))
                self.payment_methods_vars[method] = var
        else:
            # Hide price field
            self.price_entry.configure(state="disabled")
            self.price_frame.pack_forget()
            
            # Hide payment methods section if it exists
            if hasattr(self, 'payment_methods_frame'):
                self.payment_methods_frame.pack_forget()
    
    def show_review(self):
        """
        # -- Selida episkopisis ton stoixeion tis ekdilosis -- #
        """
        # -- Update form data -- #
        self.update_form_data()
        
        # -- Review Title -- #
        review_label = ctk.CTkLabel(
            self.content_frame,
            text="Review your event details",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="black"
        )
        review_label.pack(pady=(0, 20))
        
        # -- Frame for data display -- #
        data_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        data_frame.pack(fill="both", expand=True)
        
        # -- Event Details -- #
        # -- Basic Details -- #
        details = [
            ("Event Title:", self.form_data["title"]),
            ("Description:", self.form_data["description"]),
            ("Date:", self.form_data["date"]),
            ("Time:", self.form_data["time"]),
            ("Location:", self.form_data["location"]),
            ("Event Type:", self.form_data["event_type"].capitalize()),
            ("Maximum Participants:", self.form_data["max_participants"]),
            ("Event Cost:", "Paid" if self.form_data["is_paid"] else "Free"),
        ]
        
        if self.form_data["is_paid"]:
            details.append(("Price:", f"€{self.form_data['price']}"))
            if self.form_data["payment_methods"]:
                details.append(("Payment Methods:", ", ".join(self.form_data["payment_methods"])))

        # -- Add Files Info -- #
        if self.form_data["uploaded_files"]:
            details.append(("Uploaded Files:", str(len(self.form_data["uploaded_files"]))))
        
        # -- Add Notification Settings -- #
        details.append(("Notification Target:", self.form_data["notification_settings"]["target"]))
        timings = self.form_data["notification_settings"]["timing"]
        if timings:
            details.append(("Notification Timing:", ", ".join(timings)))
        
        for label, value in details:
            row = ctk.CTkFrame(data_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            label = ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black"
            )
            label.pack(side="left")
            
            value = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color="black"
            )
            value.pack(side="right")
    
    def show_additional_info(self):
        """
        # -- Pedia gia tin prosthiki arxeion kai eikonon -- #
        """
        # -- Title -- #
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Upload Files",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="black"
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # -- Upload Sections -- #
        sections = [
            ("Event Images", "Upload event images (JPG, PNG)"),
            ("Event Documents", "Upload documents (PDF, DOC)"),
            ("Additional Files", "Upload other related files")
        ]

        for section_title, placeholder in sections:
            section_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            section_frame.pack(fill="x", pady=(0, 20))

            # Section Label
            section_label = ctk.CTkLabel(
                section_frame,
                text=section_title,
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            section_label.pack(side="left")

            # Upload Button
            upload_btn = ctk.CTkButton(
                section_frame,
                text="Choose File",
                fg_color="#C8A165",
                text_color="black",
                hover_color="#b38e58",
                font=ctk.CTkFont(family="Roboto", size=14),
                width=120,
                height=32,
                corner_radius=8
            )
            upload_btn.pack(side="right")

    def show_notifications(self):
        """
        # -- Pedia gia tis rithmiseis eidopoiiseon -- #
        """
        # -- Title -- #
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Notification Settings",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="black"
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # -- Target Audience -- #
        target_label = ctk.CTkLabel(
            self.content_frame,
            text="Send Notifications To:",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="black"
        )
        target_label.pack(anchor="w", pady=(0, 10))

        targets = ["All Participants", "Specific Groups", "Custom Lists"]
        self.target_var = ctk.StringVar(value=targets[0])

        for target in targets:
            radio = ctk.CTkRadioButton(
                self.content_frame,
                text=target,
                font=ctk.CTkFont(family="Roboto", size=14),
                variable=self.target_var,
                value=target
            )
            radio.pack(anchor="w", pady=(0, 5))

        # -- Separator -- #
        separator = ctk.CTkFrame(self.content_frame, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=20)

        # -- Notification Timing -- #
        timing_label = ctk.CTkLabel(
            self.content_frame,
            text="When to Send Notifications:",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="black"
        )
        timing_label.pack(anchor="w", pady=(0, 10))

        timings = ["On Creation", "1 Month Before", "1 Year Before", "Custom Time"]
        self.timing_vars = {}

        for timing in timings:
            var = ctk.BooleanVar(value=timing == "On Creation")
            checkbox = ctk.CTkCheckBox(
                self.content_frame,
                text=timing,
                font=ctk.CTkFont(family="Roboto", size=14),
                variable=var
            )
            checkbox.pack(anchor="w", pady=(0, 5))
            self.timing_vars[timing] = var

    def update_form_data(self):
        """
        # -- Enimerwsi ton dedomenon tis formas -- #
        """
        if self.current_step == 0:
            self.form_data["title"] = self.title_entry.get()
            self.form_data["description"] = self.desc_text.get("1.0", "end-1c")
            self.form_data["date"] = self.date_entry.get()
            self.form_data["time"] = self.time_entry.get()
        elif self.current_step == 1:
            self.form_data["location"] = self.location_entry.get()
            self.form_data["event_type"] = self.event_type_var.get()
        elif self.current_step == 2:
            self.form_data["max_participants"] = self.capacity_entry.get()
            self.form_data["is_paid"] = self.is_paid_var.get()
            self.form_data["price"] = self.price_entry.get() if self.is_paid_var.get() else "0"
            # Payment methods updated automatically through update_payment_methods()
        elif self.current_step == 4:
            # Update notification settings
            self.form_data["notification_settings"]["target"] = self.target_var.get()
            selected_timings = [
                timing for timing, var in self.timing_vars.items()
                if var.get()
            ]
            self.form_data["notification_settings"]["timing"] = selected_timings

    def show_date_picker(self, event):
        """
        # -- Emfanisi tou picker gia epilogi imerominias -- #
        """
        from tkcalendar import Calendar
        
        date_picker = ctk.CTkToplevel(self)
        date_picker.title("Select Date")
        date_picker.geometry("300x300")
        date_picker.transient(self)
        date_picker.grab_set()
        
        # Center the picker
        date_picker.update_idletasks()
        x = (date_picker.winfo_screenwidth() - date_picker.winfo_width()) // 2
        y = (date_picker.winfo_screenheight() - date_picker.winfo_height()) // 2
        date_picker.geometry(f"+{x}+{y}")
        
        def on_date_select():
            selected_date = cal.get_date()
            self.date_entry.configure(state="normal")
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, selected_date)
            self.date_entry.configure(state="readonly")
            date_picker.destroy()
        
        cal = Calendar(date_picker, selectmode="day")
        cal.pack(pady=20)
        
        select_btn = ctk.CTkButton(
            date_picker,
            text="Select",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            command=on_date_select
        )
        select_btn.pack(pady=10)
    
    def show_time_picker(self, event):
        """
        # -- Emfanisi tou picker gia epilogi oras -- #
        """
        time_picker = ctk.CTkToplevel(self)
        time_picker.title("Select Time")
        time_picker.geometry("300x400")
        time_picker.transient(self)
        time_picker.grab_set()
        
       
        time_picker.update_idletasks()
        x = (time_picker.winfo_screenwidth() - time_picker.winfo_width()) // 2
        y = (time_picker.winfo_screenheight() - time_picker.winfo_height()) // 2
        time_picker.geometry(f"+{x}+{y}")
        
        hours_frame = ctk.CTkFrame(time_picker)
        hours_frame.pack(pady=20)
        
        hours_label = ctk.CTkLabel(hours_frame, text="Hour")
        hours_label.pack()
        
        hours = ctk.CTkScrollableFrame(hours_frame, width=100, height=200)
        hours.pack()
        
        minutes_frame = ctk.CTkFrame(time_picker)
        minutes_frame.pack(pady=20)
        
        minutes_label = ctk.CTkLabel(minutes_frame, text="Minute")
        minutes_label.pack()
        
        minutes = ctk.CTkScrollableFrame(minutes_frame, width=100, height=200)
        minutes.pack()
        
        selected_hour = ctk.StringVar()
        selected_minute = ctk.StringVar()
        
        def on_time_select():
            # Ensure both hour and minute are selected before proceeding
            hour_val = selected_hour.get()
            minute_val = selected_minute.get()
            if hour_val and minute_val:
                selected_time = f"{hour_val}:{minute_val}"
                self.time_entry.configure(state="normal")
                self.time_entry.delete(0, "end")
                self.time_entry.insert(0, selected_time)
                self.time_entry.configure(state="readonly")
                time_picker.destroy()
            else:
                
                print("Please select both hour and minute.")

        # Hours buttons
        for h in range(24):
            hour = f"{h:02d}"
            btn = ctk.CTkButton(
                hours,
                text=hour,
                width=70,
                height=30,
                fg_color="#E5E5E5" if h % 2 == 0 else "transparent",
                text_color="black",
                hover_color="#C8A165",
                command=lambda h=hour: selected_hour.set(h)
            )
            btn.pack(pady=2)
        
        # Minutes buttons
        for m in range(0, 60, 5):
            minute = f"{m:02d}"
            btn = ctk.CTkButton(
                minutes,
                text=minute,
                width=70,
                height=30,
                fg_color="#E5E5E5" if m % 10 == 0 else "transparent", 
                text_color="black",
                hover_color="#C8A165",
                command=lambda m=minute: selected_minute.set(m)
            )
            btn.pack(pady=2)
        
        select_btn = ctk.CTkButton(
            time_picker,
            text="Select",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            command=on_time_select
        )
        select_btn.pack(pady=10)
    
    def update_progress_indicators(self):
        """
        # -- Enimerwsi xromatwn progress indicators -- #
        """
        for i, (frame, label) in enumerate(self.step_frames):
            if i < self.current_step:  # Completed steps
                frame.configure(fg_color="#74A35C")  # Prasino
                label.configure(text="✓", text_color="black")
            elif i == self.current_step:  # Current step
                frame.configure(fg_color="#C8A165")  # Xriso
                label.configure(text=str(i + 1), text_color="black")
            else:  # Future steps
                frame.configure(fg_color="#E5E5E5")  
                label.configure(text=str(i + 1), text_color="black")
    
    def update_navigation(self):
        """
        # -- Enimerwsi UI stoixeiwn navigation -- #
        """
        # -- Elegxos gia to koumpi Previous -- #
        if self.current_step == 0:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")
            
        # -- Elegxos gia to koumpi Next/Finish -- #
        if self.current_step == len(self.steps) - 1:
            self.next_btn.configure(text="Create Event")
        else:
            self.next_btn.configure(text="Next →")
    
    def next_step(self):
        """
        # -- Metavasi sto epomeno vima tis formas -- #
        """
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            # -- Elegxos an exei epilexthei toulaxiston mia methodos pliromis -- #
            if self.is_paid_var.get() and not self.form_data["payment_methods"]:
                print("Please select at least one payment method")
                return  # Prevent moving to the next step
            
            # -- Tha prostethei i dimiourgia tou event argotera -- #
            print("Event creation will be implemented later")
    
    def prev_step(self):
        """
        # -- Metavasi sto proigoumeno vima tis formas -- #
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    def cancel_creation(self):
        """
        # -- Epistrofi stin arxiki selida diaxeirisis events -- #
        """
        # -- Katharismos tis trexousas selidas -- #
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # -- Epanafora tis selidas diaxeirisis -- #
        manage_page = self.manage_page.__class__(self.master, self.manage_page.dashboard)
        manage_page.pack(fill="both", expand=True)
