import os
import time
import threading
import logging
from datetime import datetime
from src.auth.snap_auth import SnapAuthenticator
from src.monitor.product_monitor import ProductMonitor
from src.browser.session_manager import SessionManager
from src.payment.payment_handler import PaymentHandler
from src.ai_navigator.openrouter_client import OpenRouterClient
from src.adaptive_scraper.element_finder import AdaptiveElementFinder
from src.utils.config import Config

def setup_logging():
    """Setup logging that handles Unicode characters properly"""
    class UnicodeFilter(logging.Filter):
        def filter(self, record):
            # Replace Unicode emojis with text equivalents for Windows console
            if hasattr(record, 'msg') and isinstance(record.msg, str):
                record.msg = record.msg.replace('✅', '[OK]')
                record.msg = record.msg.replace('❌', '[ERROR]')
                record.msg = record.msg.replace('⚠️', '[WARN]')
                record.msg = record.msg.replace('🔐', '[AUTH]')
                record.msg = record.msg.replace('👀', '[MONITOR]')
                record.msg = record.msg.replace('🤖', '[AI]')
                record.msg = record.msg.replace('🎯', '[TARGET]')
                record.msg = record.msg.replace('🚀', '[START]')
                record.msg = record.msg.replace('🛑', '[STOP]')
                record.msg = record.msg.replace('🛠️', '[SETUP]')
                record.msg = record.msg.replace('🧪', '[TEST]')
                record.msg = record.msg.replace('🔧', '[FIX]')
                record.msg = record.msg.replace('💰', '[COST]')
                record.msg = record.msg.replace('📊', '[STATS]')
                record.msg = record.msg.replace('📦', '[PRODUCT]')
                record.msg = record.msg.replace('🌐', '[BROWSER]')
                record.msg = record.msg.replace('💳', '[PAYMENT]')
            return True

    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log', encoding='utf-8'),  # UTF-8 for file
            logging.StreamHandler()  # Plain text for console
        ]
    )
    
    # Add Unicode filter to console handler
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.addFilter(UnicodeFilter())

logger = logging.getLogger(__name__)

setup_logging()

