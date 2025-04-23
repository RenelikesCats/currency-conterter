import requests
import os
import tkinter as tk
from tkinter import ttk

DEFAULT_API_KEY = os.environ.get("API_KEY_CURRENCIES") # Environment variable
BASE_URL_TEMPLATE = "https://api.freecurrencyapi.com/v1/latest?apikey={}"
CURRENCIES = ["EUR", "USD", "CAD", "AUD", "CNY", "JPY", "CZK", "CHF", "SEK", "TRY"]

class CurrencyConverterAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url_template = BASE_URL_TEMPLATE
        self.currencies = ",".join(CURRENCIES)

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_exchange_rates(self, base_currency):
        if not self.api_key:
            raise ValueError("API Key is required.")

        url = self.base_url_template.format(self.api_key) + f"&base_currency={base_currency}&currencies={self.currencies}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            rates = data.get("data")
            if rates:
                return rates
            else:
                return None

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"API Request Error: {e}")
        except ValueError as e:
            raise ValueError(f"JSON Decoding Error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}")

class CurrencyConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")

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
        self.result_display = tk.Label(master, textvariable=self.result_text, justify="left")

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

if __name__ == "__main__":
    root = tk.Tk()
    gui = CurrencyConverterGUI(root)
    root.mainloop()