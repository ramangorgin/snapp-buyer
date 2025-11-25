import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.ai_navigator.openrouter_client import OpenRouterClient

logger = logging.getLogger(__name__)

class AdaptiveElementFinder:
    def __init__(self, driver, openrouter_client):
        self.driver = driver
        self.ai_client = openrouter_client
        self.wait = WebDriverWait(driver, 10)
    
    def get_page_html(self):
        """Get current page HTML for AI analysis"""
        return self.driver.page_source
    
    def find_products_on_landing_page(self):
        """Find products on the landing page using AI"""
        logger.info("🔍 AI analyzing landing page for products...")
        
        html = self.get_page_html()
        task = "Find all product elements on this landing page. Look for product cards, items, or any elements that might represent products for sale."
        context = "This is a Black Friday deals page. Products might be in cards, grids, or lists."
        
        analysis = self.ai_client.analyze_page(html, task, context)
        
        if "elements_found" in analysis:
            products = []
            for element in analysis["elements_found"]:
                if element.get("type") in ["product", "card", "item"]:
                    products.append({
                        "name": element.get("description", "Unknown Product"),
                        "selector": element.get("selector"),
                        "confidence": element.get("confidence", "low")
                    })
            return products
        else:
            logger.warning("❌ No products found by AI analysis")
            return []
    
    def find_add_to_cart_button(self):
        """Find add to cart button using AI"""
        logger.info("🔍 AI analyzing product page for add to cart button...")
        
        html = self.get_page_html()
        task = "Find the 'Add to Cart' button or any button that adds product to shopping cart. Also look for buy now, purchase, or similar buttons."
        context = "This is a product page. Need to find the button that adds item to cart."
        
        analysis = self.ai_client.analyze_page(html, task, context)
        
        if "elements_found" in analysis:
            for element in analysis["elements_found"]:
                if element.get("action") == "click" and "cart" in element.get("description", "").lower():
                    return element.get("selector")
        
        # Fallback: try common selectors
        common_selectors = [
            "button[class*='add-to-cart']",
            "button[class*='addToCart']", 
            "button[class*='cart']",
            "a[class*='add-to-cart']",
            "input[value*='Add to Cart']",
            "//button[contains(text(), 'Add to Cart')]",
            "//button[contains(text(), 'Add to Basket')]",
            "//a[contains(text(), 'Add to Cart')]"
        ]
        
        for selector in common_selectors:
            try:
                if selector.startswith("//"):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                return selector
            except:
                continue
        
        return None
    
    def find_payment_elements(self):
        """Find payment form elements using AI"""
        logger.info("🔍 AI analyzing checkout page for payment forms...")
        
        html = self.get_page_html()
        task = "Find all form elements needed for checkout: name, address, phone, email, payment method selection, and final purchase button."
        context = "This is a checkout/payment page. Need to find form fields and final purchase button."
        
        analysis = self.ai_client.analyze_page(html, task, context)
        
        form_elements = {}
        if "elements_found" in analysis:
            for element in analysis["elements_found"]:
                if element.get("type") == "input" or element.get("action") == "fill":
                    field_type = self._classify_form_field(element.get("description", ""))
                    if field_type:
                        form_elements[field_type] = element.get("selector")
        
        return form_elements
    
    def _classify_form_field(self, description: str) -> str:
        """Classify form field by description for Iranian forms"""
        description = description.lower()
        
        # Persian and English field mappings
        field_mappings = {
            'name': ['name', 'نام', 'نام و نام خانوادگی', 'fullname', 'full name'],
            'name_en': ['name en', 'نام انگلیسی', 'english name'],
            'national_code': ['national code', 'کد ملی', 'کدملی', 'code melli', 'melli code'],
            'birth_date': ['birth date', 'تاریخ تولد', 'تاریخ تولد شمسی', 'birthdate'],
            'birth_date_en': ['birth date en', 'تاریخ تولد میلادی', 'birthdate gregorian'],
            'birth_city': ['birth city', 'شهر تولد', 'محل تولد', 'birth place'],
            'gender': ['gender', 'جنسیت', 'sex', 'male/female', 'مرد/زن'],
            'phone': ['phone', 'mobile', 'تلفن', 'موبایل', 'شماره تماس', 'phone number'],
            'email': ['email', 'ایمیل', 'email address', 'پست الکترونیکی'],
            'address': ['address', 'آدرس', 'نشانی', 'complete address', 'آدرس کامل'],
            'city': ['city', 'شهر', 'city of residence', 'شهر محل سکونت'],
            'province': ['province', 'استان', 'ostan', 'state'],
            'postal_code': ['postal code', 'کد پستی', 'post code', 'zip code'],
            'father_name': ['father name', 'نام پدر', 'name of father'],
            'job': ['job', 'occupation', 'شغل', 'کار', 'occupation', 'profession'],
            'education': ['education', 'تحصیلات', 'education level', 'مدرک تحصیلی']
        }
        
        for field_name, keywords in field_mappings.items():
            if any(keyword in description for keyword in keywords):
                return field_name
        
        return None    
        
    def click_element(self, selector: str):
        """Click element using selector"""
        try:
            if selector.startswith("//"):
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            else:
                element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            
            element.click()
            logger.info(f"✅ Clicked element: {selector}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to click element {selector}: {e}")
            return False
    
    def fill_form_field(self, selector: str, value: str):
        """Fill form field with value"""
        try:
            if selector.startswith("//"):
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            else:
                element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            
            element.clear()
            element.send_keys(value)
            logger.info(f"✅ Filled field {selector} with: {value}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to fill field {selector}: {e}")
            return False