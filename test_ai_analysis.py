import requests
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ai_html_analysis(api_key):
    """Test if the AI can analyze HTML and find elements for our use case"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    # Sample HTML that might be similar to Snapp landing page
    sample_html = """
    <div class="product-grid">
        <div class="product-item" data-product-id="123">
            <img src="samsung-s25.jpg" alt="Samsung S25 Ultra">
            <h3 class="product-title">Samsung S25 Ultra 256GB</h3>
            <div class="product-price">15,000,000 تومان</div>
            <button class="add-to-cart-btn" onclick="addToCart(123)">افزودن به سبد خرید</button>
        </div>
        <div class="product-item" data-product-id="124">
            <img src="asus-laptop.jpg" alt="Asus Laptop">
            <h3 class="product-title">Asus Vivobook X1504VA</h3>
            <div class="product-price">25,000,000 تومان</div>
            <button class="add-to-cart-btn" onclick="addToCart(124)">افزودن به سبد خرید</button>
        </div>
    </div>
    <div class="load-more-container">
        <button id="load-more-products" class="load-more-btn">محصولات بیشتر</button>
    </div>
    """
    
    prompt = f"""
    TASK: Find all product elements and interactive buttons on this e-commerce page.

    HTML CONTENT:
    {sample_html}

    INSTRUCTIONS:
    Analyze this HTML and identify:
    1. Product items/cards
    2. "Add to cart" buttons  
    3. "Load more products" button
    4. Any other interactive elements

    For each element, provide precise CSS selectors or XPaths.

    RESPONSE FORMAT - STRICT JSON ONLY:
    {{
        "elements_found": [
            {{
                "type": "button|link|form|input|product",
                "description": "what this element does",
                "selector": "css selector or xpath",
                "action": "click|fill|select",
                "confidence": "high|medium|low"
            }}
        ],
        "recommended_actions": ["step1", "step2"]
    }}

    Return ONLY valid JSON.
    """
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system", 
                "content": "You are a web automation expert. Analyze HTML and provide specific CSS selectors and XPaths for automation. Return ONLY valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.1
    }
    
    print("🧪 Testing AI HTML Analysis with Mistral 7B...")
    print("=" * 60)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            print("✅ AI Analysis Successful!")
            print(f"📊 Tokens used: {usage}")
            print("\n🤖 AI Response:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Try to parse the JSON response
            try:
                parsed = json.loads(content)
                print("\n🎯 Parsed Results:")
                if "elements_found" in parsed:
                    for i, element in enumerate(parsed["elements_found"], 1):
                        print(f"  {i}. {element['type']}: {element['description']}")
                        print(f"     Selector: {element['selector']}")
                        print(f"     Action: {element['action']} | Confidence: {element['confidence']}")
                
                if "recommended_actions" in parsed:
                    print(f"\n📋 Recommended Actions: {parsed['recommended_actions']}")
                    
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse AI response as JSON: {e}")
                print("Raw response might not be in correct format.")
                return False
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_real_snapp_scenario(api_key):
    """Test a more realistic scenario with Persian text"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    # More realistic Persian e-commerce HTML
    persian_html = """
    <div class="products-container">
        <div class="product-card">
            <div class="product-image">
                <img src="/images/samsung-s25.jpg" alt="موبایل سامسونگ اس۲۵ اولترا">
            </div>
            <div class="product-info">
                <h3 class="product-name">موبایل سامسونگ مدل Galaxy S25 Ultra 5G دو سیم کارت ظرفیت 256 گیگابایت</h3>
                <div class="product-price">
                    <span class="original-price">۷۵,۰۰۰,۰۰۰ تومان</span>
                    <span class="discounted-price">۱۵,۰۰۰,۰۰۰ تومان</span>
                </div>
                <button class="btn-add-to-cart" data-product="12345">
                    <span>افزودن به سبد خرید</span>
                </button>
            </div>
        </div>
        
        <div class="product-card">
            <div class="product-image">
                <img src="/images/ps5.jpg" alt="پلی استیشن 5">
            </div>
            <div class="product-info">
                <h3 class="product-name">کنسول بازی سونی مدل PlayStation 5 Slim Digital Edition ظرفیت 1 ترابایت</h3>
                <div class="product-price">
                    <span class="original-price">۳۵,۰۰۰,۰۰۰ تومان</span>
                    <span class="discounted-price">۷,۰۰۰,۰۰۰ تومان</span>
                </div>
                <button class="btn-add-to-cart" data-product="12346">
                    <span>افزودن به سبد خرید</span>
                </button>
            </div>
        </div>
    </div>
    <div class="pagination">
        <button class="btn-load-more" id="loadMoreProducts">نمایش محصولات بیشتر</button>
    </div>
    """
    
    prompt = f"""
    TASK: Analyze this Persian e-commerce page and find elements for automation.

    HTML CONTENT:
    {persian_html}

    CONTEXT: This is a Black Friday deals page with products in Persian/Farsi.

    INSTRUCTIONS:
    Find:
    1. Product cards/items
    2. "Add to cart" buttons (look for Persian text: "افزودن به سبد خرید")
    3. "Load more products" button
    4. Product names and prices

    Provide precise CSS selectors that would work for automation.

    RESPONSE FORMAT - STRICT JSON ONLY:
    {{
        "elements_found": [
            {{
                "type": "product|button|link",
                "description": "element description",
                "selector": "css selector",
                "action": "click|fill|select",
                "confidence": "high|medium|low"
            }}
        ],
        "recommended_actions": ["action1", "action2"]
    }}

    Return ONLY valid JSON.
    """
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a web automation expert. Analyze HTML with Persian text and provide specific CSS selectors. Return ONLY valid JSON."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.1
    }
    
    print("\n" + "=" * 60)
    print("🧪 Testing Persian E-commerce Analysis...")
    print("=" * 60)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("✅ Persian Analysis Successful!")
            print("\n🤖 AI Response:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Try to parse JSON
            try:
                parsed = json.loads(content)
                print("\n🎯 Found Elements:")
                for i, element in enumerate(parsed.get("elements_found", []), 1):
                    print(f"  {i}. [{element['type']}] {element['description']}")
                    print(f"     → {element['selector']}")
                    
                return True
            except json.JSONDecodeError:
                print("❌ Response not in JSON format")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    api_key = "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"
    
    print("🚀 Testing Mistral 7B AI for HTML Analysis")
    print("This will test if the AI can find product elements for automation.")
    
    # Test 1: Basic HTML analysis
    success1 = test_ai_html_analysis(api_key)
    
    # Test 2: Persian e-commerce analysis
    success2 = test_real_snapp_scenario(api_key)
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"Basic HTML Analysis: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"Persian E-commerce Analysis: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 EXCELLENT! Mistral 7B is ready for your Snapp buyer project!")
        print("The AI can analyze HTML and find elements for automation.")
    else:
        print("\n⚠️ Some tests failed. The AI might need adjustment.")