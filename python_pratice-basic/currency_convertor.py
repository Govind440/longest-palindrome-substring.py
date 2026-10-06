import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3
import threading
from datetime import datetime
import json
import os

APP_TITLE = "Nova Currency Converter"
DB_FILE = "currency_history.db"
SETTINGS_FILE = "currency_settings.json"

API_URL = "https://open.er-api.com/v6/latest/{}"

CURRENCIES = {
    "USD": "US Dollar",
    "INR": "Indian Rupee",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "HKD": "Hong Kong Dollar",
    "SGD": "Singapore Dollar",
    "NZD": "New Zealand Dollar",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "DKK": "Danish Krone",
    "KRW": "South Korean Won",
    "AED": "UAE Dirham",
    "SAR": "Saudi Riyal",
    "QAR": "Qatari Riyal",
    "KWD": "Kuwaiti Dinar",
    "BHD": "Bahraini Dinar",
    "OMR": "Omani Rial",
    "ZAR": "South African Rand",
    "BRL": "Brazilian Real",
    "MXN": "Mexican Peso",
    "RUB": "Russian Ruble",
    "TRY": "Turkish Lira",
    "THB": "Thai Baht",
    "MYR": "Malaysian Ringgit",
    "IDR": "Indonesian Rupiah",
    "PHP": "Philippine Peso",
    "VND": "Vietnamese Dong",
    "PKR": "Pakistani Rupee",
    "BDT": "Bangladeshi Taka",
    "LKR": "Sri Lankan Rupee",
    "NPR": "Nepalese Rupee",
    "EGP": "Egyptian Pound",
    "ILS": "Israeli New Shekel",
    "PLN": "Polish Zloty",
    "CZK": "Czech Koruna",
    "HUF": "Hungarian Forint",
    "RON": "Romanian Leu",
}

SYMBOLS = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "KRW": "₩",
    "RUB": "₽",
    "TRY": "₺",
    "THB": "฿",
}

OFFLINE_RATES_FROM_USD = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 150.0,
    "AUD": 1.50,
    "CAD": 1.36,
    "CHF": 0.89,
    "CNY": 7.20,
    "AED": 3.6725,
    "SAR": 3.75,
    "SGD": 1.34,
    "HKD": 7.82,
    "NZD": 1.62,
    "ZAR": 18.2,
    "BRL": 5.0,
    "MXN": 17.0,
}


class CurrencyDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_file)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    amount REAL NOT NULL,
                    from_currency TEXT NOT NULL,
                    to_currency TEXT NOT NULL,
                    rate REAL NOT NULL,
                    result REAL NOT NULL
                )
            """)

    def add(self, amount, from_currency, to_currency, rate, result):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO conversions
                (created_at, amount, from_currency, to_currency, rate, result)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    amount,
                    from_currency,
                    to_currency,
                    rate,
                    result,
                ),
            )

    def recent(self, limit=20):
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT created_at, amount, from_currency, to_currency, rate, result
                FROM conversions
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
            return cur.fetchall()

    def clear(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM conversions")


class CurrencyService:
    def __init__(self):
        self.cache = {}

    def get_rates(self, base):
        base = base.upper()

        if base in self.cache:
            cached_time, cached_rates = self.cache[base]
            age = (datetime.now() - cached_time).total_seconds()
            if age < 300:
                return cached_rates, "cache"

        response = requests.get(API_URL.format(base), timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise RuntimeError("Exchange-rate service returned an error.")

        rates = data.get("rates", {})
        if not rates:
            raise RuntimeError("No exchange-rate data received.")

        self.cache[base] = (datetime.now(), rates)
        return rates, "live"

    def offline_convert(self, amount, from_currency, to_currency):
        if (
            from_currency not in OFFLINE_RATES_FROM_USD
            or to_currency not in OFFLINE_RATES_FROM_USD
        ):
            raise RuntimeError("Offline rate is unavailable for this currency pair.")

        usd_amount = amount / OFFLINE_RATES_FROM_USD[from_currency]
        result = usd_amount * OFFLINE_RATES_FROM_USD[to_currency]
        rate = result / amount
        return result, rate


class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry("1050x720")
        self.minsize(920, 650)

        ctk.set_default_color_theme("blue")
        self.settings = self.load_settings()

        theme = self.settings.get("theme", "Dark")
        ctk.set_appearance_mode(theme)

        self.db = CurrencyDatabase(DB_FILE)
        self.service = CurrencyService()

        self.last_result_text = ""
        self.current_status = "Ready"

        self._configure_grid()
        self._build_ui()
        self._load_saved_preferences()
        self.refresh_history()

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def _build_ui(self):
        self._build_header()

        content = ctk.CTkFrame(self, corner_radius=24)
        content.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)
        content.grid_rowconfigure(0, weight=1)

        self.converter_panel = ctk.CTkFrame(content, corner_radius=20)
        self.converter_panel.grid(row=0, column=0, sticky="nsew", padx=(18, 9), pady=18)

        self.history_panel = ctk.CTkFrame(content, corner_radius=20)
        self.history_panel.grid(row=0, column=1, sticky="nsew", padx=(9, 18), pady=18)

        self._build_converter()
        self._build_history()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=20)
        header.grid_columnconfigure(0, weight=1)

        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_box, text="💱 Nova Currency", font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_box,
            text="Fast, modern and practical currency conversion",
            font=ctk.CTkFont(size=13),
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e")

        self.theme_switch = ctk.CTkSwitch(
            right, text="Dark mode", command=self.toggle_theme
        )
        self.theme_switch.pack(side="left", padx=10)

        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def _build_converter(self):
        self.converter_panel.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self.converter_panel,
            text="Currency Converter",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(24, 6))

        ctk.CTkLabel(
            self.converter_panel,
            text="Enter an amount and choose your currency pair.",
            font=ctk.CTkFont(size=13),
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 20))

        self.amount_var = tk.StringVar(value="100")
        self.from_var = tk.StringVar(value="USD")
        self.to_var = tk.StringVar(value="INR")

        ctk.CTkLabel(self.converter_panel, text="Amount").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=24
        )

        self.amount_entry = ctk.CTkEntry(
            self.converter_panel,
            textvariable=self.amount_var,
            height=48,
            font=ctk.CTkFont(size=18),
            placeholder_text="Enter amount",
        )
        self.amount_entry.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=24, pady=(7, 18)
        )
        self.amount_entry.bind("<Return>", lambda event: self.convert())

        ctk.CTkLabel(self.converter_panel, text="From").grid(
            row=4, column=0, sticky="w", padx=(24, 10)
        )
        ctk.CTkLabel(self.converter_panel, text="To").grid(
            row=4, column=1, sticky="w", padx=(10, 24)
        )

        values = sorted(CURRENCIES.keys())

        self.from_combo = ctk.CTkComboBox(
            self.converter_panel,
            values=values,
            variable=self.from_var,
            height=44,
            state="readonly",
        )
        self.from_combo.grid(row=5, column=0, sticky="ew", padx=(24, 10), pady=(7, 12))

        self.to_combo = ctk.CTkComboBox(
            self.converter_panel,
            values=values,
            variable=self.to_var,
            height=44,
            state="readonly",
        )
        self.to_combo.grid(row=5, column=1, sticky="ew", padx=(10, 24), pady=(7, 12))

        tools = ctk.CTkFrame(self.converter_panel, fg_color="transparent")
        tools.grid(row=6, column=0, columnspan=2, sticky="ew", padx=24, pady=(2, 12))
        tools.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(
            tools, text="⇄ Swap", height=38, command=self.swap_currencies
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            tools,
            text="Reset",
            height=38,
            fg_color="transparent",
            border_width=1,
            command=self.reset_form,
        ).grid(row=0, column=1, sticky="ew", padx=6)

        ctk.CTkButton(
            tools,
            text="Copy",
            height=38,
            fg_color="transparent",
            border_width=1,
            command=self.copy_result,
        ).grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self.convert_button = ctk.CTkButton(
            self.converter_panel,
            text="Convert Currency",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.convert,
        )
        self.convert_button.grid(
            row=7, column=0, columnspan=2, sticky="ew", padx=24, pady=(4, 18)
        )

        self.result_card = ctk.CTkFrame(self.converter_panel, corner_radius=18)
        self.result_card.grid(
            row=8, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 12)
        )
        self.result_card.grid_columnconfigure(0, weight=1)

        self.result_label = ctk.CTkLabel(
            self.result_card,
            text="Your converted amount will appear here",
            font=ctk.CTkFont(size=22, weight="bold"),
            wraplength=520,
        )
        self.result_label.grid(row=0, column=0, padx=22, pady=(22, 8))

        self.rate_label = ctk.CTkLabel(
            self.result_card, text="", font=ctk.CTkFont(size=13)
        )
        self.rate_label.grid(row=1, column=0, padx=22, pady=(0, 8))

        self.status_label = ctk.CTkLabel(
            self.result_card, text="Ready", font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=0, padx=22, pady=(0, 20))

        ctk.CTkLabel(
            self.converter_panel,
            text="Tip: Press Enter to convert instantly.",
            font=ctk.CTkFont(size=12),
        ).grid(row=9, column=0, columnspan=2, padx=24, pady=(3, 20))

    def _build_history(self):
        self.history_panel.grid_columnconfigure(0, weight=1)
        self.history_panel.grid_rowconfigure(2, weight=1)

        heading = ctk.CTkFrame(self.history_panel, fg_color="transparent")
        heading.grid(row=0, column=0, sticky="ew", padx=18, pady=(22, 10))
        heading.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            heading, text="Recent History", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            heading,
            text="Clear",
            width=70,
            height=32,
            fg_color="transparent",
            border_width=1,
            command=self.clear_history,
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            self.history_panel,
            text="Your latest conversions are stored locally.",
            font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 10))

        self.history_box = ctk.CTkScrollableFrame(self.history_panel)
        self.history_box.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.history_box.grid_columnconfigure(0, weight=1)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except (json.JSONDecodeError, OSError):
                pass
        return {"theme": "Dark", "from": "USD", "to": "INR"}

    def save_settings(self):
        data = {
            "theme": ctk.get_appearance_mode(),
            "from": self.from_var.get(),
            "to": self.to_var.get(),
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
        except OSError:
            pass

    def _load_saved_preferences(self):
        from_currency = self.settings.get("from", "USD")
        to_currency = self.settings.get("to", "INR")

        if from_currency in CURRENCIES:
            self.from_var.set(from_currency)
        if to_currency in CURRENCIES:
            self.to_var.set(to_currency)

    def toggle_theme(self):
        mode = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(mode)
        self.save_settings()

    def validate_amount(self):
        raw = self.amount_var.get().strip().replace(",", "")
        if not raw:
            raise ValueError("Please enter an amount.")

        amount = float(raw)

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        return amount

    def convert(self):
        try:
            amount = self.validate_amount()
        except ValueError as exc:
            messagebox.showerror("Invalid Amount", str(exc))
            return

        from_currency = self.from_var.get()
        to_currency = self.to_var.get()

        if from_currency == to_currency:
            self.show_result(
                amount, from_currency, to_currency, 1.0, amount, "same currency"
            )
            return

        self.convert_button.configure(state="disabled", text="Converting...")
        self.status_label.configure(text="Fetching latest exchange rate...")

        thread = threading.Thread(
            target=self._convert_worker,
            args=(amount, from_currency, to_currency),
            daemon=True,
        )
        thread.start()

    def _convert_worker(self, amount, from_currency, to_currency):
        try:
            rates, source = self.service.get_rates(from_currency)

            if to_currency not in rates:
                raise RuntimeError("Selected target currency is not available.")

            rate = float(rates[to_currency])
            result = amount * rate

            self.after(
                0,
                lambda: self.show_result(
                    amount, from_currency, to_currency, rate, result, source
                ),
            )

        except (requests.RequestException, ValueError, RuntimeError):
            try:
                result, rate = self.service.offline_convert(
                    amount, from_currency, to_currency
                )

                self.after(
                    0,
                    lambda: self.show_result(
                        amount,
                        from_currency,
                        to_currency,
                        rate,
                        result,
                        "offline fallback",
                    ),
                )
            except (RuntimeError, ValueError):
                self.after(
                    0,
                    lambda: self.handle_conversion_error(
                        "No valid exchange rate is available."
                    ),
                )

    def show_result(self, amount, from_currency, to_currency, rate, result, source):
        symbol = SYMBOLS.get(to_currency, "")
        formatted_result = f"{symbol}{result:,.4f} {to_currency}"

        self.result_label.configure(text=formatted_result)
        self.rate_label.configure(text=f"1 {from_currency} = {rate:,.6f} {to_currency}")

        source_text = {
            "live": "Live exchange rate",
            "cache": "Cached live rate",
            "offline fallback": "Offline fallback rate",
            "same currency": "Same currency",
        }.get(source, source)

        self.status_label.configure(
            text=(f"{source_text} • Updated " f"{datetime.now().strftime('%H:%M:%S')}")
        )

        self.last_result_text = (
            f"{amount:,.4f} {from_currency} = "
            f"{result:,.4f} {to_currency}\n"
            f"Rate: 1 {from_currency} = {rate:,.6f} {to_currency}"
        )

        self.db.add(amount, from_currency, to_currency, rate, result)

        self.save_settings()
        self.refresh_history()
        self.convert_button.configure(state="normal", text="Convert Currency")

    def handle_conversion_error(self, error):
        self.convert_button.configure(state="normal", text="Convert Currency")
        self.status_label.configure(text="Conversion failed")
        messagebox.showerror(
            "Conversion Error",
            "Unable to retrieve a valid exchange rate.\n\n"
            f"Details: {error}\n\n"
            "Check your internet connection or try another currency pair.",
        )

    def swap_currencies(self):
        current_from = self.from_var.get()
        current_to = self.to_var.get()

        self.from_var.set(current_to)
        self.to_var.set(current_from)

        if self.amount_var.get().strip():
            self.convert()

    def reset_form(self):
        self.amount_var.set("100")
        self.from_var.set("USD")
        self.to_var.set("INR")
        self.result_label.configure(text="Your converted amount will appear here")
        self.rate_label.configure(text="")
        self.status_label.configure(text="Ready")
        self.last_result_text = ""

    def copy_result(self):
        if not self.last_result_text:
            messagebox.showinfo("Copy Result", "Convert an amount first.")
            return

        self.clipboard_clear()
        self.clipboard_append(self.last_result_text)
        self.update()
        self.status_label.configure(text="Result copied to clipboard")

    def refresh_history(self):
        for widget in self.history_box.winfo_children():
            widget.destroy()

        rows = self.db.recent(20)

        if not rows:
            ctk.CTkLabel(
                self.history_box,
                text="No conversion history yet.",
                font=ctk.CTkFont(size=13),
            ).grid(row=0, column=0, padx=10, pady=20)
            return

        for index, row in enumerate(rows):
            created_at, amount, from_currency, to_currency, rate, result = row

            card = ctk.CTkFrame(self.history_box, corner_radius=14)
            card.grid(row=index, column=0, sticky="ew", padx=4, pady=6)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=(
                    f"{amount:,.2f} {from_currency}  →  " f"{result:,.2f} {to_currency}"
                ),
                font=ctk.CTkFont(size=14, weight="bold"),
            ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 3))

            ctk.CTkLabel(
                card,
                text=f"Rate: {rate:,.6f}  •  {created_at}",
                font=ctk.CTkFont(size=11),
            ).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

    def clear_history(self):
        if not self.db.recent(1):
            return

        confirmed = messagebox.askyesno(
            "Clear History", "Do you want to delete all conversion history?"
        )

        if confirmed:
            self.db.clear()
            self.refresh_history()

    def on_close(self):
        self.save_settings()
        self.destroy()


if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
