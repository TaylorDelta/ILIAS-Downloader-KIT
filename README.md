# Web Scraper with Selenium and Tkinter

This project is a Python-based web scraper that utilizes the `selenium` library for web automation, `tkinter` for a simple graphical user interface (GUI), and the Microsoft Edge WebDriver. The script is designed to automate web interactions, such as downloading files or extracting content, based on user input through a Tkinter interface.

## Requirements

Before running the script, ensure that you have the following:

- Python 3.x
- `selenium` library
- `tkinter` library (typically bundled with Python)
- Microsoft Edge WebDriver

You can install the necessary Python libraries using the following pip command:

`pip install selenium`

Ensure that you have the correct version of the Microsoft Edge WebDriver installed, which matches the version of Microsoft Edge on your system. You can download it from the official Microsoft Edge WebDriver site.

## How to Use

1. Clone this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Run the `scraper.py` script. The script will launch a Tkinter window where you can input the necessary data, such as URLs and file paths.

4. The script will use Selenium to interact with the webpage and perform actions like downloading files or scraping data.

5. If the script involves downloading files (e.g., zip files), it will automatically extract the contents for further processing.

## How It Works

- **Selenium WebDriver**: The script uses Selenium to control a web browser (Microsoft Edge). It navigates to specific URLs, interacts with elements (like buttons or input fields), and downloads files as necessary.
  
- **Tkinter GUI**: The Tkinter module provides a simple interface where users can input data required for the scraper to function, such as URLs, search keywords, or file paths.

- **File Handling**: The script supports downloading and extracting files, especially zip files, and can process them for further usage.

- **Automation**: The script waits for web elements to load before interacting with them and can be customized to handle different web pages, form submissions, or file downloads.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
