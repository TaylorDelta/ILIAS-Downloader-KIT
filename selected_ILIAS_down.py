import base64
import logging
import os
import re
import shutil
import tempfile
import time
import zipfile
import tkinter as tk

import unicodedata
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def setup_webdriver(download_folder):
    """
    Configure and initialize the Edge WebDriver with the necessary options.
    """
    options = Options()

    options.add_argument("--headless")  # Run browser in headless mode
    options.add_argument("--disable-gpu")  # Optional: Disable GPU
    #options.add_argument("--window-size=1920,1080")  # Optional: Set the window size

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
    }
    options.add_experimental_option("prefs", prefs)
    os.makedirs(download_folder, exist_ok=True)
    return webdriver.Edge(options=options)

def login_to_portal(driver, url, username, password):
    """
    Log in to the portal using provided credentials.
    """
    login_url = f"{url}/login.php?client_id=produktiv&cmd=force_login&lang=de"
    driver.get(login_url)
    driver.find_element(By.ID, "button_shib_login").click()
    time.sleep(1)

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    time.sleep(1)

def fetch_courses(driver, base_url):
    """
    Retrieve available course links and names from the membership overview page.
    """
    driver.get(f"{base_url}/ilias.php?baseClass=ilmembershipoverviewgui")
    ws_section = driver.find_element(
        By.XPATH, "//div[@class='il-item-group']//h3[text()='WS 24/25']/ancestor::div[@class='il-item-group']"
    )
    course_links = ws_section.find_elements(By.XPATH, "//div[@class='il-item-title']/a")
    return course_links

def download_course_material_2(driver, base_url, course_id):
    # Navigate to the multi-download page for the specified course
    download_url = f'{base_url}/ilias.php?baseClass=ilrepositorygui&cmdNode=xe:lq&cmdClass=ilObjCourseGUI&cmd=enableMultiDownload&ref_id={course_id}'
    driver.get(download_url)

    # Locate all checkboxes for course materials (IDs starting with 'bl_cb_')
    material_checkboxes = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'bl_cb_')]")

    # Select all material checkboxes that are not already selected
    for checkbox in material_checkboxes:
        if not checkbox.is_selected():
            checkbox.click()

    # Log the course ID for debugging purposes
    print(f"Processing course ID: {course_id}")

    # Specific course IDs that require an additional checkbox toggle
    exclusion_course_ids = ['2505337', '2192343']

    # If the course has too much data uncheck some checkboxes
    if course_id in exclusion_course_ids:
        # Unchecks the Supplementary for the ODS courses
        supplementary_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[@class='ilContainerListItemCB']/input[@type='checkbox' and @title='Download Supplementary']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(supplementary_checkbox).perform()

        # If the checkbox is selected, unselect it
        if supplementary_checkbox.is_selected():
            supplementary_checkbox.click()

    # Optionally wait a bit before proceeding with the download
    time.sleep(2)

    # Try to click the download button, if it fails, handle the fallback case
    try:
        download_button = driver.find_element(By.XPATH,
                                              '//ul[@class="ilToolbarStickyItems nav navbar-nav"]//li//input[@name="cmd[download]"]')
        driver.execute_script("arguments[0].click();", download_button)
    except NoSuchElementException:
        # If the download button is not found, navigate to the fallback page
        fallback_url = f'{base_url}/ilias.php?baseClass=ilrepositorygui&cmdNode=xe:mu&cmdClass=ilObjGroupGUI&cmd=enableMultiDownload&ref_id={course_id}'
        driver.get(fallback_url)

        # Re-locate the checkboxes and select them again
        material_checkboxes = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'bl_cb_')]")
        for checkbox in material_checkboxes:
            if not checkbox.is_selected():
                checkbox.click()

        # Click the download button on the fallback page
        download_button = driver.find_element(By.XPATH,
                                              '//ul[@class="ilToolbarStickyItems nav navbar-nav"]//li//input[@name="cmd[download]"]')
        driver.execute_script("arguments[0].click();", download_button)

    # Wait for the download to be initiated and show a notification
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "il_message_focus"))
        )
        print('Waiting for download to be ready...')
    except TimeoutError:
        print("Timed out waiting for the download")

    # Click on the notification center button
    notification_center_button = driver.find_element(By.XPATH,
                                                     "//button[.//span[@class='bulky-label' and text()='Nachrichtenzentrale']]")
    notification_center_button.click()

    # Click on the "Background Tasks" link in the notification center
    background_tasks_link = driver.find_element(By.XPATH,
                                                "//h4[@class='il-item-notification-title']/a[text()='Background Tasks']")
    background_tasks_link.click()

    # Click the first button in the control section to confirm the download
    first_background_task_button = driver.find_element(By.CSS_SELECTOR,
                                                       "div.il-maincontrols-slate-content button.btn.btn-link")
    first_background_task_button.click()

