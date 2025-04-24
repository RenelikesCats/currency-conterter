import tkinter as tk
from tkinter import ttk
from api_handler import CurrencyConverterAPI, CURRENCIES
import os
import requests

DEFAULT_API_KEY = os.environ.get("API_KEY_CURRENCIES") # Environment variable

class CurrencyConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")
        master.resizable(height=False, width=False) #Prevent resizing

        self.api_key = tk.StringVar(master, value=DEFAULT_API_KEY if DEFAULT_API_KEY else "")
        self.amount_str = tk.StringVar(master)
        self.base_currency_var = tk.StringVar(master, value=CURRENCIES[0])
        self.result_text = tk.StringVar(master)

        self.api_handler = CurrencyConverterAPI(self.api_key.get())

        self.api_key_frame = ttk.LabelFrame(master, text="API Key")
        self.api_key_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.api_key_label = ttk.Label(self.api_key_frame, text="Enter API Key:")
        self.api_key_entry = ttk.Entry(self.api_key_frame, textvariable=self.api_key, show="*") # Initially hide

        self.amount_label = ttk.Label(master, text="Enter Amount:")
        self.amount_entry = ttk.Entry(master, textvariable=self.amount_str)

        self.base_currency_label = ttk.Label(master, text="Select Base Currency:")
        self.base_currency_dropdown = ttk.Combobox(master, textvariable=self.base_currency_var, values=CURRENCIES)

        self.convert_button = ttk.Button(master, text="Convert", command=self.calculate_and_display)

        self.result_label = ttk.Label(master, text="Converted Amounts:")
        self.result_display = tk.Label(master, textvariable=self.result_text, justify="left", font=("Helvetica", 14))

        self.show_api_key_button = ttk.Button(self.api_key_frame, text="Show", command=self._toggle_api_key_visibility)
        self._layout_widgets()
        self._layout_api_key_widgets()

    def _layout_widgets(self):
        self.amount_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.base_currency_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.base_currency_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.result_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.result_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def _layout_api_key_widgets(self):
        self.api_key_label.grid(row=0, column=0, padx=5, pady=5, sticky="w", in_=self.api_key_frame)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew", in_=self.api_key_frame)
        self.show_api_key_button.grid(row=0, column=2, padx=5, pady=5, sticky="e", in_=self.api_key_frame)

    def _toggle_api_key_visibility(self):
        if self.api_key_entry.cget("show") == "":
            self.api_key_entry.config(show="*")
            self.show_api_key_button.config(text="Show")
        else:
            self.api_key_entry.config(show="")
            self.show_api_key_button.config(text="Hide")

    def calculate_and_display(self):
        api_key = self.api_key.get()
        base_currency = self.base_currency_var.get()
        amount_str = self.amount_str.get()

        if not api_key:
            self.result_text.set("API Key is required.\nPlease enter it.")
            return
        if not base_currency:
            self.result_text.set("Please select a base currency.")
            return
        if not amount_str:
            self.result_text.set("Please enter an amount to convert.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            self.result_text.set("Invalid amount. Please enter a number.")
            return

        self.api_handler.set_api_key(api_key)
        try:
            rates = self.api_handler.get_exchange_rates(base_currency)
            if rates:
                converted_amounts = {currency: amount * rate for currency, rate in rates.items()}
                self.result_text.set("\n".join(f"{key}: {value:.2f}" for key, value in converted_amounts.items()))
            else:
                self.result_text.set("Could not retrieve exchange rates.")
        except ValueError as e:
            self.result_text.set(str(e))
        except requests.exceptions.RequestException as e:
            self.result_text.set(str(e))
        except Exception as e:
            self.result_text.set(f"An unexpected error occurred: {e}")