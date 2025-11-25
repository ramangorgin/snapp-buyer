try:
    import selenium
    print("✅ selenium installed")
except ImportError:
    print("❌ selenium missing")

try:
    import requests
    print("✅ requests installed")
except ImportError:
    print("❌ requests missing")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ webdriver-manager installed")
except ImportError:
    print("❌ webdriver-manager missing")

try:
    import yaml
    print("✅ pyyaml installed")
except ImportError:
    print("❌ pyyaml missing")

print("\nRunning basic browser test...")
try:
    import os, sys, platform
    from selenium import webdriver
    # Use Selenium Manager (built into Selenium 4.15) instead of webdriver-manager

    # Bypass any system/environment proxy settings for this test
    for key in ['HTTP_PROXY','http_proxy','HTTPS_PROXY','https_proxy','ALL_PROXY','all_proxy']:
        os.environ.pop(key, None)
    os.environ.setdefault('NO_PROXY', '*')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--proxy-server=direct://')
    options.add_argument('--proxy-bypass-list=*')

    print(f"Python: {sys.version}")
    print(f"Platform: {platform.platform()} | Arch: {platform.machine()} | Bits: {platform.architecture()}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    print("✅ Browser test successful!")
    driver.quit()
except Exception as e:
    print(f"❌ Browser test failed: {e}")
