# Web Scraper with Selenium and Tkinter

This project is a Python-based web scraper that automates the process of logging into a website, selecting courses, and downloading related files. The script uses Selenium for web automation, Tkinter for a graphical user interface (GUI) to select files, and processes ZIP files by extracting them after downloading.

## Features

- Logs into a website using provided credentials.
- Navigates through the available courses and displays them in a Tkinter-based GUI.
- Allows the user to select which courses to download.
- Downloads files and extracts any ZIP archives.
- Automatically deletes ZIP files after extraction to keep the download folder clean.
- Supports Microsoft Edge WebDriver for browser automation.

## Requirements

To run this script, you need the following:

- Python 3.x
- Selenium (install via pip)
- Tkinter (usually comes with Python)
- Microsoft Edge WebDriver (Ensure the version matches your Edge browser)

## Setup

1. Install Python 3.x if you haven’t already.
2. Install Selenium via pip: `pip install selenium`
3. Download Microsoft Edge WebDriver and make sure the version matches your Microsoft Edge browser version.

## Usage

1. Update the script with your details:
   - `username`: Your login username.
   - `password`: Your login password.
   - `download_folder`: The folder where you want the files to be downloaded.
   - `login_url`: The URL for the login page of your website.
   
2. Run the script. The Tkinter window will appear with checkboxes for each course available.

3. Select the courses you want to download and click "Done" to initiate the download process.

4. The script will automatically:
   - Log into the website using Selenium.
   - Navigate through the course list.
   - Download the selected course files.
   - Extract ZIP files and delete them after extraction.

## How it Works

- **Login and Course Selection**: The script uses Selenium to open the login page, fills in the credentials, and logs in. Once logged in, it fetches the list of courses and displays them in a Tkinter window with checkboxes.
  
- **File Download and Extraction**: After the user selects the courses to download and clicks "Done", the script downloads the files and checks if any ZIP files need to be extracted. It extracts them and deletes the ZIP file after extraction.

- **Download Completeness**: The script periodically checks for `.crdownload` files in the download folder to ensure the download has finished before moving to the next action.

- **Clean-up**: The script automatically closes the browser when the download and extraction process is completed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
