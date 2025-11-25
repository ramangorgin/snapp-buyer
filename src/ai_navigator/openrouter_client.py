import requests
import json
import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self, api_key: str, model: str = "mistralai/mistral-7b-instruct"):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/snapp-buyer",
            "X-Title": "Snapp Buyer Automation"
        }
    
    def analyze_page(self, html_content: str, task: str, context: Dict = None) -> Dict[str, Any]:
        """Analyze page content using AI to find elements and actions"""
        try:
            prompt = self._build_prompt(html_content, task, context)
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.1
            }
            
            logger.info(f"🤖 Sending request to {self.model}...")
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                usage = result.get('usage', {})
                logger.info(f"✅ AI analysis complete - Tokens: {usage.get('total_tokens', 0)}")
                return self._parse_ai_response(content)
            else:
                logger.error(f"❌ OpenRouter API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except requests.Timeout:
            logger.error("❌ AI analysis timeout")
            return {"error": "Timeout"}
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {e}")
            return {"error": str(e)}
    
    def _build_prompt(self, html_content: str, task: str, context: Dict) -> str:
        """Build prompt for specific tasks"""
        # Clean HTML - remove excessive whitespace
        cleaned_html = ' '.join(html_content[:2000].split())  # Reduced for Mistral
        
        base_prompt = f"""
TASK: {task}

HTML CONTENT:
{cleaned_html}

CONTEXT: {context or 'E-commerce page with products'}

INSTRUCTIONS:
Analyze the HTML and find elements for web automation. Provide CSS selectors.

Respond with ONLY this JSON format, no other text:
{{
    "elements_found": [
        {{
            "type": "product|button|form",
            "description": "brief description",
            "selector": "css selector",
            "action": "click|fill",
            "confidence": "high|medium|low"
        }}
    ]
}}
"""
        return base_prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured data with better error handling"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove common prefixes/suffixes that Mistral adds
            cleaned_text = re.sub(r'^[\s\S]*?\{', '{', cleaned_text)  # Remove everything before first {
            cleaned_text = re.sub(r'\}[\s\S]*?$', '}', cleaned_text)  # Remove everything after last }
            
            # Remove specific Mistral artifacts
            cleaned_text = cleaned_text.replace('<s> [OUT]', '').replace('[/OUT]', '')
            cleaned_text = cleaned_text.replace('```json', '').replace('```', '')
            cleaned_text = cleaned_text.strip()
            
            # Try to parse as JSON
            parsed_data = json.loads(cleaned_text)
            logger.info(f"✅ Successfully parsed AI response with {len(parsed_data.get('elements_found', []))} elements")
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ Failed to parse AI response as JSON: {e}")
            logger.warning(f"Raw response: {response_text[:200]}...")
            
            # Fallback: extract selectors using regex
            return self._extract_selectors_fallback(response_text)
    
    def _extract_selectors_fallback(self, response_text: str) -> Dict[str, Any]:
        """Fallback method to extract selectors when JSON parsing fails"""
        elements = []
        
        # Look for CSS selectors in the text
        css_selectors = re.findall(r'[\."#\w\-\s]+\{', response_text)
        css_selectors.extend(re.findall(r'[\."#\w\-\s]+\.[\w\-]+', response_text))
        css_selectors.extend(re.findall(r'#[\w\-]+', response_text))
        
        # Also look for common patterns
        if 'add-to-cart' in response_text.lower() or 'افزودن' in response_text:
            elements.append({
                "type": "button",
                "description": "Add to cart button (fallback)",
                "selector": "button.add-to-cart, .add-to-cart, [class*='cart']",
                "action": "click",
                "confidence": "medium"
            })
        
        if 'product' in response_text.lower() or 'محصول' in response_text:
            elements.append({
                "type": "product", 
                "description": "Product item (fallback)",
                "selector": ".product, [class*='product'], .item, [class*='item']",
                "action": "click",
                "confidence": "medium"
            })
        
        # Add any found CSS selectors
        for selector in set(css_selectors[:5]):  # Limit to 5 unique selectors
            if len(selector) > 2 and '{' not in selector:
                elements.append({
                    "type": "element",
                    "description": f"Found selector: {selector}",
                    "selector": selector.strip(),
                    "action": "click",
                    "confidence": "low"
                })
        
        return {
            "elements_found": elements,
            "recommended_actions": ["Use fallback selectors"],
            "fallback_used": True
        }
    
    def test_connection(self) -> bool:
        """Test if API key and connection work"""
        try:
            test_payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Say 'OK' if working."}],
                "max_tokens": 10
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ OpenRouter connection test SUCCESS with {self.model}")
                return True
            else:
                logger.error(f"❌ OpenRouter connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ OpenRouter connection test error: {e}")
            return False