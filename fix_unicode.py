# fix_unicode.py - Run this once to fix Unicode issues
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("✅ Unicode fix applied - Windows console should now handle emojis properly")