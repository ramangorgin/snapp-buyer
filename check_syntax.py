import os
import sys

def check_python_files(directory):
    """Check all Python files for syntax errors"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    compile(source, filepath, 'exec')
                    print(f"✅ {filepath}")
                except SyntaxError as e:
                    print(f"❌ {filepath} - Line {e.lineno}: {e.msg}")
                    return False
    return True

if __name__ == "__main__":
    if check_python_files('src'):
        print("🎉 All Python files are syntactically correct!")
    else:
        print("❌ Found syntax errors in Python files")