class PaymentHandler:
    """
    PaymentHandler: Klasi gia tin diaxeirisi plirwmwn.
    Pros to paron einai apli ylopoiisi gia dokimes.
    """
    @staticmethod
    def process_payment(amount, card_number, cvv, expiry_date, cardholder_name):
        """
        Prosomiwsi epeksergasias plirwmis.
        Epistrefei True gia epitixia, False gia apotixia.
        """
        print("\n[PAYMENT SIMULATION] Processing payment...")
        print(f"Amount: €{amount:.2f}")
        print(f"Card: **** **** **** {card_number[-4:]}")
        print(f"Cardholder: {cardholder_name}")
        print("[PAYMENT SIMULATION] Payment successful!")
        return True

    @staticmethod
    def validate_card_info(card_number, cvv, expiry_date):
        """
        Elegxos egkirotitas stoixeiwn kartas.
        Epistrefei True an ta stoixeia einai egkira, False an oxi.
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
