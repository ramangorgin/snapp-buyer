import requests
import json

def test_openrouter(api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/snapp-buyer",
        "X-Title": "Snapp Buyer Test"
    }
    
    data = {
        "model": "google/gemini-flash-1.5-8b",
        "messages": [
            {"role": "user", "content": "Hello, are you working?"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            print("✅ API Key is working!")
            result = response.json()
            print(f"🤖 Response: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

# Test your API key
if __name__ == "__main__":
    your_api_key = "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"

    test_openrouter(your_api_key)