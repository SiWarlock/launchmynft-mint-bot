import requests
import base64
import time
import os
import pathlib
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


def mint(values, isWindows, wallet):
    try:
        # Initialize Chrome driver first
        options = Options()
        options.add_extension("Phantom.crx")
        options.add_argument("--disable-gpu")
        
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        os.environ['WDM8LOCAL'] = '1'
        
        driver = webdriver.Chrome(options=options)
        print("Assertion - successfully found chrome driver")
        
        # Now we can get the main window handle
        main_window = driver.current_window_handle
        
        def selectWallet():
            print("Status - Selecting wallet on ME")

            # Click Connect Wallet button
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Connect Wallet')]")))
            connect_wallet = driver.find_element(
                By.XPATH, "//button[contains(text(), 'Connect Wallet')]")
            driver.execute_script("arguments[0].click();", connect_wallet)

            # Click Solana option
            solana_selector = "div.SignInButton_walletRow__wT2qe:first-of-type"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, solana_selector)))
            solana = driver.find_element(By.CSS_SELECTOR, solana_selector)
            driver.execute_script("arguments[0].click();", solana)

            # Click Phantom option directly (since it's now in the first row)
            try:
                phantom = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Phantom')]")))
                driver.execute_script("arguments[0].click();", phantom)
                print("Clicked Phantom")
            except Exception as e:
                print(f"Failed to click Phantom: {e}")

            # Switch to Phantom popup window
            original_window = driver.current_window_handle
            WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            # Click Connect in Phantom popup
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Connect')]")))
            connect = driver.find_element(
                By.XPATH, "//button[contains(text(),'Connect')]")
            driver.execute_script("arguments[0].click();", connect)
            
            # Switch back to main window
            driver.switch_to.window(main_window)

        def initWallet():
            print("Status - Initializing wallet")
            # add wallet to chrome
            original_window = driver.current_window_handle
            WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            print("Event - Switch window")
            
            # Click "I already have a wallet"
            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'I already have a wallet')]")))
            recovery_btn = driver.find_element(
                By.XPATH, "//button[contains(text(),'I already have a wallet')]").click()
            
            # After clicking "I already have a wallet"
            # time.sleep(2)  # Give UI time to transition
            
            # Click Import Private Key option
            private_key_option = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(),'Import Private Key')]")))
            driver.execute_script("arguments[0].click();", private_key_option)
            
            # time.sleep(2)  # Give time for the form to appear
            
            # Fill in name field
            name_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Name']")))
            name_field.clear()  # Clear any existing text
            name_field.send_keys(wallet['name'])
            
            # Fill in private key field
            private_key_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea[placeholder='Private key'], input[placeholder='Private key']")))
            private_key_field.clear()  # Clear any existing text
            private_key_field.send_keys(wallet['privateKey'])
            
            # Click Import button
            import_btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Import']")))
            driver.execute_script("arguments[0].click();", import_btn)
            
            # Wait for password fields and fill them
            password = "Password123!"
            
            # Fill first password field
            password_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")))
            password_field.send_keys(password)
            
            # Fill confirm password field
            confirm_password_field = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")[1]
            confirm_password_field.send_keys(password)
            
            # Click Terms of Service checkbox
            tos_checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            driver.execute_script("arguments[0].click();", tos_checkbox)
            
            # Click Continue button
            continue_btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Continue']")))
            driver.execute_script("arguments[0].click();", continue_btn)
               # Wait 3 seconds
            time.sleep(2)
            
            # Close current window/tab
            driver.close()
            # Switch back to original window
            driver.switch_to.window(original_window)

        print("Bot started") 
        if isWindows:
            print("OS : Windows")
        else:
            print("OS : Mac")
        

        # opens the launchpad page
        driver.get(values[0])

        # Actions - Initialize wallet
        initWallet()

        print("Reloading page to detect Phantom...")
        driver.get(values[0])  # Reload the launchpad page
        time.sleep(2) 

        # Actions - select wallet on magic eden
        selectWallet()

        # After wallet connection, handle the slider
        print("Moving slider to max position...")
        try:
            # Wait for slider
            slider = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='range']")))
            
            # Method 1: JavaScript + ActionChains combination
            max_value = driver.execute_script("return arguments[0].max", slider)
            driver.execute_script(f"arguments[0].value = {max_value}", slider)
            
            # Force update using multiple methods
            actions = ActionChains(driver)
            actions.click(slider).perform()
            actions.send_keys(Keys.END).perform()
            
            # Trigger multiple events to ensure update
            driver.execute_script("""
                var slider = arguments[0];
                slider.value = arguments[1];
                slider.dispatchEvent(new Event('input', { bubbles: true }));
                slider.dispatchEvent(new Event('change', { bubbles: true }));
                slider.dispatchEvent(new MouseEvent('mouseup'));
            """, slider, max_value)
            
            print(f"Moved slider to maximum value: {max_value}")
            
            # Verify the value was set
            current_value = driver.execute_script("return arguments[0].value", slider)
            print(f"Current slider value: {current_value}")
            
        except Exception as e:
            print(f"Error moving slider: {e}")
            # Fallback method: Try to tab to slider and use keyboard
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.TAB).perform()  # Tab to slider
                actions.send_keys(Keys.END).perform()  # Move to end
                print("Used keyboard navigation fallback")
            except Exception as e:
                print(f"Fallback method also failed: {e}")
        
        print("Clicking mint button...")
        try:
            # Wait for and click mint button
            mint_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mint')]")))
            driver.execute_script("arguments[0].click();", mint_button)
            print("Clicked mint button")
            
            # Switch to Phantom popup window
            original_window = driver.current_window_handle
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            
            # Wait for and click confirm button in Phantom
            confirm_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]")))
            driver.execute_script("arguments[0].click();", confirm_button)
            print("Confirmed transaction in Phantom")
            
            # Switch back to main window
            driver.switch_to.window(original_window)
            
            # Wait for transaction completion (look for success message or status change)
            try:
                # Wait for success message or transaction completion indicator
                success_element = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Success') or contains(text(), 'Minted')]")))
                print("Transaction completed successfully")
            except Exception as e:
                print("Waiting for transaction completion timed out")
                
        except Exception as e:
            print(f"Error during minting process: {e}")
            
        print("Mint process completed")
        
        # time.sleep(2)

        print("Minting Finished")
    
    
    finally:
        # Clean up after each wallet
        try:
            driver.quit()
        except:
            pass
