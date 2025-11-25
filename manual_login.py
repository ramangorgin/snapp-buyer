import webbrowser
import time

print("🚀 Manual Login Helper")
print("=" * 50)
print("I'll open the Snapp login page for you manually.")

# Open Snapp login page
snapp_url = "https://app.snapp.taxi/login"
print(f"📋 Opening: {snapp_url}")
webbrowser.open(snapp_url)

print("\n📝 Please complete these steps:")
print("1. Enter your phone number: 09014282751")
print("2. Wait for SMS code")
print("3. Enter the SMS code")
print("4. Login successfully")
print("5. Come back here and press Enter")

input("Press Enter AFTER you complete login in the browser...")

print("✅ Great! Now let's test if we can access Snapp Pay...")

# Try to open Snapp Pay page
snapp_pay_url = "https://snapppay.ir/timetable/"
print(f"📋 Opening Snapp Pay: {snapp_pay_url}")
webbrowser.open(snapp_pay_url)

print("\n🔍 Check if you can see the Black Friday products page.")
print("If you can see it, the automation should work!")