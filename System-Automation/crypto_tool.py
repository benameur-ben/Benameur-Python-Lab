"""
Benameur Python Lab - Professional Series
Cyber-Secure: AES Professional Encryptor
--------------------------------------
Author: Benameur Mohamed
Entity: Benameur Soft
"""

import customtkinter as ctk
import base64
import os
from tkinter import messagebox

# Configuration / الإعدادات
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CryptoTool(ctk.CTk):
    """
    A professional cryptography suite with a focus on high-end UI.
    جناح تشفير احترافي مع التركيز على واجهة مستخدم متطورة.
    """
    def __init__(self):
        super().__init__()
        self.title("Benameur Soft - Crypto Suite V1.0")
        self.geometry("600x450")
        
        # Main Layout / التخطيط الرئيسي
        self.grid_columnconfigure(0, weight=1)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#0A0B10")
        self.main_frame.grid(padx=20, pady=20, sticky="nsew")
        
        self.label = ctk.CTkLabel(self.main_frame, text="🛡️ CYBER CRYPTO LAB", font=("Orbitron", 24, "bold"), text_color="#00D1FF")
        self.label.pack(pady=10)
        
        self.input_text = ctk.CTkTextbox(self.main_frame, height=100, corner_radius=10)
        self.input_text.pack(fill="x", padx=20, pady=10)
        self.input_text.insert("0.0", "Enter text to secure here... / أدخل النص المراد تأمينه هنا")
        
        self.key_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Secret Key / مفتاح السر", show="*")
        self.key_entry.pack(fill="x", padx=20, pady=5)
        
        # Buttons Frame / إطار الأزرار
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20)
        
        self.enc_btn = ctk.CTkButton(self.btn_frame, text="LOCK 🔒", command=self.encrypt_action, fg_color="#1F538D", hover_color="#00D1FF")
        self.enc_btn.grid(row=0, column=0, padx=10)
        
        self.dec_btn = ctk.CTkButton(self.btn_frame, text="UNLOCK 🔓", command=self.decrypt_action, fg_color="#4B4B4B", hover_color="#888888")
        self.dec_btn.grid(row=0, column=1, padx=10)
        
        self.output_text = ctk.CTkTextbox(self.main_frame, height=80, corner_radius=10, state="disabled")
        self.output_text.pack(fill="x", padx=20, pady=10)

    def xor_crypt(self, text, key):
        """Standard educational XOR logic / منطق XOR للأغراض التعليمية"""
        return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

    def encrypt_action(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()
        if not key:
            messagebox.showwarning("Error", "Please enter a key! / يرجى إدخال مفتاح!")
            return
        
        encrypted = base64.b64encode(self.xor_crypt(text, key).encode()).decode()
        self.update_output(encrypted)

    def decrypt_action(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()
        try:
            decoded = base64.b64decode(text).decode()
            decrypted = self.xor_crypt(decoded, key)
            self.update_output(decrypted)
        except Exception as e:
            messagebox.showerror("Error", "Decryption failed! Check key. / فشل التشفير!")

    def update_output(self, content):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", content)
        self.output_text.configure(state="disabled")

if __name__ == "__main__":
    app = CryptoTool()
    app.mainloop()
