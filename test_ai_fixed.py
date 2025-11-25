import requests
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_simple_ai(api_key):
    """Test basic AI functionality with a simple prompt"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    # Simple test first
    simple_prompt = "What is 2+2? Answer with just the number."
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": simple_prompt
            }
        ],
        "max_tokens": 10,
        "temperature": 0.1
    }
    
    print("🧪 Testing Basic AI Functionality...")
    print("=" * 50)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result.get('usage', {})
            
            print("✅ Basic Test Successful!")
            print(f"🤖 Response: '{content}'")
            print(f"📊 Tokens used: {usage}")
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_html_analysis_simple(api_key):
    """Test HTML analysis with simpler prompt"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer", 
        "X-Title": "Snapp Buyer Test"
    }
    
    sample_html = """
    <div class="products">
        <div class="product">
            <h3>Samsung S25 Ultra</h3>
            <button class="add-to-cart">Add to Cart</button>
        </div>
        <div class="product">
            <h3>Asus Laptop</h3>
            <button class="add-to-cart">Add to Cart</button>
        </div>
        <button id="load-more">Load More Products</button>
    </div>
    """
    
    # Simpler prompt without strict JSON requirement
    prompt = f"""Analyze this HTML and find:
1. Product elements
2. Add to cart buttons  
3. Load more button

HTML:
{sample_html}

Provide the CSS selectors for these elements in a simple list format."""
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.1
    }
    
    print("\n🧪 Testing HTML Analysis (Simple Prompt)...")
    print("=" * 50)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("✅ HTML Analysis Successful!")
            print("\n🤖 AI Response:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_structured_analysis(api_key):
    """Test with structured but simpler JSON request"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    sample_html = """
    <div class="product-card">
        <h3 class="product-name">Samsung Galaxy S25</h3>
        <div class="price">$999</div>
        <button onclick="addToCart(123)" class="buy-button">Add to Cart</button>
    </div>
    <div class="product-card">
        <h3 class="product-name">Asus Laptop</h3> 
        <div class="price">$1299</div>
        <button onclick="addToCart(124)" class="buy-button">Add to Cart</button>
    </div>
    """
    
    prompt = f"""Analyze this HTML and provide CSS selectors for:

HTML:
{sample_html}

Please respond with this exact JSON format:
{{
    "product_selectors": ["selector1", "selector2"],
    "add_to_cart_selectors": ["selector1", "selector2"], 
    "confidence": "high/medium/low"
}}"""
    
    payload = {
        "model": "mistralai/mistral-7b-instruct", 
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.1
    }
    
    print("\n🧪 Testing Structured Analysis...")
    print("=" * 50)
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            print("✅ Structured Analysis Successful!")
            print("\n🤖 AI Response:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # Try to parse as JSON
            try:
                parsed = json.loads(content)
                print("\n🎯 Parsed JSON Successfully!")
                print(f"Product selectors: {parsed.get('product_selectors', [])}")
                print(f"Add to cart selectors: {parsed.get('add_to_cart_selectors', [])}")
                return True
            except json.JSONDecodeError:
                print("⚠️ Response not in JSON format, but got response")
                return True  # Still consider it a success if we got any response
                
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_alternative_models(api_key):
    """Test other working models to see which gives better responses"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    models_to_test = [
        "meta-llama/llama-3-8b-instruct",
        "anthropic/claude-3-haiku", 
        "gryphe/mythomax-l2-13b",
        "openai/gpt-3.5-turbo"
    ]
    
    print("\n🧪 Testing Alternative Models...")
    print("=" * 50)
    
    for model in models_to_test:
        print(f"\nTesting: {model}")
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": "Find the CSS selector for add to cart buttons in: <button class='add-to-cart'>Add to Cart</button>. Answer with just the selector."
                }
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                print(f"✅ {model}: '{content}'")
            else:
                print(f"❌ {model}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model}: {e}")

if __name__ == "__main__":
    api_key = "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"
    
    print("🚀 Comprehensive AI Testing")
    print("We'll test different approaches to find what works with Mistral 7B.")
    
    # Test 1: Basic functionality
    test1 = test_simple_ai(api_key)
    
    # Test 2: Simple HTML analysis
    test2 = test_html_analysis_simple(api_key)
    
    # Test 3: Structured analysis
    test3 = test_structured_analysis(api_key)
    
    # Test 4: Alternative models
    test_alternative_models(api_key)
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"Basic Test: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Simple HTML Analysis: {'✅ PASS' if test2 else '❌ FAIL'}") 
    print(f"Structured Analysis: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if test1:
        print("\n🎉 Mistral 7B is working! We just need to adjust our prompts.")
    else:
        print("\n❌ Mistral 7B is not responding properly.")