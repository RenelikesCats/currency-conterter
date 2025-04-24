 ## Currency Converter Desktop App

A simple desktop application to convert currencies in real-time.

## Technologies Used

* Python
* Tkinter (for the graphical user interface)
* [Freecurrencyapi.com](https://freecurrencyapi.com/)  (api for realtime currency conversion)

## How to use?

1.  **Obtain an API Key:** To use this application, you'll need a free API key from [Freecurrencyapi.com](https://freecurrencyapi.com/).

2.  **Running the Application:** Execute the main Python script of the application.

3.  **Entering Your API Key:** You have two options for providing your API key:

    * **Option 1: On-Screen Input (Temporary):**
        * When the application starts, you will see a prompt to "Enter Api Key".
        * Paste your API key into the provided field and click "Submit" or a similar button.
        * ![On-screen API Key Input](https://github.com/user-attachments/assets/429f1d15-2b40-4f3f-bee7-30f412915e81)

    * **Option 2: Environment Variable (Persistent):**
        * For a more permanent solution, you can save your API key as an environment variable on your system.
        * Ensure the environment variable is named **exactly** as `FREE_CURRENCY_API_KEY`.
        * ![Environment Variable Setup](https://github.com/user-attachments/assets/929b47a7-f1ed-4ef7-b3d3-0dc8661ba918)
        * If the application detects this environment variable, you won't be prompted to enter the API key each time.


## Acknowledgements

* Special thanks to the book "Python GUI Programming with Tkinter, 2nd edition" for its valuable guidance in developing the GUI.
* Thanks to [Freecurrencyapi.com](https://freecurrencyapi.com/) for the real-time currency exchange rate API.







