# Automated ILIAS Downloader

This project is a Python-based web scraper that automates the process of logging into the ILIAS learning platform, selecting courses, and downloading all available course files, data, and PDFs. The script uses Selenium with Edge WebDriver for web automation and Tkinter for a simple graphical user interface (GUI) to select courses. ZIP files are downloaded, extracted, and cleaned up automatically.

## Features

- Logs into the ILIAS learning platform using provided credentials.
- Allows users to select courses to download using a Tkinter-based GUI.
- Downloads all available course files, including PDFs and data.
- Extracts ZIP archives and removes them after extraction.
- Uses Microsoft Edge WebDriver for browser automation.
- Provides a customizable download folder for saving files.

## Requirements

To run this script, you need the following:

- Python 3.x
- Selenium library (install via pip)
- Tkinter library (usually bundled with Python)
- Microsoft Edge WebDriver (ensure the version matches your Edge browser)

You can install Selenium using pip:
pip install selenium

Make sure to download the appropriate version of **Microsoft Edge WebDriver** that matches the version of Microsoft Edge you are using. You can get it from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

## Setup

1. Install Python 3.x if you haven't already.
2. Install Selenium by running `pip install selenium` in your terminal.
3. Download Microsoft Edge WebDriver and ensure the version matches your Edge browser version.
4. Update the script with the following information:
   - `username`: Your ILIAS login username.
   - `password`: Your ILIAS login password.
   - `login_url`: The URL of your institution's ILIAS login page.
   - `download_folder`: The folder path where the files will be saved.

## Usage

1. Update the script with your ILIAS credentials and login URL:
   - Set the `username`, `password`, `login_url`, and `download_folder` variables in the script.
   
2. Run the script:
   - The Tkinter window will appear displaying a list of courses available for download. Each course will be listed with a checkbox.

3. Select the courses you want to download and click the "Done" button to begin the download process.

4. The script will:
   - Log into ILIAS using Selenium and the provided credentials.
   - Fetch the list of available courses and display them in the Tkinter GUI.
   - Download the selected course files, including PDFs, ZIPs, and other data files.
   - Extract ZIP files automatically and delete them after extraction to keep the download folder clean.

## How it Works

- **Login and Course Selection**: 
  - The script uses Selenium to automate the login process to the ILIAS platform. Once logged in, it retrieves the list of courses available to the user.
  - The courses are displayed in a Tkinter-based GUI with checkboxes, allowing the user to select which courses they want to download.

- **File Download and Extraction**:
  - After the user selects the desired courses and clicks "Done," the script initiates the download process. It interacts with the ILIAS platform to trigger the download of course files.
  - If ZIP files are downloaded, they are extracted automatically into the specified folder.
  - The script deletes the original ZIP files after extraction to maintain a clean download directory.

- **Download Completeness**:
  - The script checks periodically for `.crdownload` files (temporary download files) in the download folder to ensure that the download process is complete before proceeding.

- **Browser Automation**:
  - The script uses Microsoft Edge WebDriver to automate browser actions, making it necessary to have Edge installed and the correct version of WebDriver downloaded.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
