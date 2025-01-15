# ILIAS Course Downloader

This Python script automates the process of logging into ILIAS, downloading course materials, and extracting ZIP files. It leverages the `Selenium` library for browser automation, enabling the bulk download of multiple course materials at once. The script is designed to work with Microsoft Edge and currently supports Windows only.

## Versions Available

1. **all_ILIAS_auto_down**: Downloads all course materials with a single click.
2. **selected_ILIAS_auto_down**: Allows you to choose which courses to download.

## Note

Please note that the script is still under development and may encounter issues with certain tasks, particularly when handling courses with a large amount of data. If you experience any issues, feel free to provide feedback!

## Requirements

- Python 3.x
- Selenium (`pip install selenium`)
- Microsoft Edge WebDriver
- A web portal with downloadable course materials

## Setup Instructions

### 1. Install Dependencies

Ensure that you have Python installed and set up. Then, install the required Python package `Selenium`:

```bash
pip install selenium
```

### 2. Download and Setup Edge WebDriver

Download the appropriate version of Microsoft Edge WebDriver from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

Ensure the `msedgedriver` is on your system's PATH, or specify the path to the `msedgedriver` executable in the script.

### 3. Set Up Credentials and URLs

Update the following placeholders in the script with your actual values:

- `USERNAME`: Your portal username.
- `PASSWORD`: Your portal password.
- `BASE_URL`: The base URL of your portal (e.g., "https://ilias.institution.com").
- `DOWNLOAD_FOLDER`: The folder where the downloaded files will be stored (e.g., "C:\Users\user\Documents\Downloads").

### 4. Run the Script

Execute the script with Python:

```bash
python download_course_materials.py
```

## Script Overview

### `setup_webdriver(download_folder)`
Configures the Edge WebDriver to run in headless mode and sets up the download folder.

### `login_to_portal(driver, url, username, password)`
Logs into the portal using provided credentials.

### `fetch_courses(driver, base_url)`
Retrieves available course links and names from the membership overview page.

### `download_course_material(driver, base_url, course_id)`
Downloads course materials by selecting available checkboxes on the course's download page.

### `wait_for_download_completion(download_folder)`
Waits for all downloads to complete by checking for `.crdownload` files in the specified download folder.

### `extract_zip_files(zip_folder, final_destination_base)`
Extracts any ZIP files in the download folder and moves the extracted contents to the final destination folder.

### `normalize_path(path)`
Normalizes file paths for compatibility across different operating systems.

### `normalize_text(text)`
Normalizes text for file and folder name compatibility by replacing special characters.

### `sanitize_name(path)`
Sanitizes file and folder names to remove any unwanted spaces or special characters.

## Notes

- **Headless Mode**: The script runs the WebDriver in headless mode for efficiency (no browser window will open).
- **Error Handling**: The script includes basic error handling for cases where some files might fail to download or unzip.
- **Course Exclusions**: Specific courses may require additional actions (e.g., unchecking supplementary material), which is handled automatically for courses with certain IDs.
- **File Overwriting**: The script handles existing files by overwriting them during extraction.

## Troubleshooting

- If the download does not complete, ensure the `download_folder` is accessible and has enough space.
- If ZIP extraction fails, check for permission issues with the destination folder.
- Ensure that `msedgedriver` is properly installed and accessible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
