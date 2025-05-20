import datetime
import tkinter.messagebox as messagebox
import customtkinter as ctk
from tkinter.messagebox import askyesno
from src.classes.event.ManageEvent import ManageEvent

class CreateEventPage(ctk.CTkFrame):
    def __init__(self, master, dashboard):
        # -- Dimiourgia tou vasikou frame gia ti selida dimiourgias event -- #
        super().__init__(master, fg_color="transparent")
        self.dashboard = dashboard
        self.master = master  # Store master reference

        # Store user info explicitly and validate
        # Validate dashboard and current_user
        if not hasattr(dashboard, 'current_user') or dashboard.current_user is None:
            raise ValueError("No active user session. Please log in again.")
        if not hasattr(dashboard.current_user, 'user_id'):
            raise ValueError("Invalid user session. Please log in again.")
            
        self.current_user = dashboard.current_user
        self.current_step = 0

        # Bind to master events
        self.bind("<Destroy>", self.on_destroy)
        
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
        # -- Πεδία για τα βασικά στοιχεία της εκδήλωσης -- #
        """
        import datetime

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
            height=35,
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.title_entry.pack(anchor="w", pady=(0, 20))
        self.title_entry.insert(0, self.form_data.get("title", ""))

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
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8
        )
        self.desc_text.pack(anchor="w", pady=(0, 20))
        self.desc_text.insert("1.0", self.form_data.get("description", ""))

        # -- Date & Time frame -- #
        datetime_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        datetime_frame.pack(fill="x", pady=(0, 20))

        # -- Date frame -- #
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
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8,
            state="readonly"
        )
        self.date_entry.pack(anchor="w")
        self.date_entry.configure(state="normal")
        self.date_entry.delete(0, "end")

        # -- Προσθήκη μορφοποίησης ημερομηνίας --
        raw_date = self.form_data.get("date", "")
        if raw_date:
            try:
                # Δοκίμασε αν είναι ISO (YYYY-MM-DD)
                parsed_date = datetime.datetime.strptime(raw_date, "%Y-%m-%d")
                formatted_date = parsed_date.strftime("%m/%d/%Y")
                self.date_entry.insert(0, formatted_date)
            except Exception:
                self.date_entry.insert(0, raw_date)
        self.date_entry.configure(state="readonly")
        self.date_entry.bind("<Button-1>", self.show_date_picker)

        # -- Time frame -- #
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
            border_width=2,
            border_color="#C8A165",
            fg_color="white",
            corner_radius=8,
            state="readonly"
        )
        self.time_entry.pack(anchor="w")
        self.time_entry.configure(state="normal")
        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, self.form_data.get("time", ""))
        self.time_entry.configure(state="readonly")
        self.time_entry.bind("<Button-1>", self.show_time_picker)

        # -- Error Label -- #
        self.error_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=14)
        )
        self.error_label.pack(anchor="w", pady=(5, 10))


            
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
        
        # -- Error Label -- #
        self.error_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=14)
        )
        self.error_label.pack(anchor="w", pady=(5, 10))

    
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

        # -- Error Label -- #
        self.error_label = ctk.CTkLabel(
            self.content_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=14)
        )
        self.error_label.pack(anchor="w", pady=(5, 10))


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
            
            # Payment methods options using radiobuttons
            methods_label = ctk.CTkLabel(
                self.payment_methods_frame,
                text="Select Payment Method",
                font=ctk.CTkFont(family="Roboto", size=14),
                text_color="black"
            )
            methods_label.pack(anchor="w", pady=(0, 10))

            methods = [
                ("Credit Card", "credit_card"),
                ("Bank Transfer", "bank_transfer"),
                ("Cryptocurrency", "cryptocurrency")
            ]
            
            stored_payment_method = self.form_data.get("payment_method")
            if stored_payment_method and stored_payment_method in ["credit_card", "bank_transfer", "cryptocurrency"]:
                default_method = stored_payment_method
            else:
                default_method = "credit_card"
                
            self.payment_method_var = ctk.StringVar(value=default_method)
            
            methods_frame = ctk.CTkFrame(self.checkboxes_frame, fg_color="transparent")
            methods_frame.pack(fill="x", padx=10, pady=10)
            
            for display_text, value in methods:
                radio = ctk.CTkRadioButton(
                    methods_frame,
                    text=display_text,
                    font=ctk.CTkFont(family="Roboto", size=14),
                    variable=self.payment_method_var,
                    value=value,
                    fg_color="#C8A165",
                    hover_color="#b38e58"
                )
                radio.pack(anchor="w", pady=(0, 5))
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
            if hasattr(self, 'payment_method_var'):
                method_display = {
                    'credit_card': 'Credit Card',
                    'bank_transfer': 'Bank Transfer',
                    'cryptocurrency': 'Cryptocurrency'
                }
                payment_method = method_display.get(self.payment_method_var.get(), self.payment_method_var.get())
                details.append(("Payment Method:", payment_method))

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
        # -- Πεδία για τις ρυθμίσεις ειδοποιήσεων -- #
        """
        import datetime
        from tkinter import messagebox

        # Καθαρισμός περιεχομένου
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Τίτλος
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="Notification Settings",
            font=ctk.CTkFont(family="Roboto", size=16),
            text_color="black"
        )
        title_label.pack(anchor="w", pady=(0, 20))

        # Target Audience
        target_label = ctk.CTkLabel(
            self.content_frame,
            text="Send Notifications To:",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="black"
        )
        target_label.pack(anchor="w", pady=(0, 10))

        targets = ["All Users", "Users following you", "Custom Lists"]
        selected_target = self.form_data.get("notification_settings", {}).get("target", targets[0])
        self.target_var = ctk.StringVar(value=selected_target)

        for target in targets:
            radio = ctk.CTkRadioButton(
                self.content_frame,
                text=target,
                font=ctk.CTkFont(family="Roboto", size=14),
                variable=self.target_var,
                value=target
            )
            radio.pack(anchor="w", pady=(0, 5))

        # Διαχωριστικό
        separator = ctk.CTkFrame(self.content_frame, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=20)

        # Notification Timing
        timing_label = ctk.CTkLabel(
            self.content_frame,
            text="When to Send Notifications:",
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="black"
        )
        timing_label.pack(anchor="w", pady=(0, 10))

        # Ημερομηνία Event για έλεγχο εγκυρότητας
        try:
            date_str = self.date_entry.get().strip()
            event_date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            today = datetime.date.today()
            days_until_event = (event_date - today).days
        except Exception:
            days_until_event = 3650  # Assume far future if invalid date

        timings = ["On Creation", "1 Month Before", "1 Year Before", "Custom Time"]
        saved_timings = self.form_data.get("notification_settings", {}).get("timing", ["On Creation"])
        if not saved_timings:
            saved_timings = ["On Creation"]

        self.timing_vars = {}

        def on_timing_click(timing):
            if timing == "1 Month Before" and days_until_event < 30:
                messagebox.showerror("Invalid Timing", "Το event είναι σε λιγότερο από 30 μέρες.")
                self.timing_vars[timing].set(False)
            elif timing == "1 Year Before" and days_until_event < 365:
                messagebox.showerror("Invalid Timing", "Το event είναι σε λιγότερο από 1 χρόνο.")
                self.timing_vars[timing].set(False)

        for timing in timings:
            var = ctk.BooleanVar(value=(timing in saved_timings))
            cb = ctk.CTkCheckBox(
                self.content_frame,
                text=timing,
                font=ctk.CTkFont(family="Roboto", size=14),
                variable=var,
                command=lambda t=timing: on_timing_click(t)
            )
            cb.pack(anchor="w", pady=(0, 5))
            self.timing_vars[timing] = var




    def update_form_data(self):
        """
        # -- Ενημέρωση των δεδομένων της φόρμας ανά βήμα -- #
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
            if hasattr(self, 'payment_method_var'):
                self.form_data["payment_method"] = self.payment_method_var.get()
            
        elif self.current_step == 4:
            # Ενημέρωση ρυθμίσεων ειδοποιήσεων
            self.form_data.setdefault("notification_settings", {})
            self.form_data["notification_settings"]["target"] = self.target_var.get()
            selected_timings = [
                timing for timing, var in self.timing_vars.items() if var.get()
            ]
            self.form_data["notification_settings"]["timing"] = selected_timings

        else:
            pass  


    def show_date_picker(self, event):
        from tkcalendar import Calendar
        import datetime

        date_picker = ctk.CTkToplevel(self)
        date_picker.title("Select Date")
        date_picker.geometry("300x300")
        date_picker.transient(self)
        date_picker.grab_set()

        # Κεντράρισμα του picker
        date_picker.update_idletasks()
        x = (date_picker.winfo_screenwidth() - date_picker.winfo_width()) // 2
        y = (date_picker.winfo_screenheight() - date_picker.winfo_height()) // 2
        date_picker.geometry(f"+{x}+{y}")

        # Προσπάθεια ανάγνωσης αρχικής ημερομηνίας από το entry
        try:
            init_date = datetime.datetime.strptime(self.date_entry.get(), "%m/%d/%Y").date()
        except Exception:
            init_date = None

        if init_date:
            cal = Calendar(date_picker, selectmode="day",
                        year=init_date.year,
                        month=init_date.month,
                        day=init_date.day)
        else:
            cal = Calendar(date_picker, selectmode="day")

        cal.pack(pady=20)

        def on_date_select():
            raw_date = cal.get_date()  # συνήθως MM/DD/YY
            try:
                parsed_date = datetime.datetime.strptime(raw_date, "%m/%d/%y")
                formatted_date = parsed_date.strftime("%m/%d/%Y")
            except Exception:
                formatted_date = raw_date  # fallback, αν αποτύχει η μετατροπή

            self.date_entry.configure(state="normal")
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, formatted_date)
            self.date_entry.configure(state="readonly")
            self.form_data["date"] = formatted_date
            date_picker.destroy()

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
        Show a simplified time picker with common time slots
        """
        time_picker = ctk.CTkToplevel(self)
        time_picker.title("Select Time")
        time_picker.geometry("250x300")
        time_picker.transient(self)
        time_picker.grab_set()
        
        # Center the window
        time_picker.update_idletasks()
        x = (time_picker.winfo_screenwidth() - time_picker.winfo_width()) // 2
        y = (time_picker.winfo_screenheight() - time_picker.winfo_height()) // 2
        time_picker.geometry(f"+{x}+{y}")
        
        container = ctk.CTkFrame(time_picker, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Common time slots section
        presets_label = ctk.CTkLabel(container, text="Quick Selection", font=ctk.CTkFont(size=14, weight="bold"))
        presets_label.pack(pady=(0, 10))
        
        presets = [
            ("Morning", "09:00"),
            ("Noon", "12:00"),
            ("Afternoon", "15:00"),
            ("Evening", "18:00"),
            ("Night", "20:00")
        ]
        
        # Create buttons for presets
        for label, time_value in presets:
            btn = ctk.CTkButton(
                container,
                text=f"{label} ({time_value})",
                fg_color="#C8A165",
                text_color="black",
                hover_color="#b38e58",
                command=lambda t=time_value: self.set_time(t, time_picker)
            )
            btn.pack(pady=2, fill="x")
            
        separator = ctk.CTkFrame(container, height=2, fg_color="#E5E5E5")
        separator.pack(fill="x", pady=10)
            
        # Custom time selection
        custom_label = ctk.CTkLabel(container, text="Custom Time", font=ctk.CTkFont(size=14, weight="bold"))
        custom_label.pack(pady=(0, 10))
        
        # Time selection frame
        time_frame = ctk.CTkFrame(container, fg_color="transparent")
        time_frame.pack(fill="x")
        
        # Hour selection
        hour_var = ctk.StringVar()
        hour_menu = ctk.CTkOptionMenu(
            time_frame,
            values=[f"{h:02d}" for h in range(24)],
            variable=hour_var,
            fg_color="#E5E5E5",
            text_color="black",
            button_color="#C8A165",
            button_hover_color="#b38e58",
            width=70
        )
        hour_menu.pack(side="left", padx=5)
        
        # Separator label
        ctk.CTkLabel(time_frame, text=":", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        
        # Minute selection
        minute_var = ctk.StringVar()
        minute_menu = ctk.CTkOptionMenu(
            time_frame,
            values=[f"{m:02d}" for m in range(0, 60, 15)],
            variable=minute_var,
            fg_color="#E5E5E5",
            text_color="black",
            button_color="#C8A165",
            button_hover_color="#b38e58",
            width=70
        )
        minute_menu.pack(side="left", padx=5)
        
        # Set button for custom time
        def set_custom_time():
            if hour_var.get() and minute_var.get():
                self.set_time(f"{hour_var.get()}:{minute_var.get()}", time_picker)
            else:
                error_label.configure(text="Please select both hour and minute")
                
        set_btn = ctk.CTkButton(
            container,
            text="Set Time",
            fg_color="#C8A165",
            text_color="black",
            hover_color="#b38e58",
            command=set_custom_time
        )
        set_btn.pack(pady=10, fill="x")
        
        # Error label
        error_label = ctk.CTkLabel(container, text="", text_color="red")
        error_label.pack()
        
        # Try to set initial values if time exists
        try:
            current_time = self.form_data.get("time", "").split(":")
            if len(current_time) == 2:
                hour_var.set(current_time[0])
                minute_var.set(current_time[1])
        except Exception:
            pass
            
    def set_time(self, time_str, picker):
        """Helper method to set time and close picker"""
        self.time_entry.configure(state="normal")
        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, time_str)
        self.time_entry.configure(state="readonly")
        self.form_data["time"] = time_str
        picker.destroy()
        
    
    

    def validate_event_data(self):
        MAX_TITLE_LENGTH = 100
        MAX_DESCRIPTION_LENGTH = 500

        if self.current_step == 0:
            # Έλεγχος τίτλου
            title = self.title_entry.get().strip()
            if not title:
                return "Παρακαλώ εισάγετε τίτλο εκδήλωσης."
            if len(title) > MAX_TITLE_LENGTH:
                return f"Ο τίτλος δεν μπορεί να είναι πάνω από {MAX_TITLE_LENGTH} χαρακτήρες."

            # Έλεγχος περιγραφής
            description = self.desc_text.get("1.0", "end").strip()
            if not description:
                return "Παρακαλώ εισάγετε περιγραφή εκδήλωσης."
            if len(description) > MAX_DESCRIPTION_LENGTH:
                return f"Η περιγραφή δεν μπορεί να είναι πάνω από {MAX_DESCRIPTION_LENGTH} χαρακτήρες."

        

            # Έλεγχος ημερομηνίας
            date_str = self.date_entry.get().strip()
            if not date_str:
                return "Παρακαλώ επιλέξτε ημερομηνία."
            import datetime
            try:
                selected_date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                min_allowed_date = datetime.date.today() + datetime.timedelta(days=2)
                if selected_date < min_allowed_date:
                    return "Παρακαλώ επιλέξτε ημερομηνία τουλάχιστον 2 μέρες μετά από σήμερα."
            except Exception:
                return "Παρακαλώ επιλέξτε σωστή ημερομηνία (MM/DD/YYYY)."

            # Έλεγχος ώρας
            time_str = self.time_entry.get().strip()
            if not time_str:
                return "Παρακαλώ επιλέξτε ώρα."
            try:
                hour, minute = map(int, time_str.split(":"))
                if not (0 <= hour < 24 and 0 <= minute < 60):
                    raise ValueError
            except Exception:
                return "Παρακαλώ επιλέξτε σωστή ώρα (HH:MM)."

        elif self.current_step == 1:
            # Έλεγχος τοποθεσίας στο βήμα 1
            location = self.location_entry.get().strip()
            if not location:
                return "Παρακαλώ εισάγετε τοποθεσία εκδήλωσης."

        elif self.current_step == 2:
            # Έλεγχος μέγιστου αριθμού συμμετεχόντων
            capacity = self.capacity_entry.get().strip()
            if not capacity:
                return "Παρακαλώ εισάγετε αριθμό συμμετεχόντων."
            if not capacity.isdigit() or int(capacity) <= 0:
                return "Εισάγετε έγκυρο αριθμό συμμετεχόντων."

            # Έλεγχος τοποθεσίας από form_data 
            location = self.form_data.get("location", "").strip()
            if not location:
                return "Παρακαλώ εισάγετε τοποθεσία εκδήλωσης."

            # Έλεγχος κόστους για επί πληρωμή εκδήλωση
            if self.is_paid_var.get():
                price = self.price_entry.get().strip()
                if not price:
                    return "Παρακαλώ εισάγετε τιμή."
                try:
                    if float(price) <= 0:
                        return "Η τιμή πρέπει να είναι θετικός αριθμός."
                except Exception:
                    return "Παρακαλώ εισάγετε έγκυρη τιμή."

        return None  





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
        self.update_form_data()

        error = self.validate_event_data()
        if error:
            self.show_error(error)  # Εμφάνιση popup με το λάθος
            return  # Μπλοκάρει τη μετάβαση λόγω λάθους

        # Καθαρίζουμε τυχόν προηγούμενα errors (αν υπάρχει ακόμα)
        if hasattr(self, "error_label") and self.error_label.winfo_exists():
            self.error_label.configure(text="")

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            if self.is_paid_var.get() and not hasattr(self, 'payment_method_var'):
                self.show_error("Please select a payment method")
                return

            self.save_event()   



    def prev_step(self):
        self.update_form_data()
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
            if hasattr(self, "error_label") and self.error_label.winfo_exists():
                self.error_label.configure(text="")



    def show_error(self, message):
        import tkinter.messagebox as mb
        mb.showerror("Error", message)


    def show_success(self, message):
        from CTkMessagebox import CTkMessagebox
        CTkMessagebox(title="Success", message=message, icon="check")


    def cancel_creation(self):
        if askyesno(
            title="Cancel Creation",
            message="Are you sure you want to cancel? All entered data will be lost."
        ):
            # destroy any toplevels
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkToplevel):
                    widget.destroy()
            # clear data
            self.form_data = {key: "" for key in self.form_data}
            # go back
            self.dashboard.show_page("Manage Events")

    def on_destroy(self, event=None):
        """Cleanup when frame is destroyed"""
        if event.widget == self:
            # Clear any active toplevel windows
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkToplevel):
                    widget.destroy()
            
            # Return focus to dashboard
            if hasattr(self, 'dashboard'):
                self.dashboard.focus_set()
    
    def _validate_user(self):
        """Check if we have a valid user session"""
        if not hasattr(self, 'current_user') or self.current_user is None:
            self.show_error("No active user session. Please log in again.")
            return False
        if not hasattr(self.current_user, 'user_id'):
            self.show_error("Invalid user session. Please log in again.")
            return False
        return True

    def save_event(self):
        """
        Αποθηκεύει την εκδήλωση αφού έχουν περάσει τα validations.
        """
        # Check for valid user first
        if not self._validate_user():
            return

        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
        except OSError:
            self.show_error("Δεν υπάρχει σύνδεση στο internet. Παρακαλώ δοκιμάστε ξανά.")
            return

        # Use stored form data instead of widget values
        try:
            datetime_str = f"{self.form_data['date']} {self.form_data['time']}"
            event_datetime = datetime.datetime.strptime(datetime_str, "%m/%d/%Y %H:%M")
        except (ValueError, KeyError) as e:
            self.show_error("Invalid date/time format in stored data")
            return

        # Create event manager and set properties
        event_manager = ManageEvent(self.current_user)
        event_manager.title = self.form_data["title"]
        event_manager.description = self.form_data["description"]
        event_manager.event_date = event_datetime
        event_manager.venue = self.form_data["location"]
        event_manager.is_public = self.form_data["event_type"] == "public"
        event_manager.max_participants = int(self.form_data["max_participants"]) if self.form_data["max_participants"] else None
        event_manager.is_paid = self.form_data["is_paid"]
        event_manager.cost = float(self.form_data["price"]) if self.form_data["is_paid"] and self.form_data["price"] else 0.0
        event_manager.payment_method = self.payment_method_var.get() if self.is_paid_var.get() else None
        event_manager.status = "scheduled"
        event_manager.category = "General"  # Using default category for now

        success, result = event_manager.create_event()

        if success:
            self.show_success("Event Created Successfully!")
            self.dashboard.show_page("Manage Events")  # Return to manage events page
        else:
            self.show_error(f"Αποτυχία επικοινωνίας με τη βάση: {result}")