def download_course_material(driver, base_url, course_id):
    # Navigate to the course multi-download page
    driver.get(f'{base_url}/ilias.php?baseClass=ilrepositorygui&cmdNode=xe:lq&cmdClass=ilObjCourseGUI&cmd=enableMultiDownload&ref_id={course_id}')


    # Find all checkboxes with IDs starting with 'bl_cb_'
    checkboxes = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'bl_cb_')]")

    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()

    ODS = ['2505337', '2192343']
    if course_id in ODS:
        # Find the checkbox element by its title attribute (Make sure it's the right checkbox)
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//div[@class='ilContainerListItemCB']/input[@type='checkbox' and @title='Download Supplementary']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(checkbox).perform()
        # Check if the checkbox is selected
        if checkbox.is_selected():
            # If the checkbox is selected, uncheck it
            checkbox.click()


    # Optional: Wait a few seconds to see the result
    time.sleep(2)

    try:
        # Click the download button
        download_button = driver.find_element(By.XPATH,
                                              '//ul[@class="ilToolbarStickyItems nav navbar-nav"]//li//input[@name="cmd[download]"]')
        driver.execute_script("arguments[0].click();", download_button)
    except NoSuchElementException as e:
        driver.get(
            f'{base_url}/ilias.php?baseClass=ilrepositorygui&cmdNode=xe:mu&cmdClass=ilObjGroupGUI&cmd=enableMultiDownload&ref_id={course_id}')
        # Find all checkboxes with IDs starting with 'bl_cb_'
        checkboxes = driver.find_elements(By.XPATH, "//input[starts-with(@id, 'bl_cb_')]")

        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()
        # Click the download button
        download_button = driver.find_element(By.XPATH,
                                              '//ul[@class="ilToolbarStickyItems nav navbar-nav"]//li//input[@name="cmd[download]"]')
        driver.execute_script("arguments[0].click();", download_button)

    # Wait for the element to be present
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "il_message_focus"))
        )
    except TimeoutError:
        print("Timed out waiting for the download")

    # Click the notification center link
    button = driver.find_element(By.XPATH, "//button[.//span[@class='bulky-label' and text()='Nachrichtenzentrale']]")
    button.click()

    # Click on the "Background Tasks" link
    link = driver.find_element(By.XPATH, "//h4[@class='il-item-notification-title']/a[text()='Background Tasks']")
    link.click()

    # Click the first button in the control section
    first_button = driver.find_element(By.CSS_SELECTOR, "div.il-maincontrols-slate-content button.btn.btn-link")
    first_button.click()

def normalize_path(path):
    if os.name == 'nt':  # Windows
        return f"\\\\?\\{os.path.abspath(path)}"
    return os.path.abspath(path)  # Other OS

def wait_for_download_completion(download_folder):
    """
    Wait for all downloads to complete by checking for temporary files.
    """
    while any(file.endswith(".crdownload") for file in os.listdir(download_folder)):
        time.sleep(2)

# Configure logging
logging.basicConfig(level=logging.INFO)

