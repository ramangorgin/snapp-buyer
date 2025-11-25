import os
import time
import logging
import webbrowser
from src.ai_navigator.openrouter_client import OpenRouterClient
from src.utils.config import Config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleSnappBuyer:
    def __init__(self, api_key):
        self.config = Config()
        self.ai_client = OpenRouterClient(api_key)
        self.is_monitoring = False
        
    def setup(self):
        """Basic setup"""
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        print("✅ Setup complete")
    
    def manual_mode(self):
        """Manual monitoring mode with AI assistance"""
        print("\n" + "=" * 60)
        print("🎯 MANUAL SNAPP BUYER - AI ASSISTED")
        print("=" * 60)
        print("You're already logged in and on the deals page!")
        print("The AI will help analyze pages when needed.")
        print("\nCurrent Status:")
        print("✅ Logged into Snapp")
        print("✅ On deals page: https://snapppay.ir/timetable/")
        print("✅ AI system ready")
        print("✅ Monitoring ready for Black Friday")
        
        print("\n📋 FOR BLACK FRIDAY (December 6th 23:55):")
        print("1. Keep this page open: https://snapppay.ir/timetable/")
        print("2. At 23:55, start refreshing every 2-3 seconds")
        print("3. When products become clickable, click FAST!")
        print("4. Use AI analysis below if you need help finding elements")
        print("5. Complete checkout manually")
        
        self.ai_assistant()
    
    def ai_assistant(self):
        """AI assistant for element finding"""
        print("\n" + "=" * 60)
        print("🤖 AI PAGE ANALYZER")
        print("=" * 60)
        print("Paste HTML from any page and AI will find elements for you!")
        print("Commands: 'analyze', 'test', 'help', 'quit'")
        
        while True:
            command = input("\n🔍 Enter command: ").strip().lower()
            
            if command == 'quit':
                print("👋 Good luck with Black Friday!")
                break
                
            elif command == 'test':
                self.test_ai()
                
            elif command == 'analyze':
                self.analyze_page()
                
            elif command == 'help':
                print("\n📖 AVAILABLE COMMANDS:")
                print("analyze - Paste HTML and find elements")
                print("test    - Test AI with sample HTML") 
                print("help    - Show this help")
                print("quit    - Exit program")
                
            else:
                print("❌ Unknown command. Type 'help' for options.")
    
    def test_ai(self):
        """Test AI with sample HTML"""
        print("\n🧪 Testing AI with sample HTML...")
        
        sample_html = """
        <div class="product-card">
            <img src="samsung-s25.jpg" alt="Samsung S25">
            <h3 class="product-title">سامسونگ S25 اولترا</h3>
            <div class="product-price">15,000,000 تومان</div>
            <button class="add-to-cart-btn">افزودن به سبد خرید</button>
        </div>
        <button class="load-more">محصولات بیشتر</button>
        """
        
        task = "Find product elements and buttons"
        context = "Persian e-commerce page with Black Friday deals"
        
        result = self.ai_client.analyze_page(sample_html, task, context)
        
        print("🤖 AI ANALYSIS RESULT:")
        print("-" * 40)
        if "elements_found" in result:
            for i, element in enumerate(result["elements_found"], 1):
                print(f"{i}. {element['type'].upper()}: {element['description']}")
                print(f"   Selector: {element['selector']}")
                print(f"   Action: {element['action']} | Confidence: {element['confidence']}")
        else:
            print("❌ Analysis failed:", result.get('error', 'Unknown error'))
        print("-" * 40)
    
    def analyze_page(self):
        """Analyze user-pasted HTML"""
        print("\n📝 Paste the HTML code you want to analyze:")
        print("(Copy HTML from browser developer tools - F12)")
        print("Type 'END' on a new line when finished:")
        
        html_lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            html_lines.append(line)
        
        html_content = '\n'.join(html_lines)
        
        if not html_content.strip():
            print("❌ No HTML provided")
            return
        
        print("🔍 Analyzing HTML...")
        
        task = "Find all interactive elements: products, buttons, forms, links"
        context = "Snapp Pay Black Friday deals page"
        
        result = self.ai_client.analyze_page(html_content, task, context)
        
        print("\n🎯 ANALYSIS RESULTS:")
        print("=" * 50)
        
        if "elements_found" in result:
            print(f"Found {len(result['elements_found'])} elements:")
            print("-" * 50)
            
            # Group by type
            products = [e for e in result["elements_found"] if e["type"] == "product"]
            buttons = [e for e in result["elements_found"] if e["type"] == "button"]
            forms = [e for e in result["elements_found"] if e["type"] == "form"]
            other = [e for e in result["elements_found"] if e["type"] not in ["product", "button", "form"]]
            
            if products:
                print("\n🛍️ PRODUCTS:")
                for element in products:
                    print(f"  • {element['description']}")
                    print(f"    CSS: {element['selector']}")
            
            if buttons:
                print("\n🔘 BUTTONS:")
                for element in buttons:
                    print(f"  • {element['description']}")
                    print(f"    CSS: {element['selector']}")
                    print(f"    Action: {element['action']}")
            
            if forms:
                print("\n📝 FORMS:")
                for element in forms:
                    print(f"  • {element['description']}")
                    print(f"    CSS: {element['selector']}")
            
            if other:
                print("\n🔗 OTHER ELEMENTS:")
                for element in other:
                    print(f"  • {element['type']}: {element['description']}")
                    print(f"    CSS: {element['selector']}")
                    
        else:
            print("❌ Analysis failed:", result.get('error', 'Unknown error'))
        
        print("=" * 50)

def main():
    print("🎯 Simple Snapp Buyer - AI Assisted")
    print("=" * 50)
    
    api_key = "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"
    
    buyer = SimpleSnappBuyer(api_key)
    
    try:
        # Setup
        buyer.setup()
        
        # Test AI
        print("🤖 Testing AI connection...")
        if buyer.ai_client.test_connection():
            print("✅ AI system ready!")
        else:
            print("❌ AI connection failed")
            return
        
        # Start manual mode
        buyer.manual_mode()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()