import os
import re
import time
import tkinter as tk
import zipfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options


def normalize_text(text):
    text = text.replace('-', 'n')  # Change "-" to "n"
    text = text.replace('ö', 'oe')  # Change "ö" to "oe"
    text = text.replace('Ö', 'Oe')  # Change "Ö" to "Oe"
    text = text.replace('ß', 'ss')  # Change "Ö" to "Oe"
    text = text.replace('–', 'n')  # Change "–" to "n" (En Dash, longer hyphen)
    text = text.replace('/', '_')  # Change "–" to "n"

    # Add other replacements as needed (like ä->ae, ü->ue, etc.)
    # text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove any remaining non-alphanumeric characters if needed
    return text


def download(url, driver, id):
    driver.get(
        f'{url}/ilias.php?baseClass=ilrepositorygui&cmdNode=xe:lq&cmdClass=ilObjCourseGUI&cmd=enableMultiDownload&ref_id={id}')
    # List of checkbox IDs to be clicked
    checkbox_ids = ["bl_cb_1", "bl_cb_2", "bl_cb_3", "bl_cb_4"]
    # Click all checkboxes for all data
    for checkbox_id in checkbox_ids:
        try:
            # Locate the checkbox by its ID
            checkbox = driver.find_element(By.ID, checkbox_id)
            # Check if the checkbox is unchecked
            if not checkbox.is_selected():
                checkbox.click()  # Click the checkbox to check it
        except Exception as e:
            pass

    # Initiate download
    download_button = driver.find_element(By.XPATH,
                                          '//ul[@class="ilToolbarStickyItems nav navbar-nav"]//li//input[@name="cmd[download]"]')
    driver.execute_script("arguments[0].click();", download_button)

    driver.implicitly_wait(10)

    button = driver.find_element(By.XPATH, "//button[.//span[@class='bulky-label' and text()='Nachrichtenzentrale']]")
    button.click()

    # Locate the link using XPath and click it
    link = driver.find_element(By.XPATH, "//h4[@class='il-item-notification-title']/a[text()='Background Tasks']")
    link.click()

    # Extract the name from the <h1> tag
    header = driver.find_element(By.XPATH, '//h1[@class="il-page-content-header media-heading ilHeader "]')
    header_name = header.text.strip()

    # Normalize the header text (apply character replacements)
    normalized_header_name = normalize_text(header_name)
    driver.implicitly_wait(20)

    # Locate the first button inside the div with the class 'il-maincontrols-slate-content'
    first_button = driver.find_element(By.CSS_SELECTOR, "div.il-maincontrols-slate-content button.btn.btn-link")

    # Click the button
    first_button.click()
    #
    buttons = driver.find_elements(By.XPATH, '//button[@class="close" and @aria-label="Schließen"]')

    #Click each button
    for button in buttons:
        button.click()

    driver.implicitly_wait(1)


def get_courses(url, username, password, download_folder):
    # Set up the EdgeOptions object
    options = Options()

    # Set preferences for the download folder
    prefs = {
        "download.default_directory": download_folder,  # Set download folder path
        "download.prompt_for_download": False,  # Disable prompt for downloading
        "download.directory_upgrade": True,  # Allow folder path change during runtime
        "safebrowsing.enabled": False  # Disable safebrowsing warning for downloaded files
    }

    # Apply preferences to the EdgeOptions
    options.add_experimental_option("prefs", prefs)

    # Create WebDriver instance with the EdgeOptions
    driver = webdriver.Edge(options=options)

    login_url = f'{url}/login.php?client_id=produktiv&cmd=force_login&lang=de'

    driver.get(login_url)

    # Step 2: Click the login button (button_shib_login)
    login_button = driver.find_element(By.ID, "button_shib_login")  # Locate by ID
    login_button.click()

    time.sleep(1)

    # Locate the username and password input fields
    username_field = driver.find_element(By.ID, "username")  # Replace with actual element ID or XPath
    password_field = driver.find_element(By.ID, "password")  # Replace with actual element ID or XPath

    # Fill in the login credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the form (adjust if needed based on the form)
    password_field.send_keys(Keys.RETURN)  # or use driver.find_element(By.ID, "login_button").click() if it's a button

    # Step 3: Wait for the login to complete
    time.sleep(1)  # Adjust the sleep time based on the website's response time

    driver.get(f'{url}/ilias.php?baseClass=ilmembershipoverviewgui')

    # Locate the div with the class 'il-item-group' containing the h3 with text 'WS 24/25'
    parent_div = driver.find_element(By.XPATH,
                                     "//div[@class='il-item-group']//h3[text()='WS 24/25']/ancestor::div[@class='il-item-group']")

    # Find all the 'a' tags inside div with class 'il-item-title' within that parent div
    links = parent_div.find_elements(By.XPATH, ".//div[@class='il-item-title']//a")
    names = driver.find_elements(By.XPATH, "//div[@class='il-item-title']/a")

    # Extract and print the text (name) for each element

    return driver, links, names