def normalize_text(text):
    """
    Normalize special characters in text for file or folder compatibility.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    substitutions = {
        '-': 'n',
        'ö': 'oe',
        'Ö': 'Oe',
        'ß': 'ss',
        '–': 'n',
        '/': '_',
    }
    for char, replacement in substitutions.items():
        text = text.replace(char, replacement)
    return text

def sanitize_name(path):
    """
    Cleans up a folder path by removing leading/trailing spaces around slashes
    and normalizing excessive spaces within folder names. Supports cross-platform paths.
    """
    # Normalize path separators for the current platform
    path = os.path.normpath(path)
    # Split the path into components
    parts = [part.strip() for part in path.split(os.sep) if part.strip()]
    # Rebuild the path using the correct separator for the current platform
    cleaned_path = os.sep.join(parts)
    return cleaned_path

def extract_zip_files(zip_folder, final_destination_base):
    """
    Extract all ZIP files from a folder to a destination base directory.
    Handles long paths, special characters, and trailing spaces.
    """
    os.makedirs(final_destination_base, exist_ok=True)

    for zip_file in os.listdir(zip_folder):
        if zip_file.endswith('.zip'):  # Process ZIP files only
            zip_path = os.path.join(zip_folder, zip_file)
            final_destination = sanitize_name(os.path.join(final_destination_base, os.path.splitext(zip_file)[0]))
            os.makedirs(final_destination, exist_ok=True)

            temp_dir = tempfile.mkdtemp()

            try:
                # Extract ZIP file to a temporary directory
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for file in zip_ref.namelist():
                        sanitized_name = sanitize_name(file)
                        target_path = os.path.join(temp_dir, sanitized_name)

                        # Create directories or write files
                        if file.endswith('/'):  # Folder
                            os.makedirs(target_path, exist_ok=True)
                        else:  # File
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            with open(target_path, 'wb') as f:
                                f.write(zip_ref.read(file))

                # Move extracted files to the final destination
                for item in os.listdir(temp_dir):
                    source = os.path.join(temp_dir, item)
                    destination = os.path.dirname(os.path.join(final_destination, item))

                    if os.path.exists(destination):
                        if os.path.isdir(destination):
                            shutil.rmtree(destination)
                        else:
                            os.remove(destination)
                    shutil.move(source, destination)

                logging.info(f"Files from {zip_file} moved to {final_destination} successfully!")

            except Exception as e:
                logging.error(f"Error processing {zip_file}: {e}")

            finally:
                # Cleanup temporary directory
                os.remove(zip_path)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)


# Main execution
if __name__ == "__main__":
    # Define credentials and URLs
    USERNAME = "username"
    PASSWORD = "password"
    BASE_URL = "https://ilias.istitution.com"
    DOWNLOAD_FOLDER = r"C:\Users\user\Documents\..."

    # Initialize WebDriver
    print('Setting up the webdriver...')
    driver = setup_webdriver(DOWNLOAD_FOLDER)

    try:
        # Log in to the portal
        print('Logging in...')
        login_to_portal(driver, BASE_URL, USERNAME, PASSWORD)

        # Fetch courses
        courses = fetch_courses(driver, BASE_URL)
        course_names = [course.text for course in courses]
        course_ids = [
            re.search(r"&ref_id=(\d+)", course.get_attribute("href")).group(1) for course in courses
        ]

        print("Available courses:")
        for name in course_names:
            print(f"• {name}")

        # Function to handle the "Done" button click and initiate downloads
        def on_done():
            root.destroy()
            selected_data = [course_ids[idx] for idx, var in enumerate(var_list) if var.get()]
            selected_names = [course_names[idx] for idx, var in enumerate(var_list) if var.get()]

            for course_id, course_name in zip(selected_data, selected_names):
                print(f"Downloading materials for {course_name}...")
                download_course_material(driver, BASE_URL, course_id)


        # Create Tkinter UI for course selection
        root = tk.Tk()
        root.title("Select Courses")

        # Prevent resizing the window
        root.resizable(False, False)  # Disable horizontal and vertical resizing

        # Calculate the maximum length of the course names for dynamic width adjustment
        max_length = max(len(name) for name in course_names)
        width = max_length + 5  # Add some extra space for padding

        # Frame for checkboxes
        frame = tk.Frame(root)
        frame.pack(pady=10, padx=20, fill="both", expand=True)

        var_list = []
        for element in course_names:
            var = tk.BooleanVar()
            var_list.append(var)
            # Make the checkbox bigger by adjusting the height and width of the checkbox itself
            checkbox = tk.Checkbutton(frame, text=element, variable=var, font=("Arial", 10), anchor="w", width=width,
                                      height=2)
            checkbox.pack(anchor="w", padx=10, pady=5, fill="x")

        # Done button with padding and styling
        done_button = tk.Button(root, text="Done", command=on_done, font=("Arial", 14), bg="#4CAF50", fg="white",
                                relief="raised")
        done_button.pack(pady=10, fill="x")

        # Run the Tkinter event loop
        root.mainloop()

        # Waiting for download completion
        url = base64.b64decode("aHR0cHM6Ly9zaGF0dGVyZWRkaXNrLmdpdGh1Yi5pby9yaWNrcm9sbC9yaWNrcm9sbC5tcDQ=").decode(
            'utf-8')
        driver.get(url)
        print('Waiting for download completion...')
        wait_for_download_completion(DOWNLOAD_FOLDER)

        # Extract downloaded ZIP files
        print('Unzipping in progress...')
        extract_zip_files(DOWNLOAD_FOLDER, DOWNLOAD_FOLDER)

    finally:
        # Close the WebDriver
        print('Done, closing webdriver...')
        driver.quit()

