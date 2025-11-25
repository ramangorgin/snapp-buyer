from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

print("🧪 Testing browser automation...")

try:
    # Try with basic options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("🔄 Attempting to open Chrome...")
    driver = webdriver.Chrome(options=options)
    
    print("✅ Chrome opened successfully!")
    driver.get("https://www.google.com")
    print("✅ Page loaded successfully!")
    
    input("Press Enter to close browser...")
    driver.quit()
    print("✅ Browser closed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Troubleshooting steps:")
    print("1. Make sure Google Chrome is installed")
    print("2. Check if ChromeDriver is compatible with your Chrome version")
    print("3. Try running as Administrator")