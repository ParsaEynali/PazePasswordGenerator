import os
import sys
import time
import random
import string
from dataclasses import dataclass, field
from typing import List, Optional, Dict

try:
    import winsound
except ImportError:
    winsound = None

from colorama import init, Fore, Style

init(autoreset=True)


# =========================
# Data Model
# =========================
@dataclass
class PasswordEntry:
    name: str
    password: str
    strength_level: int = 0 # 0: Unknown, 1: Weak, 2: Medium, 3: Strong, 4: Very Strong, 5: Excellent

    def __str__(self):
        strength_map = {
            0: "Unknown",
            1: "Weak",
            2: "Medium",
            3: "Strong",
            4: "Very Strong",
            5: "Excellent"
        }
        lang = getattr(PasswordApp, '_current_lang_manager', LanguageManager()).lang # Access current language
        if lang == "fa":
            strength_map_fa = {
                0: "ناشناخته",
                1: "ضعیف",
                2: "متوسط",
                3: "قوی",
                4: "بسیار قوی",
                5: "عالی"
            }
            strength_map = strength_map_fa

        strength_color = {
            1: Fore.RED, 2: Fore.YELLOW, 3: Fore.CYAN, 4: Fore.BLUE, 5: Fore.GREEN, 0: Fore.WHITE
        }
        return f"{self.name} : {strength_color[self.strength_level]}{strength_map[self.strength_level]}{Style.RESET_ALL} [{self.password}]"


