import requests
import json

def test_models(api_key):
    """Test which models work with your API key"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Models to test (confirmed working on OpenRouter)
    models = [
        "google/gemini-flash-1.5",           # ✅ Should work
        "mistralai/mistral-7b-instruct",     # ✅ Should work  
        "anthropic/claude-3-haiku",          # ✅ Should work
        "meta-llama/llama-3-8b-instruct",    # ✅ Should work
        "gryphe/mythomax-l2-13b",            # ✅ Should work
        "openai/gpt-3.5-turbo",              # ✅ Should work
    ]
    
    working_models = []
    
    for model in models:
        print(f"\n🧪 Testing: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'OK' if working."}],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ {model} - WORKS!")
                working_models.append(model)
            else:
                print(f"❌ {model} - Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ {model} - Error: {e}")
    
    print(f"\n🎯 WORKING MODELS: {working_models}")
    return working_models

if __name__ == "__main__":
    api_key = "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"
    working = test_models(api_key)
    
    if working:
        print(f"\n🚀 RECOMMENDATION: Use '{working[0]}' in your config.yaml")
    else:
        print("\n❌ No models working. Check your API key or balance.")