def close_driver(driver):
    driver.quit()  # Close the browser when done


def extract_all_zips_in_folder(folder_path):
    # Loop through each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.zip'):  # Check if the file is a zip file
            zip_path = os.path.join(folder_path, file_name)

            try:
                # Create a directory to extract to (same name as zip file)
                extract_dir = os.path.join(folder_path, file_name[:-4])
                os.makedirs(extract_dir, exist_ok=True)

                # Extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                    print(f"Extracted {file_name} to {extract_dir}")

                # Delete the zip file after extraction
                os.remove(zip_path)
                print(f"Deleted {file_name} after extraction.")

            except FileNotFoundError:
                print(f"File not found: {zip_path}. Skipping...")
            except Exception as e:
                print(f"Error processing {zip_path}: {e}")


if __name__ == "__main__":
    # Input
    username = "username"
    password = "password"
    download_folder = "download_folder"
    login_url = 'loginurl'

    # Login and get all available courses
    driver, links, names = get_courses(login_url, username, password, download_folder)

    files = []
    for element in names:
        files.append(element.text)

    # Extract and print the href attribute (the URL) of each link
    ref_id_pattern = re.compile(r"&ref_id=(\d+)")
    # Extract and print the number from each link
    ref_ids = []
    # Extract and store the ref_id numbers in the list
    for link in links:
        href = link.get_attribute('href')
        # Search for the ref_id number in the href attribute
        match = ref_id_pattern.search(href)
        if match:
            # Append the matched ref_id number to the list
            ref_ids.append(match.group(1))


    # Function to handle the Done button click
    def on_done():
        root.destroy()
        selected_data = [ref_ids[idx] for idx, var in enumerate(var_list) if var.get()]
        for x in selected_data:
            download(login_url, driver, x)


    # Create the main window
    root = tk.Tk()
    root.title("Select Elements")
    root.geometry("500x500")

    # Create a list to store the variable for each checkbox
    var_list = []

    # Create checkboxes for each element
    for element in files:
        var = tk.BooleanVar()
        var_list.append(var)
        checkbox = tk.Checkbutton(root, text=element, variable=var)
        checkbox.pack(anchor="w")

    # Add Done button
    done_button = tk.Button(root, text="Done", command=on_done)
    done_button.pack(pady=10)

    # Run the application
    root.mainloop()


    def is_download_complete(download_folder):
        # List files in the download folder
        files_in_directory = os.listdir(download_folder)
        # Check if there are any temporary files (e.g., .crdownload for Chrome)
        for file in files_in_directory:
            if file.endswith(".crdownload"):
                return False  # A download is still in progress
        return True  # No .crdownload files, download is complete


    # Trigger your download action (for example, clicking a download link)
    driver.get("http://example.com/file-to-download")

    # Check periodically for download completion
    while not is_download_complete(download_folder):
        time.sleep(1)  # Check every second

    close_driver(driver)