# =========================
# Language Manager
# =========================
class LanguageManager:
    _instance = None

    def __new__(cls): # Singleton pattern
        if cls._instance is None:
            cls._instance = super(LanguageManager, cls).__new__(cls)
            cls._instance.lang = "en"
            cls._instance.texts = {
                "en": {
                    "welcome": "Password Generator Pro",
                    "menu": "Main Menu",
                    "generate": "Generate Password",
                    "manage": "Manage Saved Passwords",
                    "settings": "Settings",
                    "exit": "Exit",
                    "choice": "Enter your choice: ",
                    "name": "Enter password name: ",
                    "level": "Choose password level (1-5): ",
                    "custom": "Custom generation",
                    "length": "Password length: ",
                    "use_lower": "Use lowercase? (y/n): ",
                    "use_upper": "Use uppercase? (y/n): ",
                    "use_digits": "Use digits? (y/n): ",
                    "use_symbols": "Use symbols? (y/n): ",
                    "saved": "Password saved successfully.",
                    "generated": "Generated password",
                    "invalid": "Invalid input.",
                    "back": "Press Enter to return...",
                    "file_missing": "No saved password file found.",
                    "saved_menu": "Saved Password Manager",
                    "view_all": "View all",
                    "search": "Search by name",
                    "delete": "Delete by name",
                    "edit": "Edit by name",
                    "copy": "Display for copy",
                    "load_failed": "Failed to load saved passwords.",
                    "not_found": "No matching entry found.",
                    "deleted": "Entry deleted.",
                    "updated": "Entry updated.",
                    "language": "Select language",
                    "lang_en": "English",
                    "lang_fa": "Persian",
                    "confirm": "Are you sure? (y/n): ",
                    "empty": "No entries found.",
                    "enter_search": "Enter search term: ",
                    "enter_delete": "Enter name to delete: ",
                    "enter_edit": "Enter name to edit: ",
                    "strength_meter": "Password Strength:",
                    "weak": "Weak", "medium": "Medium", "strong": "Strong", "very_strong": "Very Strong", "excellent": "Excellent",
                    "unknown": "Unknown",
                    "strength_levels": {1: "Weak", 2: "Medium", 3: "Strong", 4: "Very Strong", 5: "Excellent"},
                    "strength_levels_fa": {1: "ضعیف", 2: "متوسط", 3: "قوی", 4: "بسیار قوی", 5: "عالی"},
                    "strength_colors": {1: Fore.RED, 2: Fore.YELLOW, 3: Fore.CYAN, 4: Fore.BLUE, 5: Fore.GREEN, 0: Fore.WHITE}
                },
                "fa": {
                    "welcome": "پروژه حرفه‌ای تولید رمز عبور",
                    "menu": "منوی اصلی",
                    "generate": "تولید پسورد",
                    "manage": "مدیریت پسوردهای ذخیره‌شده",
                    "settings": "تنظیمات",
                    "exit": "خروج",
                    "choice": "انتخاب شما: ",
                    "name": "نام پسورد را وارد کنید: ",
                    "level": "سطح پسورد را انتخاب کنید (1-5): ",
                    "custom": "تولید سفارشی",
                    "length": "طول پسورد: ",
                    "use_lower": "حروف کوچک استفاده شود؟ (y/n): ",
                    "use_upper": "حروف بزرگ استفاده شود؟ (y/n): ",
                    "use_digits": "عدد استفاده شود؟ (y/n): ",
                    "use_symbols": "نمادها استفاده شوند؟ (y/n): ",
                    "saved": "پسورد با موفقیت ذخیره شد.",
                    "generated": "پسورد تولید شده",
                    "invalid": "ورودی نامعتبر است.",
                    "back": "برای بازگشت Enter را بزنید...",
                    "file_missing": "فایل پسوردهای ذخیره‌شده پیدا نشد.",
                    "saved_menu": "مدیریت پسوردهای ذخیره‌شده",
                    "view_all": "مشاهده همه",
                    "search": "جستجو بر اساس نام",
                    "delete": "حذف بر اساس نام",
                    "edit": "ویرایش بر اساس نام",
                    "copy": "نمایش برای کپی",
                    "load_failed": "بارگذاری پسوردها ناموفق بود.",
                    "not_found": "موردی یافت نشد.",
                    "deleted": "مورد حذف شد.",
                    "updated": "مورد بروزرسانی شد.",
                    "language": "انتخاب زبان",
                    "lang_en": "انگلیسی",
                    "lang_fa": "فارسی",
                    "confirm": "آیا مطمئن هستید؟ (y/n): ",
                    "empty": "موردی وجود ندارد.",
                    "enter_search": "عبارت جستجو را وارد کنید: ",
                    "enter_delete": "نام مورد برای حذف را وارد کنید: ",
                    "enter_edit": "نام مورد برای ویرایش را وارد کنید: ",
                    "strength_meter": "سطح امنیت پسورد:",
                    "weak": "ضعیف", "medium": "متوسط", "strong": "قوی", "very_strong": "بسیار قوی", "excellent": "عالی",
                    "unknown": "ناشناخته",
                    "strength_levels": {1: "ضعیف", 2: "متوسط", 3: "قوی", 4: "بسیار قوی", 5: "عالی"},
                    "strength_levels_fa": {1: "ضعیف", 2: "متوسط", 3: "قوی", 4: "بسیار قوی", 5: "عالی"},
                    "strength_colors": {1: Fore.RED, 2: Fore.YELLOW, 3: Fore.CYAN, 4: Fore.BLUE, 5: Fore.GREEN, 0: Fore.WHITE}
                }
            }
        return cls._instance

    def set_language(self, choice: str):
        self.lang = "fa" if choice == "2" else "en"

    def t(self, key: str) -> str:
        return self.texts[self.lang].get(key, key) # Use .get to avoid KeyError, return key if not found

    def get_strength_text(self, level: int, lang_key: str = "strength_levels") -> str:
        texts_dict = self.texts[self.lang].get(lang_key, {})
        return texts_dict.get(level, self.t("unknown"))

    def get_strength_color(self, level: int) -> str:
        return self.texts[self.lang]["strength_colors"].get(level, Fore.WHITE)


