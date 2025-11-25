import json
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.driver = None
        self.current_session_id = None
    
    def create_driver(self, headless=False):
        """Create and configure Chrome driver"""
        try:
            options = Options()
            
            if headless:
                options.add_argument('--headless')
            
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Set user agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
            
            # Try to find ChromeDriver automatically
            try:
                # First try: Use webdriver-manager if available
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except ImportError:
                # Fallback: Use system ChromeDriver
                self.driver = webdriver.Chrome(options=options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ Browser driver created successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"❌ Failed to create browser driver: {e}")
            # Ultimate fallback - try without service
            try:
                self.driver = webdriver.Chrome(options=options)
                return self.driver
            except Exception as e2:
                logger.error(f"❌ Ultimate fallback also failed: {e2}")
                raise
    
    def save_session(self, session_id=None):
        """Save current browser session"""
        if not self.driver:
            logger.error("❌ No active browser session to save")
            return False
        
        try:
            import time
            session_id = session_id or f"session_{int(time.time())}"
            self.current_session_id = session_id
            
            # Create sessions directory if it doesn't exist
            os.makedirs('data/sessions', exist_ok=True)
            
            # Save cookies
            cookies = self.driver.get_cookies()
            with open(f'data/sessions/{session_id}_cookies.json', 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False)
            
            # Save local storage
            try:
                local_storage = self.driver.execute_script("return JSON.stringify(window.localStorage);")
                with open(f'data/sessions/{session_id}_localstorage.json', 'w', encoding='utf-8') as f:
                    f.write(local_storage)
            except Exception as e:
                logger.warning(f"Could not save local storage: {e}")
            
            logger.info(f"✅ Session saved: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")
            return False
    
    def load_session(self, session_id):
        """Load browser session"""
        try:
            if not self.driver:
                self.create_driver()
            
            # Load cookies
            with open(f'data/sessions/{session_id}_cookies.json', 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            self.driver.get("https://app.snapp.taxi")  # Navigate to domain first
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            # Refresh to apply cookies
            self.driver.refresh()
            
            self.current_session_id = session_id
            logger.info(f"✅ Session loaded: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load session: {e}")
            return False
    
    def get_session_state(self):
        """Get current session state for browser transfer"""
        if not self.driver:
            return None
        
        try:
            session_data = {
                'cookies': self.driver.get_cookies(),
                'local_storage': self.driver.execute_script("return JSON.stringify(window.localStorage);"),
                'session_storage': self.driver.execute_script("return JSON.stringify(window.sessionStorage);"),
                'current_url': self.driver.current_url
            }
            
            return session_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get session state: {e}")
            return {}
    
    def close(self):
        """Close browser session"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("✅ Browser session closed")