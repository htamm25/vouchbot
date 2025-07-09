#!/usr/bin/env python3
"""
Script kiểm tra bot sẵn sàng deploy lên Railway
"""

import os
import sys
import json
import requests
from pathlib import Path

def check_files():
    """Kiểm tra các file cần thiết"""
    required_files = [
        'vouch_bot1.py',
        'requirements.txt', 
        'Procfile',
        'railway.json',
        'runtime.txt',
        '.dockerignore',
        '.gitignore',
        '.env.example'
    ]
    
    print("🔍 Kiểm tra files cần thiết...")
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - THIẾU")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_env_variables():
    """Kiểm tra environment variables"""
    print("\n🔍 Kiểm tra environment variables...")
    
    # Kiểm tra .env file
    if Path('.env').exists():
        print("  ✅ File .env tồn tại")
        
        # Đọc và kiểm tra DISCORD_TOKEN
        try:
            with open('.env', 'r') as f:
                content = f.read()
                if 'DISCORD_TOKEN=' in content and len(content.split('DISCORD_TOKEN=')[1].split('\n')[0].strip()) > 50:
                    print("  ✅ DISCORD_TOKEN có vẻ hợp lệ")
                else:
                    print("  ❌ DISCORD_TOKEN không hợp lệ hoặc thiếu")
                    return False
        except Exception as e:
            print(f"  ❌ Lỗi đọc .env: {e}")
            return False
    else:
        print("  ❌ File .env không tồn tại")
        return False
    
    return True

def check_requirements():
    """Kiểm tra requirements.txt"""
    print("\n🔍 Kiểm tra requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = ['discord.py', 'python-dotenv']
        
        for package in required_packages:
            if package in content:
                print(f"  ✅ {package}")
            else:
                print(f"  ❌ {package} - THIẾU")
                return False
                
        return True
    except Exception as e:
        print(f"  ❌ Lỗi đọc requirements.txt: {e}")
        return False

def check_procfile():
    """Kiểm tra Procfile"""
    print("\n🔍 Kiểm tra Procfile...")
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            
        if content == 'web: python vouch_bot1.py':
            print("  ✅ Procfile cấu hình đúng")
            return True
        else:
            print(f"  ❌ Procfile sai: {content}")
            return False
    except Exception as e:
        print(f"  ❌ Lỗi đọc Procfile: {e}")
        return False

def check_railway_json():
    """Kiểm tra railway.json"""
    print("\n🔍 Kiểm tra railway.json...")
    
    try:
        with open('railway.json', 'r') as f:
            config = json.load(f)
            
        if config.get('build', {}).get('builder') == 'NIXPACKS':
            print("  ✅ Builder cấu hình đúng")
        else:
            print("  ❌ Builder không đúng")
            return False
            
        if 'python vouch_bot1.py' in config.get('deploy', {}).get('startCommand', ''):
            print("  ✅ Start command đúng")
        else:
            print("  ❌ Start command không đúng")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ Lỗi đọc railway.json: {e}")
        return False

def check_gitignore():
    """Kiểm tra .gitignore"""
    print("\n🔍 Kiểm tra .gitignore...")
    
    try:
        with open('.gitignore', 'r') as f:
            content = f.read()
            
        important_ignores = ['.env', 'config.json', '*.log']
        
        for ignore in important_ignores:
            if ignore in content:
                print(f"  ✅ {ignore} được ignore")
            else:
                print(f"  ❌ {ignore} KHÔNG được ignore - BẢO MẬT")
                return False
                
        return True
    except Exception as e:
        print(f"  ❌ Lỗi đọc .gitignore: {e}")
        return False

def main():
    """Main function"""
    print("🚀 KIỂM TRA RAILWAY DEPLOYMENT READINESS\n")
    print("=" * 50)
    
    checks = [
        ("Files", check_files),
        ("Environment Variables", check_env_variables), 
        ("Requirements", check_requirements),
        ("Procfile", check_procfile),
        ("Railway Config", check_railway_json),
        ("Git Ignore", check_gitignore)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
            print()
        except Exception as e:
            print(f"  ❌ Lỗi kiểm tra {name}: {e}\n")
    
    print("=" * 50)
    print(f"📊 KẾT QUẢ: {passed}/{total} kiểm tra PASSED")
    
    if passed == total:
        print("\n🎉 BOT SẴN SÀNG DEPLOY LÊN RAILWAY!")
        print("\n📋 Các bước tiếp theo:")
        print("1. Push code lên GitHub repository")
        print("2. Tạo project mới trên Railway")
        print("3. Connect với GitHub repo")
        print("4. Thêm DISCORD_TOKEN vào Environment Variables")
        print("5. Deploy và monitor logs")
        return 0
    else:
        print("\n❌ VẪN CÒN VẤN ĐỀ CẦN SỬA")
        print("\n💡 Vui lòng sửa các lỗi trên trước khi deploy")
        return 1

if __name__ == "__main__":
    sys.exit(main())