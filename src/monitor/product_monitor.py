import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class ProductMonitor:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.config = None
        self.active_products = []
    
    def set_driver(self, driver, wait):
        """Set browser driver"""
        self.driver = driver
        self.wait = wait
    
    def navigate_to_deals_page(self):
        """Navigate to deals page"""
        try:
            self.driver.get(self.config.get('snapp.snapp_pay_url'))
            logger.info("📄 Deals page loaded")
            
            # Wait for page load
            time.sleep(5)
            return True
            
        except Exception as e:
            logger.error(f"Error loading deals page: {e}")
            return False
    
    def load_all_products(self):
        """Click 'More products' to load all products"""
        try:
            max_clicks = 5
            clicks_done = 0
            
            while clicks_done < max_clicks:
                try:
                    # Locate 'More products' button
                    more_products_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'محصولات بیشتر')]"))
                    )
                    
                    more_products_btn.click()
                    clicks_done += 1
                    logger.info(f"🔄 Clicked More products ({clicks_done}/{max_clicks})")
                    time.sleep(2)
                    
                except Exception as e:
                    logger.info("❌ 'More products' button not found or not clickable")
                    break
            
            logger.info(f"✅ Products load completed ({clicks_done} clicks)")
            return True
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            return False
    
    def check_active_products(self):
        """Check active products"""
        try:
            # Find all products
            products = self.driver.find_elements(By.CSS_SELECTOR, "[class*='product'], [class*='item']")
            
            active_products = []
            
            for product in products:
                product_info = self._extract_product_info(product)
                if product_info and self._is_target_product(product_info):
                    active_products.append(product_info)
            
            return active_products
            
        except Exception as e:
            logger.error(f"خطا در بررسی محصولات: {e}")
            return []
    
    def _extract_product_info(self, product_element):
        """Extract product info from element"""
        try:
            # This requires tuning based on real page structure
            name = product_element.find_element(By.CSS_SELECTOR, "[class*='name'], [class*='title']").text
            price = product_element.find_element(By.CSS_SELECTOR, "[class*='price']").text
            link = product_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            return {
                'name': name,
                'price': price,
                'link': link,
                'element': product_element
            }
        except:
            return None
    
    def _is_target_product(self, product_info):
        """Check if product is target"""
        target_products = self.config.get('products.priority_list', [])
        
        for target in target_products:
            if target.lower() in product_info['name'].lower():
                return True
        return False
    
    def refresh_page(self):
        """Refresh page"""
        try:
            self.driver.refresh()
            time.sleep(3)
            logger.info("🔄 Page refreshed")
            return True
        except Exception as e:
            logger.error(f"Error refreshing page: {e}")
            return False