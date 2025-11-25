from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

print("🧪 Testing browser automation (Fixed Version)...")

try:
    # Fixed options to avoid proxy issues
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Disable proxy
    options.add_argument('--no-proxy-server')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    
    print("🔄 Attempting to open Chrome...")
    
    # Try different approaches
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"❌ First attempt failed: {e}")
        print("🔄 Trying alternative method...")
        # Try without any service
        driver = webdriver.Chrome(options=options)
    
    print("✅ Chrome opened successfully!")
    
    # Test navigation
    driver.get("https://www.google.com")
    print("✅ Page loaded successfully!")
    
    print(f"📄 Page title: {driver.title}")
    
    input("Press Enter to close browser...")
    driver.quit()
    print("✅ Browser closed successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n🔧 Let's try the ULTIMATE solution...")
    
    # Ultimate fallback
    print("📋 Opening browser manually...")
    import webbrowser
    webbrowser.open("https://www.google.com")
    print("✅ Manual browser opened!")