import os
import time
import json
import logging
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class SnapAuthenticator:
    def __init__(self, config=None):
        self.driver = None
        self.wait = None
        self.config = config

    def attach_config(self, config):
        self.config = config

    def attach_driver(self, driver, wait=None):
        self.driver = driver
        self.wait = wait or WebDriverWait(driver, 20)

    def _init_driver_if_needed(self):
        if self.driver:
            return True
        try:
            from selenium.webdriver.chrome.options import Options
            options = Options()
            # Headless only if explicitly requested
            headless = False
            if self.config and self.config.get('browser.headless', False):
                headless = True
            if headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--proxy-server=direct://')
            options.add_argument('--proxy-bypass-list=*')
            self.driver = webdriver.Chrome(options=options)  # Selenium Manager resolves driver
            self.wait = WebDriverWait(self.driver, 20)
            return True
        except Exception as e:
            logger.error(f"❌ Could not start Selenium driver: {e}")
            return False
    
    def manual_login(self):
        """Start or reuse driver, open login page, wait for user login."""
        login_url = (self.config.get('snapp.login_url') if self.config else None) or "https://app.snapp.taxi/login"
        print("🔄 Preparing browser for manual login...")

        driver_ready = self._init_driver_if_needed()
        if not driver_ready:
            print("⚠️ Falling back to system browser open.")
            return self._fallback_manual_login(login_url)

        try:
            print("🌐 Navigating to login page...")
            self.driver.get(login_url)
            print("✅ Login page opened. Complete login in the browser.")
            input("Press Enter AFTER successful login...")
            if self.is_logged_in():
                print("✅ Login verified.")
                return True
            else:
                print("⚠️ Could not verify login; proceeding anyway.")
                return True
        except Exception as e:
            print(f"❌ Error during Selenium login flow: {e}")
            return self._fallback_manual_login(login_url)
    
    def _fallback_manual_login(self, login_url):
        """Fallback using default system browser."""
        print("🔧 Using fallback login method (system browser)...")
        print(f"📋 Opening: {login_url}")
        try:
            webbrowser.open(login_url)
        except Exception as e:
            print(f"⚠️ Could not auto-open browser: {e}. Please open manually: {login_url}")
        print("\nSteps:")
        print("1. Perform login in opened browser window")
        print("2. Navigate to: https://snapppay.ir/timetable/")
        print("3. Return here and press Enter")
        input("Press Enter AFTER completing login and navigation...")
        return True
    
    def is_logged_in(self):
        """Heuristic login verification by checking known elements."""
        try:
            # Try to access a page that requires login
            self.driver.get("https://app.snapp.taxi/")
            time.sleep(3)
            
            # Check for elements that indicate logged-in state
            indicators = [
                "//*[contains(text(), 'پروفایل')]",
                "//*[contains(text(), 'Profile')]",
                "//*[contains(@href, 'profile')]",
                "//*[contains(@class, 'user')]"
            ]
            
            for indicator in indicators:
                try:
                    self.driver.find_element(By.XPATH, indicator)
                    return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"⚠️ Could not verify login: {e}")
            return True  # Assume success to continue
    
    def save_cookies(self):
        """Persist cookies to disk if driver exists."""
        try:
            if self.driver:
                cookies = self.driver.get_cookies()
                os.makedirs('data/cookies', exist_ok=True)
                with open('data/cookies/snapp_cookies.json', 'w', encoding='utf-8') as f:
                    json.dump(cookies, f, ensure_ascii=False)
                print("✅ Cookies saved")
        except Exception as e:
            print(f"⚠️ Could not save cookies: {e}")
    
    def close(self):
        """Close Selenium browser if active."""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")