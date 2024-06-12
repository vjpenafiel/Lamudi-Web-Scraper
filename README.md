# Lamudi Web Scraper 🏠

This Python script is designed to scrape data from property listings on Lamudi. It extracts information such as title, price, location, number of bedrooms, and more, and saves it to a CSV file for further analysis.

## Features

- Scrapes data from Lamudi property listings.
- Extracts various details including title, price, location, number of bedrooms, etc.
- Saves the extracted data to a CSV file for easy access and analysis.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/lamudi-web-scraper.git
    ```

2. **Install the required dependencies:**

    ```bash
    pip install beautifulsoup4 requests regex
    ```

## Usage

1. **Run the `scraper.py` script:**

    ```bash
    python Web_Scraper.py
    ```

2. **The script will start scraping data from Lamudi listings and save it to a CSV file named `properties.csv`.**

## Dependencies

- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/): A Python library for pulling data out of HTML and XML files.
- [Requests](https://pypi.org/project/requests/): A simple HTTP library for making requests in Python.
- [regex](https://pypi.org/project/regex/): A regular expression library that supports various features beyond those provided by the standard Python `re` module.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