# =========================
# UI Manager
# =========================
class UIManager:
    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pause(message="Press Enter to continue..."):
        input(Fore.CYAN + message)

    @staticmethod
    def beep():
        if winsound:
            try:
                winsound.Beep(900, 100)
            except Exception:
                pass

    @staticmethod
    def slow_effect(text: str, color=Fore.CYAN, delay=0.01):
        for ch in text:
            print(color + ch + Style.RESET_ALL, end="", flush=True)
            time.sleep(delay)
        print()

    @staticmethod
    def print_banner(lang_manager: LanguageManager):
        UIManager.clear()
        title = lang_manager.t("welcome")
        banner = f"""
{Fore.GREEN}╔══════════════════════════════════════════════╗
{Fore.GREEN}║{Fore.YELLOW}        ██████╗  █████╗ ███████╗███████╗       {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}        ██╔══██╗██╔══██╗╚══███╔╝██╔════╝       {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}        ██████╔╝███████║  ███╔╝ █████╗         {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}        ██╔═══╝ ██╔══██║ ███╔╝  ██╔══╝         {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}        ██║     ██║  ██║███████╗███████╗       {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}        ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝       {Fore.GREEN}║
{Fore.GREEN}║{Fore.CYAN}          {title:<38}{Fore.GREEN}║
{Fore.GREEN}╚══════════════════════════════════════════════╝
"""
        print(banner)

    @staticmethod
    def menu_box(title: str, options: List[str]) -> None:
        width = max(len(title) + 6, max(len(opt) for opt in options) + 8)
        print(Fore.GREEN + "╔" + "═" * width + "╗")
        print(Fore.GREEN + f"║{Fore.YELLOW}{title.center(width)}{Fore.GREEN}║")
        print(Fore.GREEN + "╠" + "═" * width + "╣")
        for idx, opt in enumerate(options, 1):
            line = f"{idx}. {opt}"
            print(Fore.GREEN + f"║{Fore.CYAN}{line.ljust(width)}{Fore.GREEN}║")
        print(Fore.GREEN + "╚" + "═" * width + "╝")

    @staticmethod
    def display_password_entry(entry: PasswordEntry, lang_manager: LanguageManager):
        strength_text = lang_manager.get_strength_text(entry.strength_level)
        strength_color = lang_manager.get_strength_color(entry.strength_level)
        print(f"{entry.name} : {strength_color}{strength_text}{Style.RESET_ALL} [{entry.password}]")


# =========================
# Password Manager
# =========================
class PasswordManager:
    def __init__(self, filename="pass.txt"):
        self.filename = filename
        self.entries: List[PasswordEntry] = []
        self.load()

    def load(self):
        self.entries = []
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if " : " in line:
                        parts = line.split(" : ", 2)
                        name = parts[0]
                        password = parts[1]
                        strength_level = 0
                        if len(parts) == 3:
                            try:
                                strength_level = int(parts[2])
                            except ValueError:
                                pass # Ignore if strength level is not an int
                        self.entries.append(PasswordEntry(name=name, password=password, strength_level=strength_level))
        except Exception as e:
            print(f"Error loading passwords: {e}")
            self.entries = []

    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for entry in self.entries:
                    f.write(f"{entry.name} : {entry.password} : {entry.strength_level}\n")
        except Exception as e:
            print(f"Error saving passwords: {e}")


    def add(self, name: str, password: str, strength_level: int):
        self.entries.append(PasswordEntry(name, password, strength_level))
        self.save()

    def list_all(self) -> List[PasswordEntry]:
        return self.entries

    def search(self, term: str) -> List[PasswordEntry]:
        term = term.lower()
        return [e for e in self.entries if term in e.name.lower()]

    def delete(self, name: str) -> bool:
        before = len(self.entries)
        self.entries = [e for e in self.entries if e.name.lower() != name.lower()]
        if len(self.entries) != before:
            self.save()
            return True
        return False

    def update(self, old_name: str, new_name: str, new_password: str, new_strength_level: int) -> bool:
        for entry in self.entries:
            if entry.name.lower() == old_name.lower():
                entry.name = new_name
                entry.password = new_password
                entry.strength_level = new_strength_level
                self.save()
                return True
        return False

    def get_by_name(self, name: str) -> Optional[PasswordEntry]:
        for entry in self.entries:
            if entry.name.lower() == name.lower():
                return entry
        return None


