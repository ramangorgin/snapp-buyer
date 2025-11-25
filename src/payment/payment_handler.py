import time
import webbrowser
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.helpers import retry_on_failure, human_delay

logger = logging.getLogger(__name__)

class PaymentHandler:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.purchased_products = set()
        self.processing_products = set()
    
    def set_driver(self, driver, wait):
        """Set browser driver"""
        self.driver = driver
        self.wait = wait
    
    def should_purchase(self, product):
        """Check if product should be purchased"""
        product_id = product.get('name', 'unknown')
        
        if product_id in self.purchased_products:
            return False
        if product_id in self.processing_products:
            return False
        
        return True
    
    @retry_on_failure(max_retries=3, delay=2)
    def navigate_to_product(self, product):
        """Navigate to product page"""
        try:
            product_url = product.get('link')
            if not product_url:
                logger.error("❌ No product URL provided")
                return False
            
            self.driver.get(product_url)
            logger.info(f"🌐 Navigated to product page: {product['name']}")
            
            # Wait for page load
            time.sleep(3)
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to navigate to product: {e}")
            return False
    
    @retry_on_failure(max_retries=3, delay=1)
    def add_to_cart(self):
        """Add product to cart"""
        try:
            # Try different selectors for add to cart button
            add_to_cart_selectors = [
                "//button[contains(text(), 'Add to Cart')]",
                "//button[contains(text(), 'Add to Basket')]",
                "//button[contains(@class, 'add-to-cart')]",
                "//button[contains(@id, 'add-to-cart')]",
                "//a[contains(text(), 'Add to Cart')]"
            ]
            
            for selector in add_to_cart_selectors:
                try:
                    add_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    add_button.click()
                    logger.info("✅ Product added to cart")
                    human_delay(1, 2)
                    return True
                except:
                    continue
            
            logger.error("❌ Add to cart button not found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to add product to cart: {e}")
            return False
    
    @retry_on_failure(max_retries=2, delay=1)
    def select_snapp_pay(self):
        """Select Snapp Pay payment method"""
        try:
            # Look for Snapp Pay payment option
            snapp_pay_selectors = [
                "//div[contains(text(), 'Snapp Pay')]",
                "//label[contains(text(), 'Snapp Pay')]",
                "//input[@value='snapp-pay']",
                "//button[contains(text(), 'Snapp Pay')]"
            ]
            
            for selector in snapp_pay_selectors:
                try:
                    snapp_pay_option = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    snapp_pay_option.click()
                    logger.info("✅ Snapp Pay payment selected")
                    human_delay(1, 2)
                    return True
                except:
                    continue
            
            logger.warning("⚠️ Snapp Pay option not found, trying to proceed")
            return True  # Continue even if not found
            
        except Exception as e:
            logger.error(f"❌ Failed to select Snapp Pay: {e}")
            return False
    
    def get_payment_url(self):
        """Get payment gateway URL"""
        try:
            # Wait for redirect to payment gateway
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # Check if we're on a payment gateway page
            payment_indicators = ['bank', 'payment', 'gateway', 'shaparak']
            if any(indicator in current_url.lower() for indicator in payment_indicators):
                logger.info(f"💰 Payment gateway URL: {current_url}")
                return current_url
            else:
                # Try to find payment button/link
                payment_buttons = [
                    "//button[contains(text(), 'Pay')]",
                    "//a[contains(text(), 'Pay')]",
                    "//button[contains(text(), 'Payment')]",
                    "//a[contains(@href, 'payment')]"
                ]
                
                for selector in payment_buttons:
                    try:
                        payment_btn = self.driver.find_element(By.XPATH, selector)
                        payment_url = payment_btn.get_attribute('href') or self.driver.current_url
                        logger.info(f"💰 Payment URL found: {payment_url}")
                        return payment_url
                    except:
                        continue
                
                logger.warning("⚠️ No specific payment URL found, using current page")
                return current_url
                
        except Exception as e:
            logger.error(f"❌ Failed to get payment URL: {e}")
            return None
    
    def open_payment_in_browser(self, payment_url):
        """Open payment gateway in user's browser"""
        try:
            # Get session state for transfer
            session_state = self._get_session_state_for_transfer()
            
            # Create HTML page with session data
            self._create_payment_redirect_page(payment_url, session_state)
            
            # Open in default browser
            webbrowser.open('payment_portal.html')
            logger.info("🌐 Payment gateway opened in user's browser")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to open payment in browser: {e}")
            return False
    
    def _get_session_state_for_transfer(self):
        """Get session state for browser transfer"""
        try:
            session_data = {
                'cookies': self.driver.get_cookies(),
                'current_url': self.driver.current_url
            }
            return session_data
        except Exception as e:
            logger.error(f"❌ Failed to get session state: {e}")
            return {}
    
    def _create_payment_redirect_page(self, payment_url, session_data):
        """Create HTML page for payment redirect with session data"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Snapp Pay - Payment Gateway</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .info {{ background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛒 Snapp Pay - Payment Gateway</h1>
                <div class="info">
                    <p><strong>Status:</strong> Redirecting to payment gateway...</p>
                    <p><strong>URL:</strong> {payment_url}</p>
                    <p><strong>Time:</strong> <span id="time"></span></p>
                </div>
                <p>If redirect doesn't work automatically, <a href="{payment_url}" target="_blank">click here</a>.</p>
            </div>
            
            <script>
                // Display current time
                document.getElementById('time').textContent = new Date().toLocaleString();
                
                // Redirect to payment gateway
                setTimeout(function() {{
                    window.location.href = "{payment_url}";
                }}, 1000);
                
                // Restore cookies if available
                {self._get_cookie_script(session_data.get('cookies', []))}
            </script>
        </body>
        </html>
        """
        
        with open('payment_portal.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _get_cookie_script(self, cookies):
        """Generate JavaScript for restoring cookies"""
        if not cookies:
            return "// No cookies to restore"
        
        cookie_scripts = []
        for cookie in cookies:
            cookie_scripts.append(f"document.cookie = '{cookie['name']}={cookie['value']}; path={cookie.get('path', '/')}; domain={cookie.get('domain', '')}';")
        
        return '\n'.join(cookie_scripts)
    
    def mark_as_processing(self, product_id):
        """Mark product as being processed"""
        self.processing_products.add(product_id)
    
    def mark_as_purchased(self, product_id):
        """Mark product as purchased"""
        self.purchased_products.add(product_id)
        if product_id in self.processing_products:
            self.processing_products.remove(product_id)