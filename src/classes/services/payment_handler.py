import customtkinter as ctk

class PaymentHandler:
    """
    PaymentHandler: Handles payment processing and payment-related UI
    """
    @staticmethod
    def show_payment_dialog(parent, event, on_success):
        """Show payment dialog and handle payment process"""
        # Payment dialog
        payment = ctk.CTkToplevel(parent)
        payment.title("Payment Details")
        payment.geometry("400x500")
        payment.transient(parent)
        payment.grab_set()
        
        # Center window
        payment.update_idletasks()
        x = (payment.winfo_screenwidth() - payment.winfo_width()) // 2
        y = (payment.winfo_screenheight() - payment.winfo_height()) // 2
        payment.geometry(f"+{x}+{y}")
        
        # Event details
        title_label = ctk.CTkLabel(
            payment,
            text=event.title,
            font=ctk.CTkFont(family="Roboto", size=18, weight="bold")
        )
        title_label.pack(pady=(20,5))
        
        date_label = ctk.CTkLabel(
            payment,
            text=event.event_date.strftime('%Y-%m-%d %H:%M'),
            font=ctk.CTkFont(family="Roboto", size=14)
        )
        date_label.pack(pady=5)
        
        cost_text = "Free" if not event.is_paid else f"€{event.cost:.2f}"
        price_label = ctk.CTkLabel(
            payment,
            text=f"Amount to pay: {cost_text}",
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold")
        )
        price_label.pack(pady=(5,20))
        
        # Payment form
        form_frame = ctk.CTkFrame(payment, fg_color="transparent")
        form_frame.pack(fill="x", padx=20)
        
        # Card number
        ctk.CTkLabel(form_frame, text="Card Number:", anchor="w").pack(fill="x", pady=(0,5))
        card_number = ctk.CTkEntry(form_frame, placeholder_text="1234 5678 9012 3456")
        card_number.pack(fill="x", pady=(0,10))
        
        # Cardholder name
        ctk.CTkLabel(form_frame, text="Cardholder Name:", anchor="w").pack(fill="x", pady=(0,5))
        cardholder = ctk.CTkEntry(form_frame, placeholder_text="JOHN DOE")
        cardholder.pack(fill="x", pady=(0,10))
        
        # CVV and Expiry Date frame
        card_details = ctk.CTkFrame(form_frame, fg_color="transparent")
        card_details.pack(fill="x")
        
        # CVV
        cvv_frame = ctk.CTkFrame(card_details, fg_color="transparent")
        cvv_frame.pack(side="left", fill="x", expand=True, padx=(0,5))
        ctk.CTkLabel(cvv_frame, text="CVV:", anchor="w").pack(fill="x", pady=(0,5))
        cvv = ctk.CTkEntry(cvv_frame, placeholder_text="123", width=70)
        cvv.pack(side="left")
        
        # Expiry date
        exp_frame = ctk.CTkFrame(card_details, fg_color="transparent")
        exp_frame.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkLabel(exp_frame, text="Expiry Date:", anchor="w").pack(fill="x", pady=(0,5))
        expiry = ctk.CTkEntry(exp_frame, placeholder_text="MM/YY", width=70)
        expiry.pack(side="left")
        
        def process_payment():
            # Basic validation
            if not all([card_number.get(), cardholder.get(), cvv.get(), expiry.get()]):
                PaymentHandler.show_error(parent, "Please fill in all fields")
                return
            
            if not PaymentHandler.validate_card_info(card_number.get(), cvv.get(), expiry.get()):
                PaymentHandler.show_error(parent, "Invalid card information")
                return
            
            success = PaymentHandler.process_payment(
                amount=event.cost,
                card_number=card_number.get(),
                cvv=cvv.get(),
                expiry_date=expiry.get(),
                cardholder_name=cardholder.get()
            )
            
            if success:
                payment.destroy()
                PaymentHandler.show_processing_dialog(parent, on_success)
            else:
                PaymentHandler.show_error(parent, "Payment processing failed")
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(payment, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=20)
        
        # Pay button
        pay_btn = ctk.CTkButton(
            btn_frame,
            text="Pay",
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
            width=100,
            command=process_payment
        )
        pay_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=payment.destroy
        )
        cancel_btn.pack(side="left", padx=10)

    @staticmethod
    def show_processing_dialog(parent, callback):
        """Show payment processing dialog"""
        # Processing dialog
        processing = ctk.CTkToplevel(parent)
        processing.title("Processing Payment")
        processing.geometry("300x150")
        processing.transient(parent)
        processing.grab_set()
        
        # Center window
        processing.update_idletasks()
        x = (processing.winfo_screenwidth() - processing.winfo_width()) // 2
        y = (processing.winfo_screenheight() - processing.winfo_height()) // 2
        processing.geometry(f"+{x}+{y}")
        
        # Message
        message = ctk.CTkLabel(
            processing,
            text="Processing payment...\nPlease wait",
            font=ctk.CTkFont(family="Roboto", size=14),
            justify="center"
        )
        message.pack(expand=True)
        
        # Simulate processing
        parent.after(2000, lambda: [processing.destroy(), callback()])

    @staticmethod
    def process_payment(amount, card_number, cvv, expiry_date, cardholder_name):
        """
        Process payment simulation.
        Returns True for success, False for failure.
        """
        print("\n[PAYMENT SIMULATION] Processing payment...")
        print(f"Amount: ${amount:.2f}")
        print(f"Card: **** **** **** {card_number[-4:]}")
        print(f"Cardholder: {cardholder_name}")
        print("[PAYMENT SIMULATION] Payment successful!")
        return True

    @staticmethod
    def validate_card_info(card_number, cvv, expiry_date):
        """
        Validate card information.
        Returns True if valid, False if not.
        """
        # Simple validation 
        if (len(card_number) == 16 and 
            len(cvv) == 3 and 
            len(expiry_date) == 5 and 
            expiry_date[2] == '/' and
            expiry_date[:2].isdigit() and 
            expiry_date[3:].isdigit()):
            return True
        return False

    @staticmethod
    def show_error(parent, message):
        """Display error message dialog"""
        error = ctk.CTkToplevel(parent)
        error.title("Error")
        error.geometry("300x150")
        error.transient(parent)
        error.grab_set()
        
        # Center window
        error.update_idletasks()
        x = (error.winfo_screenwidth() - error.winfo_width()) // 2
        y = (error.winfo_screenheight() - error.winfo_height()) // 2
        error.geometry(f"+{x}+{y}")
        
        # Error message
        message_label = ctk.CTkLabel(
            error,
            text=message,
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color="red",
            justify="center"
        )
        message_label.pack(expand=True)
        
        # OK button
        ok_btn = ctk.CTkButton(
            error,
            text="OK",
            fg_color="gray",
            hover_color="#666666",
            font=ctk.CTkFont(family="Roboto", size=14),
            width=100,
            command=error.destroy
        )
        ok_btn.pack(pady=20)
