#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra syntax và import của VouchBot
"""

import sys
import os

def test_imports():
    """Test tất cả imports cần thiết"""
    try:
        import discord
        from discord import app_commands
        from discord.ext import commands
        from dotenv import load_dotenv
        import json
        import logging
        print("✅ Tất cả imports thành công!")
        print(f"   - Discord.py version: {discord.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Lỗi import: {e}")
        return False

def test_syntax():
    """Test syntax của file chính"""
    try:
        # Đọc và compile file chính
        with open('vouch_bot1.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'vouch_bot1.py', 'exec')
        print("✅ Syntax check thành công!")
        return True
    except SyntaxError as e:
        print(f"❌ Lỗi syntax: {e}")
        print(f"   Dòng {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Lỗi khác: {e}")
        return False

def test_config_files():
    """Test các file cấu hình"""
    files_to_check = [
        ('.env.example', 'File template environment'),
        ('.env', 'File environment (cần có token thực)'),
        ('requirements.txt', 'File dependencies'),
        ('README.md', 'File documentation')
    ]
    
    for filename, description in files_to_check:
        if os.path.exists(filename):
            print(f"✅ {description}: {filename}")
        else:
            print(f"⚠️  {description}: {filename} - không tồn tại")

def main():
    print("🧪 Bắt đầu kiểm tra VouchBot...\n")
    
    # Test imports
    print("1. Kiểm tra imports:")
    import_ok = test_imports()
    print()
    
    # Test syntax
    print("2. Kiểm tra syntax:")
    syntax_ok = test_syntax()
    print()
    
    # Test config files
    print("3. Kiểm tra files cấu hình:")
    test_config_files()
    print()
    
    # Kết quả tổng
    if import_ok and syntax_ok:
        print("🎉 Tất cả kiểm tra đều PASS!")
        print("💡 Bot sẵn sàng chạy khi có Discord token hợp lệ.")
        return 0
    else:
        print("❌ Có lỗi cần sửa!")
        return 1

if __name__ == "__main__":
    sys.exit(main())