# =========================
# Generator Engine
# =========================
class PasswordGenerator:
    LEVELS: Dict[int, Dict] = {
        1: {"length": 8,  "lower": True,  "upper": False, "digits": True,  "symbols": False},
        2: {"length": 10, "lower": True,  "upper": True,   "digits": True,  "symbols": False},
        3: {"length": 12, "lower": True,  "upper": True,   "digits": True,  "symbols": True},
        4: {"length": 16, "lower": True,  "upper": True,   "digits": True,  "symbols": True},
        5: {"length": 20, "lower": True,  "upper": True,   "digits": True,  "symbols": True},
    }

    def generate(self, length: int, lower: bool, upper: bool, digits: bool, symbols: bool) -> Optional[str]:
        charset = ""
        pools = []

        if lower:
            charset += string.ascii_lowercase
            pools.append(string.ascii_lowercase)
        if upper:
            charset += string.ascii_uppercase
            pools.append(string.ascii_uppercase)
        if digits:
            charset += string.digits
            pools.append(string.digits)
        if symbols:
            sym = "!@#$%^&*()-_=+[]{};:,.?/<>"
            charset += sym
            pools.append(sym)

        if not charset or length < len(pools):
            return None

        password_list = []
        # Ensure at least one of each selected character type
        for pool in pools:
            password_list.append(random.choice(pool))

        # Fill the rest of the password length
        while len(password_list) < length:
            password_list.append(random.choice(charset))

        random.shuffle(password_list)
        return "".join(password_list)

    def get_strength_level(self, password: str) -> int:
        length = len(password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digits = any(c in string.digits for c in password)
        has_symbols = any(c in "!@#$%^&*()-_=+[]{};:,.?/<>" for c in password)

        score = 0
        if length >= 8: score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1

        if has_lower: score += 1
        if has_upper: score += 1
        if has_digits: score += 1
        if has_symbols: score += 1

        # Map score to levels 1-5
        if score <= 2: return 1 # Weak
        if score <= 4: return 2 # Medium
        if score <= 6: return 3 # Strong
        if score <= 8: return 4 # Very Strong
        return 5 # Excellent

    def fake_hard_generate(self, lang_manager: LanguageManager):
        msgs = {
            "en": [
                "Initializing entropy engine...",
                "Scanning secure patterns...",
                "Mixing random seeds...",
                "Applying complexity rules...",
                "Finalizing output..."
            ],
            "fa": [
                "راه‌اندازی موتور تصادفی...",
                "بررسی الگوهای امن...",
                "ترکیب منابع تصادفی...",
                "اعمال قوانین پیچیدگی...",
                "نهایی‌سازی خروجی..."
            ]
        }

        current_msgs = msgs[lang_manager.lang]
        for msg in current_msgs:
            for dots in [".", "..", "...", "...."]:
                print(Fore.MAGENTA + f"\r{msg}{dots}   ", end="", flush=True)
                time.sleep(0.18)
        print("\r" + " " * 70, end="\r")


# =========================
# App
# =========================
class PasswordApp:
    _current_lang_manager = None # Static variable for language manager

    def __init__(self):
        self.lang_manager = LanguageManager()
        PasswordApp._current_lang_manager = self.lang_manager # Set static variable
        self.ui = UIManager()
        self.db = PasswordManager()
        self.generator = PasswordGenerator()

    def run(self):
        self.lang_manager.set_language("1") # Default to English
        self.lang_manager.lang = "en" # Ensure default is set
        
        while True:
            self.ui.print_banner(self.lang_manager)
            options = [
                self.lang_manager.t("generate"),
                self.lang_manager.t("manage"),
                self.lang_manager.t("settings"),
                self.lang_manager.t("exit"),
            ]
            self.ui.menu_box(self.lang_manager.t("menu"), options)
            choice = input(Fore.WHITE + self.lang_manager.t("choice")).strip()

            if choice == "1":
                self.generate_flow()
            elif choice == "2":
                self.manage_flow()
            elif choice == "3":
                self.settings_flow()
            elif choice == "4":
                self.ui.clear()
                print(Fore.YELLOW + ("Goodbye!" if self.lang_manager.lang == "en" else "خدانگهدار!"))
                time.sleep(0.7)
                break
            else:
                print(Fore.RED + self.lang_manager.t("invalid"))
                time.sleep(1)

    def generate_flow(self):
        self.ui.clear()
        print(Fore.YELLOW + self.lang_manager.t("generate"))
        name = input(Fore.CYAN + self.lang_manager.t("name")).strip() or "Unnamed"

        level_choice = input(Fore.CYAN + self.lang_manager.t("level")).strip()

        length, lower, upper, digits, symbols = 0, False, False, False, False

        if level_choice in ["1", "2", "3", "4", "5"]:
            cfg = self.generator.LEVELS[int(level_choice)]
            length = cfg["length"]
            lower = cfg["lower"]
            upper = cfg["upper"]
            digits = cfg["digits"]
            symbols = cfg["symbols"]
        elif level_choice == "6":
            while True:
                try:
                    length = int(input(Fore.CYAN + self.lang_manager.t("length")))
                    if length < 4: raise ValueError
                    break
                except ValueError:
                    print(Fore.RED + self.lang_manager.t("invalid"))

            def yn(prompt):
                while True:
                    ans = input(Fore.WHITE + prompt).strip().lower()
                    if ans in ["y", "yes", "1", ""]: return True
                    if ans in ["n", "no", "0"]: return False
                    print(Fore.RED + self.lang_manager.t("invalid"))

            lower = yn(self.lang_manager.t("use_lower"))
            upper = yn(self.lang_manager.t("use_upper"))
            digits = yn(self.lang_manager.t("use_digits"))
            symbols = yn(self.lang_manager.t("use_symbols"))
        else:
            print(Fore.RED + self.lang_manager.t("invalid"))
            time.sleep(1)
            return

        self.generator.fake_hard_generate(self.lang_manager)
        password = self.generator.generate(length, lower, upper, digits, symbols)

        if not password:
            print(Fore.RED + self.lang_manager.t("invalid"))
            self.ui.pause(self.lang_manager.t("back"))
            return

        strength_level = self.generator.get_strength_level(password)
        strength_text = self.lang_manager.get_strength_text(strength_level)
        strength_color = self.lang_manager.get_strength_color(strength_level)

        print(Fore.GREEN + f"\n{self.lang_manager.t('generated')}:")
        print(f"{name} : {strength_color}{strength_text}{Style.RESET_ALL} [{password}]")

        self.db.add(name, password, strength_level)
        print(Fore.CYAN + self.lang_manager.t("saved"))
        self.ui.beep()
        self.ui.beep()
        self.ui.pause(self.lang_manager.t("back"))

    def manage_flow(self):
        while True:
            self.ui.clear()
            options = [
                self.lang_manager.t("view_all"),
                self.lang_manager.t("search"),
                self.lang_manager.t("delete"),
                self.lang_manager.t("edit"),
                self.lang_manager.t("copy"),
                self.lang_manager.t("back"),
            ]
            self.ui.menu_box(self.lang_manager.t("saved_menu"), options)
            choice = input(Fore.WHITE + self.lang_manager.t("choice")).strip()

            if choice == "1":
                self.view_all()
            elif choice == "2":
                self.search_entry()
            elif choice == "3":
                self.delete_entry()
            elif choice == "4":
                self.edit_entry()
            elif choice == "5":
                self.display_for_copy()
            elif choice == "6":
                break
            else:
                print(Fore.RED + self.lang_manager.t("invalid"))
                time.sleep(1)

    def view_all(self):
        self.ui.clear()
        print(Fore.YELLOW + self.lang_manager.t("saved_menu"))
        if not self.db.entries:
            print(Fore.RED + self.lang_manager.t("empty"))
        else:
            for i, e in enumerate(self.db.entries, 1):
                UIManager.display_password_entry(e, self.lang_manager)
        self.ui.pause(self.lang_manager.t("back"))

    def search_entry(self):
        self.ui.clear()
        term = input(Fore.CYAN + self.lang_manager.t("enter_search")).strip()
        results = self.db.search(term)
        print(Fore.YELLOW + self.lang_manager.t("search"))
        if not results:
            print(Fore.RED + self.lang_manager.t("not_found"))
        else:
            for i, e in enumerate(results, 1):
                UIManager.display_password_entry(e, self.lang_manager)
        self.ui.pause(self.lang_manager.t("back"))

    def delete_entry(self):
        self.ui.clear()
        name = input(Fore.CYAN + self.lang_manager.t("enter_delete")).strip()
        if not name: return

        entry_to_delete = self.db.get_by_name(name)
        if entry_to_delete:
            print(Fore.YELLOW + f"Entry: {entry_to_delete.name} : {entry_to_delete.password}")
            confirm = input(Fore.WHITE + self.lang_manager.t("confirm")).strip().lower()
            if confirm == 'y':
                if self.db.delete(name):
                    print(Fore.GREEN + self.lang_manager.t("deleted"))
                else:
                    print(Fore.RED + self.lang_manager.t("not_found")) # Should not happen if entry_to_delete exists
            else:
                print(Fore.CYAN + "Operation cancelled.")
        else:
            print(Fore.RED + self.lang_manager.t("not_found"))
        self.ui.pause(self.lang_manager.t("back"))

    def edit_entry(self):
        self.ui.clear()
        old_name = input(Fore.CYAN + self.lang_manager.t("enter_edit")).strip()
        entry = self.db.get_by_name(old_name)
        if not entry:
            print(Fore.RED + self.lang_manager.t("not_found"))
            self.ui.pause(self.lang_manager.t("back"))
            return

        print(Fore.CYAN + f"Current: {entry.name} : {entry.password}")
        new_name = input(Fore.CYAN + f"New name (leave blank to keep '{entry.name}'): ").strip() or entry.name
        
        # Offer to regenerate or keep existing
        regen_choice = input(Fore.CYAN + "Do you want to regenerate the password? (y/n, default n): ").strip().lower()
        new_password = entry.password
        strength_level = entry.strength_level
        
        if regen_choice == 'y':
            print(Fore.YELLOW + "\nEnter new details for regeneration:")
            level_choice = input(Fore.CYAN + self.lang_manager.t("level")).strip()

            length, lower, upper, digits, symbols = 0, False, False, False, False

            if level_choice in ["1", "2", "3", "4", "5"]:
                cfg = self.generator.LEVELS[int(level_choice)]
                length = cfg["length"]
                lower = cfg["lower"]
                upper = cfg["upper"]
                digits = cfg["digits"]
                symbols = cfg["symbols"]
            elif level_choice == "6":
                while True:
                    try:
                        length = int(input(Fore.CYAN + self.lang_manager.t("length")))
                        if length < 4: raise ValueError
                        break
                    except ValueError:
                        print(Fore.RED + self.lang_manager.t("invalid"))

                def yn(prompt):
                    while True:
                        ans = input(Fore.WHITE + prompt).strip().lower()
                        if ans in ["y", "yes", "1", ""]: return True
                        if ans in ["n", "no", "0"]: return False
                        print(Fore.RED + self.lang_manager.t("invalid"))

                lower = yn(self.lang_manager.t("use_lower"))
                upper = yn(self.lang_manager.t("use_upper"))
                digits = yn(self.lang_manager.t("use_digits"))
                symbols = yn(self.lang_manager.t("use_symbols"))
            else:
                print(Fore.RED + self.lang_manager.t("invalid"))
                time.sleep(1)
                return

            self.generator.fake_hard_generate(self.lang_manager)
            new_password = self.generator.generate(length, lower, upper, digits, symbols)
            if not new_password:
                print(Fore.RED + self.lang_manager.t("invalid"))
                self.ui.pause(self.lang_manager.t("back"))
                return
            strength_level = self.generator.get_strength_level(new_password)
            
        if self.db.update(old_name, new_name, new_password, strength_level):
            print(Fore.GREEN + self.lang_manager.t("updated"))
        else:
            print(Fore.RED + self.lang_manager.t("not_found")) # Should not happen if entry exists

        self.ui.pause(self.lang_manager.t("back"))


    def display_for_copy(self):
        self.ui.clear()
        if not self.db.entries:
            print(Fore.RED + self.lang_manager.t("empty"))
        else:
            print(Fore.YELLOW + self.lang_manager.t("copy"))
            for i, e in enumerate(self.db.entries, 1):
                print(f"{e.name} : {e.password}") # Plain text for easy copy
            print(Fore.CYAN + "\n(For actual display with strength, use 'View all' option)")
        self.ui.pause(self.lang_manager.t("back"))

    def settings_flow(self):
        self.ui.clear()
        print(Fore.YELLOW + self.lang_manager.t("settings"))
        print(Fore.CYAN + "1. English")
        print(Fore.CYAN + "2. فارسی")
        choice = input(Fore.WHITE + self.lang_manager.t("choice")).strip()
        if choice in ["1", "2"]:
            self.lang_manager.set_language(choice)
            PasswordApp._current_lang_manager = self.lang_manager # Update static variable
        else:
            print(Fore.RED + self.lang_manager.t("invalid"))
            time.sleep(1)


if __name__ == "__main__":
    app = PasswordApp()
    app.run()
