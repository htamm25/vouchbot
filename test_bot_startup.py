#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test khởi động bot với mock environment
"""

import os
import sys
import tempfile
import asyncio
from unittest.mock import patch, MagicMock

def test_bot_initialization():
    """Test khởi tạo bot object"""
    try:
        # Set mock environment
        os.environ['DISCORD_TOKEN'] = 'mock_token_for_testing'
        
        # Import sau khi set env
        import discord
        from discord.ext import commands
        
        # Test tạo intents
        intents = discord.Intents.default()
        intents.message_content = False
        intents.guilds = True
        intents.guild_messages = True
        
        # Test tạo bot
        bot = commands.Bot(command_prefix="/", intents=intents)
        
        print("✅ Bot object được tạo thành công!")
        print(f"   - Bot user: {bot.user}")
        print(f"   - Command prefix: {bot.command_prefix}")
        print(f"   - Intents: guilds={intents.guilds}, messages={intents.guild_messages}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khởi tạo bot: {e}")
        return False

def test_config_functions():
    """Test các functions load/save config"""
    try:
        # Import functions từ file chính
        sys.path.insert(0, '.')
        
        # Test với temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_config = f.name
            
        # Mock CONFIG_FILE
        with patch('vouch_bot1.CONFIG_FILE', temp_config):
            from vouch_bot1 import load_config, save_config
            
            # Test save config
            test_data = {"test_guild": {"thankyou": "Test message"}}
            save_config(test_data)
            
            # Test load config
            loaded_data = load_config()
            
            if loaded_data == test_data:
                print("✅ Config load/save functions hoạt động tốt!")
                result = True
            else:
                print(f"❌ Config data không khớp: {loaded_data} != {test_data}")
                result = False
                
        # Cleanup
        os.unlink(temp_config)
        return result
        
    except Exception as e:
        print(f"❌ Lỗi test config functions: {e}")
        return False

def test_modal_classes():
    """Test các Modal classes"""
    try:
        # Test import classes
        from vouch_bot1 import ThankYouModal, FeedbackModal, StarButton, VouchView
        
        print("✅ ThankYouModal class import thành công")
        print("✅ FeedbackModal class import thành công")
        print("✅ StarButton class import thành công")
        print("✅ VouchView class import thành công")
        
        # Test class attributes
        if hasattr(ThankYouModal, 'on_submit'):
            print("✅ ThankYouModal có method on_submit")
        
        if hasattr(FeedbackModal, 'on_submit'):
            print("✅ FeedbackModal có method on_submit")
            
        if hasattr(StarButton, 'callback'):
            print("✅ StarButton có method callback")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test modal classes: {e}")
        return False

def main():
    print("🧪 Test khởi động VouchBot...\n")
    
    tests = [
        ("Bot initialization", test_bot_initialization),
        ("Config functions", test_config_functions),
        ("Modal classes", test_modal_classes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}:")
        if test_func():
            passed += 1
        print()
    
    print(f"📊 Kết quả: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Tất cả tests PASS! Bot sẵn sàng hoạt động.")
        return 0
    else:
        print("❌ Một số tests FAIL! Cần kiểm tra lại.")
        return 1

if __name__ == "__main__":
    sys.exit(main())