class AdaptiveSnappBuyer:
    def __init__(self, openrouter_api_key: str):
        self.config = Config()
        self.authenticator = SnapAuthenticator()
        self.session_manager = SessionManager()
        
        # AI Components
        self.ai_client = OpenRouterClient(openrouter_api_key)
        self.element_finder = None
        
        self.monitor = ProductMonitor()
        self.payment_handler = PaymentHandler()
        
        self.is_running = False
        self.user_data = self._load_user_data()
    
    def _load_user_data(self):
        """Load user information for forms"""
        return {
            'name': "رامان گرگین پاوه" ,
            'name_en': "Raman Gorgin Paveh" ,
            'national_code': "0150629737" ,
            'birth_date': "1383/03/14"  ,
            'birth_date_en': "2004/06/04" ,
            'birth_city': "Karaj"  ,
            'gender': "male" ,
            'phone': "09014282751" ,
            'email': "raman.gorginpaveh@gmail.com" ,
            'alternative_phone': "09910946921",
            'address': "کرج،‌ جهانشهر، بلوار مولانا، خیابان ترانه شرقی، پلاک ۱۶ واحد ۱۹"  ,
            'city': "Karaj"  ,
            'province': "Alborz"  ,
            'home_phone': "02634404954",
            'postal_code': "3148612345"  ,
            'father_name': "محمدرضا" ,
            'job': "برنامه‌نویس",
            'education': "دیپلم" 
        }
    
    def setup(self):
        """Setup the application"""
        logger.info("🛠️ Setting up application...")
        
        # Create necessary directories
        os.makedirs('data/cookies', exist_ok=True)
        os.makedirs('data/sessions', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        
        logger.info("✅ Application setup complete")
    
    def manual_login(self):
        """Start browser, perform manual login, then init AI components"""
        logger.info("🔐 Initiating manual login...")

        # Ensure authenticator has a driver (use SessionManager Selenium Manager flow)
        if not self.authenticator.driver:
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                driver = self.session_manager.create_driver(headless=self.config.get('browser.headless', False))
                self.authenticator.driver = driver
                self.authenticator.wait = WebDriverWait(driver, 20)
            except Exception as e:
                logger.error(f"❌ Failed to create Selenium driver: {e}. Falling back to manual browser open.")
        
        login_success = self.authenticator.manual_login()

        if login_success:
            logger.info("✅ Login successful (manual)")
            if self.authenticator.driver:
                self.element_finder = AdaptiveElementFinder(
                    self.authenticator.driver,
                    self.ai_client
                )
            self.session_manager.save_session()
            return True
        else:
            logger.error("❌ Login failed")
            return False
    
    def test_landing_page_analysis(self):
        """Test AI analysis on current landing page"""
        logger.info("🧪 Testing landing page analysis...")
        
        if not self.element_finder:
            logger.error("❌ Element finder not initialized. Please login first.")
            return
        
        # Navigate to deals page
        self.authenticator.driver.get(self.config.get('snapp.snapp_pay_url'))
        time.sleep(5)
        
        # Analyze page for products
        products = self.element_finder.find_products_on_landing_page()
        
        logger.info(f"📊 AI Analysis Results:")
        logger.info(f"Found {len(products)} potential product elements")
        
        for i, product in enumerate(products, 1):
            logger.info(f"  {i}. {product['name']} - Selector: {product['selector']} - Confidence: {product['confidence']}")
        
        if not products:
            logger.warning("⚠️ No products found. This might be normal before the sale starts.")
            logger.info("💡 The system will retry during the actual sale time.")
        
        return products
    
    def simulate_product_purchase_flow(self):
        """Simulate complete purchase flow for testing"""
        logger.info("🔄 Simulating purchase flow...")
        
        if not self.element_finder:
            logger.error("❌ Element finder not initialized")
            return False
        
        try:
            # Step 1: Find and click a product (when available)
            products = self.element_finder.find_products_on_landing_page()
            if not products:
                logger.warning("⏸️ No products available for testing")
                return True  # This is expected before sale
            
            # Step 2: Find add to cart button
            cart_button = self.element_finder.find_add_to_cart_button()
            if cart_button:
                logger.info(f"🛒 Add to cart button found: {cart_button}")
                # In real scenario: self.element_finder.click_element(cart_button)
            else:
                logger.warning("⏸️ No add to cart button found (expected before sale)")
            
            # Step 3: Find payment form elements
            form_elements = self.element_finder.find_payment_elements()
            logger.info(f"📝 Form elements found: {len(form_elements)}")
            
            for field, selector in form_elements.items():
                logger.info(f"  - {field}: {selector}")
            
            logger.info("✅ Purchase flow simulation completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Purchase flow simulation failed: {e}")
            return False
    
    def start_adaptive_monitoring(self):
        """Start AI-powered adaptive monitoring"""
        logger.info("👁️ Starting adaptive monitoring...")
        
        self.is_running = True
        monitor_thread = threading.Thread(target=self._adaptive_monitoring_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        logger.info("✅ Adaptive monitoring started")
    
    def _adaptive_monitoring_loop(self):
        """Main adaptive monitoring loop"""
        while self.is_running:
            try:
                # Check if sale has started by looking for active product links
                products = self.element_finder.find_products_on_landing_page()
                
                active_products = []
                for product in products:
                    if product.get('confidence') in ['high', 'medium']:
                        active_products.append(product)
                
                if active_products:
                    logger.info(f"🎯 Active products detected: {len(active_products)}")
                    self._handle_active_products(active_products)
                
                time.sleep(self.config.get('monitor.refresh_interval', 2))
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(5)
    
    def _handle_active_products(self, active_products):
        """Handle detected active products"""
        for product in active_products:
            if self._should_process_product(product):
                logger.info(f"🚀 Processing product: {product['name']}")
                
                # Process in separate thread
                thread = threading.Thread(
                    target=self._process_single_product,
                    args=(product,)
                )
                thread.start()
    
    def _should_process_product(self, product):
        """Check if product should be processed"""
        # Add your logic here - check priority, avoid duplicates, etc.
        return True
    
    def _process_single_product(self, product):
        """Process a single product through purchase flow"""
        try:
            # Click on product
            if self.element_finder.click_element(product['selector']):
                time.sleep(3)
                
                # Add to cart
                cart_button = self.element_finder.find_add_to_cart_button()
                if cart_button and self.element_finder.click_element(cart_button):
                    time.sleep(2)
                    
                    # Handle checkout forms
                    if self._complete_checkout_forms():
                        logger.info(f"✅ Successfully processed: {product['name']}")
                    else:
                        logger.error(f"❌ Checkout failed for: {product['name']}")
                else:
                    logger.error(f"❌ Cannot add to cart: {product['name']}")
            else:
                logger.error(f"❌ Cannot click product: {product['name']}")
                
        except Exception as e:
            logger.error(f"❌ Error processing {product['name']}: {e}")
    
    def _complete_checkout_forms(self):
        """Complete all checkout forms using AI"""
        try:
            form_elements = self.element_finder.find_payment_elements()
            
            # Fill all detected form fields
            for field_type, selector in form_elements.items():
                if field_type in self.user_data:
                    value = self.user_data[field_type]
                    self.element_finder.fill_form_field(selector, value)
                    time.sleep(0.5)
            
            # Find and click final purchase button
            purchase_buttons = [
                "//button[contains(text(), 'Purchase')]",
                "//button[contains(text(), 'Pay')]",
                "//button[contains(text(), 'Complete')]",
                "//input[@type='submit']"
            ]
            
            for button_selector in purchase_buttons:
                if self.element_finder.click_element(button_selector):
                    logger.info("✅ Purchase button clicked")
                    return True
            
            logger.warning("⚠️ No purchase button found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Checkout form completion failed: {e}")
            return False
    
    def stop(self):
        """Stop the application"""
        self.is_running = False
        logger.info("🛑 Application stopped")

def main():
    """Main application entry point"""
    print("🎯 Starting Adaptive Snapp Buyer")
    print("=" * 50)
    
    api_key = "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"
    
    buyer = AdaptiveSnappBuyer(api_key)

    # Test API connection first
    if buyer.ai_client.test_connection():
        print("✅ OpenRouter connection successful!")
    else:
        print("❌ OpenRouter connection failed. Check your API key.")
        return
    
    try:
        # Setup
        buyer.setup()
        
        # Manual login (opens browser and waits internally)
        print("\n1. 🔐 Manual Login")
        print("Launching browser for login...")
        if buyer.manual_login():
            print("✅ Login successful")
            
            # Test landing page analysis
            print("\n2. 🧪 Testing Landing Page Analysis")
            buyer.test_landing_page_analysis()
            
            # Test purchase flow simulation
            print("\n3. 🔄 Testing Purchase Flow")
            buyer.simulate_product_purchase_flow()
            
            print("\n4. 👁️ Starting Monitoring")
            print("System is ready for Black Friday sale!")
            print("The AI will automatically detect and process products when available.")
            
            buyer.start_adaptive_monitoring()
            
            # Keep application running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Application stopped by user")
                buyer.stop()
        
        else:
            print("❌ Login failed")
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()