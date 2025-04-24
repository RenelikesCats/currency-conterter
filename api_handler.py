import requests

BASE_URL_TEMPLATE = "https://api.freecurrencyapi.com/v1/latest?apikey={}"
CURRENCIES = ["EUR", "USD", "GBP", "CAD", "AUD", "CNY", "JPY", "CZK", "CHF", "SEK", "TRY", "PLN", "RUB"]

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

        url = self.base_url_template.format(
            self.api_key) + f"&base_currency={base_currency}&currencies={self.currencies}"

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
