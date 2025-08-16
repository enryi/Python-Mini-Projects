import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random
import string
import re
import hashlib
import requests
import threading
import time
import pyperclip
from datetime import datetime
import json

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernPasswordManager:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Password Manager")
        self.root.geometry("900x800")
        self.root.minsize(700, 600)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.generated_passwords = []
        self.current_password = tk.StringVar()
        self.strength_score = 0
        
        self.common_passwords = {
            "123456", "password", "123456789", "12345678", "12345", "1234567",
            "1234567890", "qwerty", "abc123", "million2", "000000", "1234",
            "iloveyou", "aaron431", "password1", "qqww1122", "123", "omgpop",
            "123321", "654321", "qwertyuiop", "qwer1234", "123abc", "123qwe"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        title_frame = ctk.CTkFrame(self.root, corner_radius=10)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🔐 Password Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        self.tabview = ctk.CTkTabview(self.root, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.generator_tab = self.tabview.add("🎲 Generator")
        self.checker_tab = self.tabview.add("🛡️ Security Check")
        self.history_tab = self.tabview.add("📊 History")
        
        self.setup_generator_tab()
        self.setup_checker_tab()
        self.setup_history_tab()
        
    def setup_generator_tab(self):
        self.generator_tab.grid_columnconfigure(0, weight=1)
        
        settings_frame = ctk.CTkFrame(self.generator_tab, corner_radius=10)
        settings_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        settings_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkLabel(settings_frame, text="⚙️ Password Settings", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 15), sticky="w", padx=15
        )
        
        ctk.CTkLabel(settings_frame, text="Length:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.length_slider = ctk.CTkSlider(settings_frame, from_=8, to=64, number_of_steps=56)
        self.length_slider.set(16)
        self.length_slider.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        
        self.length_label = ctk.CTkLabel(settings_frame, text="16")
        self.length_label.grid(row=2, column=1, padx=15, pady=0, sticky="w")
        self.length_slider.configure(command=self.update_length_label)
        
        options_frame = ctk.CTkFrame(settings_frame)
        options_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        options_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.use_uppercase = ctk.CTkCheckBox(options_frame, text="Uppercase (A-Z)")
        self.use_uppercase.select()
        self.use_uppercase.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.use_lowercase = ctk.CTkCheckBox(options_frame, text="Lowercase (a-z)")
        self.use_lowercase.select()
        self.use_lowercase.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.use_numbers = ctk.CTkCheckBox(options_frame, text="Numbers (0-9)")
        self.use_numbers.select()
        self.use_numbers.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.use_symbols = ctk.CTkCheckBox(options_frame, text="Symbols (!@#$%)")
        self.use_symbols.select()
        self.use_symbols.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        self.exclude_ambiguous = ctk.CTkCheckBox(options_frame, text="Exclude ambiguous (0,O,l,1)")
        self.exclude_ambiguous.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.no_repeats = ctk.CTkCheckBox(options_frame, text="No repeated characters")
        self.no_repeats.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        button_frame = ctk.CTkFrame(settings_frame)
        button_frame.grid(row=4, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        ctk.CTkButton(
            button_frame,
            text="🎲 Generate",
            command=self.generate_password,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2B7A2B",
            hover_color="#1E5F1E"
        ).grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        ctk.CTkButton(
            button_frame,
            text="📋 Copy",
            command=self.copy_password,
            height=40,
            fg_color="#1E5A96",
            hover_color="#144271"
        ).grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        ctk.CTkButton(
            button_frame,
            text="💾 Save",
            command=self.save_password,
            height=40,
            fg_color="#7B2D7B",
            hover_color="#5A1F5A"
        ).grid(row=0, column=2, padx=5, pady=10, sticky="ew")
        
        display_frame = ctk.CTkFrame(self.generator_tab, corner_radius=10)
        display_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 10))
        display_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(display_frame, text="🔑 Generated Password", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, pady=(15, 10), padx=15, sticky="w"
        )
        
        self.password_display = ctk.CTkTextbox(
            display_frame,
            height=60,
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            wrap="word"
        )
        self.password_display.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        
        strength_frame = ctk.CTkFrame(display_frame)
        strength_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        strength_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(strength_frame, text="Strength:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.strength_bar = ctk.CTkProgressBar(strength_frame, height=20)
        self.strength_bar.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.strength_bar.set(0)
        
        self.strength_label = ctk.CTkLabel(strength_frame, text="No password generated", text_color="gray")
        self.strength_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        multi_frame = ctk.CTkFrame(self.generator_tab, corner_radius=10)
        multi_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        multi_frame.grid_columnconfigure(0, weight=1)
        multi_frame.grid_rowconfigure(2, weight=1)
        
        ctk.CTkLabel(multi_frame, text="🎯 Bulk Generation", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, pady=(15, 10), padx=15, sticky="w"
        )
        
        bulk_controls = ctk.CTkFrame(multi_frame)
        bulk_controls.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        bulk_controls.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(bulk_controls, text="Count:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.count_entry = ctk.CTkEntry(bulk_controls, placeholder_text="10", width=80)
        self.count_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        ctk.CTkButton(
            bulk_controls,
            text="Generate Multiple",
            command=self.generate_multiple_passwords,
            fg_color="#B8860B",
            hover_color="#8B6914"
        ).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        
        self.multi_display = ctk.CTkTextbox(
            multi_frame,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.multi_display.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
    def setup_checker_tab(self):
        self.checker_tab.grid_columnconfigure(0, weight=1)
        
        input_frame = ctk.CTkFrame(self.checker_tab, corner_radius=10)
        input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(input_frame, text="🔍 Password Security Analysis", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, pady=(15, 15), padx=15, sticky="w"
        )
        
        self.check_entry = ctk.CTkTextbox(
            input_frame,
            height=80,
            font=ctk.CTkFont(family="Consolas", size=14)
        )
        self.check_entry.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="ew")
        self.check_entry.insert("1.0", "Enter password to analyze...")
        self.check_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        self.check_entry.bind("<FocusOut>", lambda e: self.restore_placeholder())

        button_check_frame = ctk.CTkFrame(input_frame)
        button_check_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        button_check_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            button_check_frame,
            text="🛡️ Check Security",
            command=self.check_password_security,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC143C",
            hover_color="#B22222"
        ).grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        ctk.CTkButton(
            button_check_frame,
            text="🌐 Check Breaches",
            command=self.check_password_breaches,
            height=40,
            fg_color="#FF8C00",
            hover_color="#FF7F00"
        ).grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        results_frame = ctk.CTkFrame(self.checker_tab, corner_radius=10)
        results_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(results_frame, text="📊 Analysis Results", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, pady=(15, 10), padx=15, sticky="w"
        )
        
        self.results_display = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.results_display.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        
    def setup_history_tab(self):
        self.history_tab.grid_columnconfigure(0, weight=1)
        self.history_tab.grid_rowconfigure(1, weight=1)
        
        controls_frame = ctk.CTkFrame(self.history_tab, corner_radius=10)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        controls_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(controls_frame, text="📝 Password History", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=(15, 15), padx=15, sticky="w"
        )
        
        ctk.CTkButton(
            controls_frame,
            text="🗑️ Clear History",
            command=self.clear_history,
            fg_color="#DC143C",
            hover_color="#B22222"
        ).grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
        
        ctk.CTkButton(
            controls_frame,
            text="💾 Export History",
            command=self.export_history,
            fg_color="#2B7A2B",
            hover_color="#1E5F1E"
        ).grid(row=1, column=2, padx=15, pady=(0, 15), sticky="e")
        
        history_frame = ctk.CTkFrame(self.history_tab, corner_radius=10)
        history_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(0, weight=1)
        
        self.history_display = ctk.CTkTextbox(
            history_frame,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.history_display.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
    def update_length_label(self, value):
        """Update length label"""
        self.length_label.configure(text=str(int(value)))
        
    def generate_password(self):
        """Generate a single password"""
        try:
            length = int(self.length_slider.get())
            
            chars = ""
            if self.use_lowercase.get():
                chars += string.ascii_lowercase
            if self.use_uppercase.get():
                chars += string.ascii_uppercase
            if self.use_numbers.get():
                chars += string.digits
            if self.use_symbols.get():
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
                
            if not chars:
                messagebox.showerror("Error", "Please select at least one character type")
                return
                
            if self.exclude_ambiguous.get():
                ambiguous = "0Ol1"
                chars = ''.join(c for c in chars if c not in ambiguous)
                
            if self.no_repeats.get() and len(chars) < length:
                messagebox.showerror("Error", "Cannot generate password without repeats: not enough unique characters")
                return
                
            password = ""
            used_chars = set()
            
            for _ in range(length):
                if self.no_repeats.get():
                    available_chars = [c for c in chars if c not in used_chars]
                    if not available_chars:
                        available_chars = list(chars)
                        used_chars.clear()
                    char = random.choice(available_chars)
                    used_chars.add(char)
                else:
                    char = random.choice(chars)
                password += char
                
            self.password_display.delete("1.0", "end")
            self.password_display.insert("1.0", password)
            
            self.analyze_password_strength(password)
            
            self.current_password.set(password)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
            
    def generate_multiple_passwords(self):
        """Generate multiple passwords"""
        try:
            count = int(self.count_entry.get() or "10")
            if count > 100:
                if not messagebox.askyesno("Confirm", "Generate more than 100 passwords? This might take a while."):
                    return
                    
            self.multi_display.delete("1.0", "end")
            self.multi_display.insert("end", f"Generating {count} passwords...\n\n")
            
            passwords = []
            for i in range(count):
                self.generate_password()
                password = self.current_password.get()
                if password:
                    passwords.append(f"{i+1:3d}. {password}")
                    
            self.multi_display.delete("1.0", "end")
            self.multi_display.insert("1.0", "\n".join(passwords))
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate passwords: {str(e)}")
            
    def analyze_password_strength(self, password):
        """Analyze password strength"""
        score = 0
        feedback = []
        
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            feedback.append("Consider using 12+ characters")
        else:
            score += 5
            feedback.append("Password too short (use 8+ characters)")
            
        if re.search(r'[a-z]', password):
            score += 5
        else:
            feedback.append("Add lowercase letters")
            
        if re.search(r'[A-Z]', password):
            score += 5
        else:
            feedback.append("Add uppercase letters")
            
        if re.search(r'\d', password):
            score += 5
        else:
            feedback.append("Add numbers")
            
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 10
        else:
            feedback.append("Add special characters")
            
        if not re.search(r'(.)\1{2,}', password):
            score += 10
        else:
            feedback.append("Avoid repeated characters")
            
        if not re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)', password.lower()):
            score += 10
        else:
            feedback.append("Avoid sequential patterns")
            
        if password.lower() not in self.common_passwords:
            score += 15
        else:
            score = min(score, 20)
            feedback.append("This is a common password!")
            
        if not re.search(r'\b(password|admin|user|login|welcome)\b', password.lower()):
            score += 10
        else:
            feedback.append("Avoid dictionary words")
            
        if len(set(password)) / len(password) > 0.7:
            score += 5
            
        score = min(score, 100)
        self.strength_score = score
        
        self.strength_bar.set(score / 100)
        
        if score >= 90:
            strength_text = "🛡️ Excellent"
            color = "#2B7A2B"
        elif score >= 75:
            strength_text = "💪 Strong"
            color = "#4CAF50"
        elif score >= 60:
            strength_text = "⚡ Good"
            color = "#FF9800"
        elif score >= 40:
            strength_text = "⚠️ Fair"
            color = "#FF5722"
        else:
            strength_text = "💀 Weak"
            color = "#DC143C"
            
        self.strength_label.configure(text=f"{strength_text} ({score}/100)", text_color=color)
        
    def check_password_security(self):
        """Comprehensive password security check"""
        password = self.check_entry.get("1.0", "end").strip()
        if not password:
            messagebox.showerror("Error", "Please enter a password to check")
            return
            
        self.results_display.delete("1.0", "end")
        self.results_display.insert("end", "🔍 SECURITY ANALYSIS REPORT\n")
        self.results_display.insert("end", "=" * 50 + "\n\n")
        
        self.analyze_password_strength(password)
        
        self.results_display.insert("end", f"📊 Overall Score: {self.strength_score}/100\n\n")
        
        self.results_display.insert("end", "🔤 CHARACTER ANALYSIS:\n")
        self.results_display.insert("end", f"   Length: {len(password)} characters\n")
        self.results_display.insert("end", f"   Unique chars: {len(set(password))}\n")
        self.results_display.insert("end", f"   Lowercase: {'✓' if re.search(r'[a-z]', password) else '✗'}\n")
        self.results_display.insert("end", f"   Uppercase: {'✓' if re.search(r'[A-Z]', password) else '✗'}\n")
        has_numbers = '✓' if re.search(r'\d', password) else '✗'
        has_symbols = '✓' if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password) else '✗'
        self.results_display.insert("end", f"   Numbers: {has_numbers}\n")
        self.results_display.insert("end", f"   Symbols: {has_symbols}\n\n")
        
        self.results_display.insert("end", "🚨 VULNERABILITY CHECKS:\n")
        
        vulnerabilities = []
        if password.lower() in self.common_passwords:
            vulnerabilities.append("⚠️ Common password detected")
        if re.search(r'(.)\1{2,}', password):
            vulnerabilities.append("⚠️ Contains repeated characters")
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            vulnerabilities.append("⚠️ Contains sequential numbers")
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            vulnerabilities.append("⚠️ Contains sequential letters")
        if re.search(r'\\b(password|admin|user|login|welcome|secret)\\b', password.lower()):
            vulnerabilities.append("⚠️ Contains dictionary words")
        if len(password) < 8:
            vulnerabilities.append("❌ Too short (minimum 8 characters)")
        if not re.search(r'[!@#$%^&*()_+\\-=\\[\\]{}|;:,.<>?]', password):
            vulnerabilities.append("⚠️ No special characters")
            
        if vulnerabilities:
            for vuln in vulnerabilities:
                self.results_display.insert("end", f"   {vuln}\n")
        else:
            self.results_display.insert("end", "   ✅ No major vulnerabilities detected\n")
            
        self.results_display.insert("end", "\n")
        
        self.results_display.insert("end", "⏱️ ESTIMATED CRACK TIMES:\n")
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\\d', password):
            charset_size += 10
        if re.search(r'[!@#$%^&*()_+\\-=\\[\\]{}|;:,.<>?]', password):
            charset_size += 32
            
        if charset_size > 0:
            combinations = charset_size ** len(password)
            
            seconds_slow = combinations / 1000
            seconds_fast = combinations / 1000000
            seconds_gpu = combinations / 1000000000
            
            self.results_display.insert("end", f"   Slow attack (1K/s): {self.format_time(seconds_slow)}\n")
            self.results_display.insert("end", f"   Fast attack (1M/s): {self.format_time(seconds_fast)}\n")
            self.results_display.insert("end", f"   GPU attack (1B/s): {self.format_time(seconds_gpu)}\n")
            
        self.results_display.insert("end", "\n")
        
        self.results_display.insert("end", "💡 RECOMMENDATIONS:\n")
        if self.strength_score >= 80:
            self.results_display.insert("end", "   ✅ This is a strong password!\n")
            self.results_display.insert("end", "   💡 Consider using a password manager\n")
        else:
            self.results_display.insert("end", "   🔄 Generate a new password with:\n")
            self.results_display.insert("end", "   • At least 12 characters\n")
            self.results_display.insert("end", "   • Mix of upper/lowercase letters\n")
            self.results_display.insert("end", "   • Numbers and special characters\n")
            self.results_display.insert("end", "   • No dictionary words or patterns\n")
            
    def check_password_breaches(self):
        """Check if password has been in data breaches (using k-anonymity)"""
        password = self.check_entry.get("1.0", "end").strip()
        if not password:
            messagebox.showerror("Error", "Please enter a password to check")
            return
            
        def check_in_thread():
            try:
                self.results_display.insert("end", "\n🌐 BREACH CHECK:\n")
                self.results_display.insert("end", "   Checking against known data breaches...\n")
                
                password_hash = hashlib.sha1(password.encode()).hexdigest().upper()
                prefix = password_hash[:5]
                suffix = password_hash[5:]
                
                response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=10)
                
                if response.status_code == 200:
                    hashes = response.text.split('\n')
                    found = False
                    
                    for hash_line in hashes:
                        if ':' in hash_line:
                            hash_suffix, count = hash_line.split(':')
                            if hash_suffix.strip() == suffix:
                                self.results_display.insert("end", f"   ❌ BREACH DETECTED! Found {count.strip()} times\n")
                                self.results_display.insert("end", "   🚨 This password has been compromised!\n")
                                self.results_display.insert("end", "   💡 Change this password immediately\n")
                                found = True
                                break
                    
                    if not found:
                        self.results_display.insert("end", "   ✅ Not found in known breaches\n")
                        self.results_display.insert("end", "   💡 This is good, but still use strong passwords\n")
                else:
                    self.results_display.insert("end", "   ❌ Could not check breaches (API error)\n")
                    
            except requests.RequestException:
                self.results_display.insert("end", "   ❌ Network error - could not check breaches\n")
            except Exception as e:
                self.results_display.insert("end", f"   ❌ Error checking breaches: {str(e)}\n")
                
        threading.Thread(target=check_in_thread, daemon=True).start()
        
    def format_time(self, seconds):
        """Format time in human readable format"""
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds/3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds/86400)} days"
        elif seconds < 31536000000:
            return f"{int(seconds/31536000)} years"
        else:
            return "Practically unbreakable"
            
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_display.get("1.0", "end").strip()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password to copy")
            
    def save_password(self):
        """Save password to history"""
        password = self.password_display.get("1.0", "end").strip()
        if password:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {
                "password": password,
                "timestamp": timestamp,
                "strength": self.strength_score,
                "length": len(password)
            }
            
            self.generated_passwords.append(entry)
            self.update_history_display()
            messagebox.showinfo("Success", "Password saved to history!")
        else:
            messagebox.showerror("Error", "No password to save")
            
    def update_history_display(self):
        """Update the history display"""
        self.history_display.delete("1.0", "end")
        
        if not self.generated_passwords:
            self.history_display.insert("1.0", "No passwords in history yet.\n\nGenerate some passwords and save them to see them here!")
            return
            
        self.history_display.insert("end", f"📊 PASSWORD HISTORY ({len(self.generated_passwords)} entries)\n")
        self.history_display.insert("end", "=" * 60 + "\n\n")
        
        for i, entry in enumerate(reversed(self.generated_passwords), 1):
            strength_emoji = "🛡️" if entry["strength"] >= 80 else "💪" if entry["strength"] >= 60 else "⚠️" if entry["strength"] >= 40 else "💀"
            
            self.history_display.insert("end", f"{i:2d}. {entry['timestamp']}\n")
            self.history_display.insert("end", f"    Password: {entry['password']}\n")
            self.history_display.insert("end", f"    Strength: {strength_emoji} {entry['strength']}/100 | Length: {entry['length']}\n")
            self.history_display.insert("end", "\n")
            
    def clear_history(self):
        """Clear password history"""
        if self.generated_passwords:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all password history?"):
                self.generated_passwords.clear()
                self.update_history_display()
                messagebox.showinfo("Success", "History cleared!")
        else:
            messagebox.showinfo("Info", "History is already empty!")
            
    def export_history(self):
        """Export history to file"""
        if not self.generated_passwords:
            messagebox.showinfo("Info", "No history to export!")
            return
            
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Password History"
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump(self.generated_passwords, f, indent=2)
                else:
                    with open(filename, 'w') as f:
                        f.write(f"Password History Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("=" * 60 + "\n\n")
                        
                        for i, entry in enumerate(self.generated_passwords, 1):
                            f.write(f"{i:2d}. {entry['timestamp']}\n")
                            f.write(f"    Password: {entry['password']}\n")
                            f.write(f"    Strength: {entry['strength']}/100 | Length: {entry['length']}\n")
                            f.write("\n")
                            
                messagebox.showinfo("Success", f"History exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history: {str(e)}")
                
    def run(self):
        """Start the application"""
        self.update_history_display()
        
        self.root.mainloop()

if __name__ == "__main__":
    required_packages = {
        'customtkinter': 'customtkinter',
        'pyperclip': 'pyperclip',
        'requests': 'requests'
    }
    
    missing_packages = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    if missing_packages:
        print("Missing required packages. Please install:")
        print(f"pip install {' '.join(missing_packages)}")
        exit(1)
    
    app = ModernPasswordManager()
    app.run()