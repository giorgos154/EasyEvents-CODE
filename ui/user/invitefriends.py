import customtkinter as ctk

class InviteFriendsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        # Kato container gia ti selida "Invite Friends" me moderne stiles kai Roboto font
        self.header = ctk.CTkLabel(self, text="Invite Friends", 
                                   font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        self.header.pack(pady=20, padx=20)
        
        # Container gia ta invitation options
        self.invite_frame = ctk.CTkFrame(self, fg_color="white")
        self.invite_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Section gia email invitation
        self.email_label = ctk.CTkLabel(self.invite_frame, text="Invite via Email:", 
                                        font=ctk.CTkFont(family="Roboto", size=16))
        self.email_label.pack(pady=(10,5), anchor="w")
        self.email_entry = ctk.CTkEntry(self.invite_frame, 
                                        placeholder_text="Enter email address",
                                        font=ctk.CTkFont(family="Roboto", size=14), width=300)
        self.email_entry.pack(pady=5, anchor="w")
        self.send_email_btn = ctk.CTkButton(self.invite_frame, text="Send Invitation  →", 
                                            fg_color="#C8A165", hover_color="#b38e58",
                                            font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                                            width=300, height=40, corner_radius=8, text_color="black")
        self.send_email_btn.pack(pady=10, anchor="w")
        
        # Section gia referral link
        self.link_label = ctk.CTkLabel(self.invite_frame, text="Share Referral Link:", 
                                      font=ctk.CTkFont(family="Roboto", size=16))
        self.link_label.pack(pady=(20,5), anchor="w")
        self.link_entry = ctk.CTkEntry(self.invite_frame, 
                                      placeholder_text="Your referral link", 
                                      font=ctk.CTkFont(family="Roboto", size=14), width=300)
        self.link_entry.pack(pady=5, anchor="w")
        self.copy_link_btn = ctk.CTkButton(self.invite_frame, text="Copy Link  →", 
                                           fg_color="#C8A165", hover_color="#b38e58",
                                           font=ctk.CTkFont(family="Roboto", size=14, weight="bold"),
                                           width=300, height=40, corner_radius=8, text_color="black")
        self.copy_link_btn.pack(pady=10, anchor="w")
        
        # Section gia invitation status (placeholder)
        self.status_label = ctk.CTkLabel(self.invite_frame, text="Invitation Status:", 
                                        font=ctk.CTkFont(family="Roboto", size=16))
        self.status_label.pack(pady=(20,5), anchor="w")
        self.status_info = ctk.CTkLabel(self.invite_frame, text="No invitations sent yet.", 
                                       font=ctk.CTkFont(family="Roboto", size=14))
        self.status_info.pack(pady=5, anchor="w")
        
        # Ta comments einai se greeklish gia na deixnoun tin leitourgia: 
        # H selida ayti epitrepei ston xristi na steilei invite via email h na koinopoihsei to referral link.
