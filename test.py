#!/usr/bin/env python3
"""
Test Suite for Terminal Chat Bluetooth
Tests various components and provides demo functionality
"""

import os
import sys
import time
import tempfile
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("=== Testing Imports ===")
    
    # Test PyBluez
    try:
        import bluetooth
        print("✅ PyBluez imported successfully")
        
        # Test basic Bluetooth functionality
        try:
            local_addr = bluetooth.read_local_bdaddr()
            print(f"✅ Local Bluetooth address: {local_addr[0]}")
        except Exception as e:
            print(f"⚠️  Bluetooth hardware issue: {e}")
            
    except ImportError:
        print("❌ PyBluez not available")
        print("   Install with: pip install pybluez")
    
    # Test colorama
    try:
        from colorama import init, Fore, Style
        init()
        print(f"{Fore.GREEN}✅ Colorama imported successfully{Style.RESET_ALL}")
    except ImportError:
        print("⚠️  Colorama not available (colors will be limited)")
        print("   Install with: pip install colorama")
    
    # Test tqdm
    try:
        from tqdm import tqdm
        print("✅ tqdm imported successfully")
    except ImportError:
        print("⚠️  tqdm not available (basic progress bars will be used)")
        print("   Install with: pip install tqdm")
    
    print()

def test_config():
    """Test configuration management"""
    print("=== Testing Configuration ===")
    
    try:
        from config_manager import config
        
        # Test getting values
        bluetooth_port = config.get('bluetooth.port')
        print(f"✅ Bluetooth port: {bluetooth_port}")
        
        # Test downloads directory
        downloads_dir = config.get_downloads_dir()
        print(f"✅ Downloads directory: {downloads_dir}")
        
        # Test setting values
        config.set('test.value', 'hello')
        test_value = config.get('test.value')
        print(f"✅ Config set/get test: {test_value}")
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
    
    print()

def test_file_operations():
    """Test file transfer components"""
    print("=== Testing File Operations ===")
    
    try:
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello, this is a test file for Bluetooth chat!")
            test_file = f.name
        
        test_path = Path(test_file)
        file_size = test_path.stat().st_size
        
        print(f"✅ Created test file: {test_path.name} ({file_size} bytes)")
        
        # Test file reading
        with open(test_file, 'rb') as f:
            chunk = f.read(1024)
            print(f"✅ File read test: {len(chunk)} bytes")
        
        # Test base64 encoding (used in file transfer)
        import base64
        encoded = base64.b64encode(chunk)
        decoded = base64.b64decode(encoded)
        
        if chunk == decoded:
            print("✅ Base64 encoding/decoding test passed")
        else:
            print("❌ Base64 encoding/decoding test failed")
        
        # Cleanup
        os.unlink(test_file)
        print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
    
    print()

def test_network():
    """Test network connectivity (for TCP fallback)"""
    print("=== Testing Network (TCP Fallback) ===")
    
    try:
        import socket
        
        # Test socket creation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("✅ TCP socket created")
        
        # Test local binding
        sock.bind(('localhost', 0))  # Let OS choose port
        bound_port = sock.getsockname()[1]
        print(f"✅ Socket bound to localhost:{bound_port}")
        
        sock.close()
        print("✅ Socket closed successfully")
        
    except Exception as e:
        print(f"❌ Network test failed: {e}")
    
    print()

def demo_bluetooth_scan():
    """Demo Bluetooth device scanning"""
    print("=== Bluetooth Scan Demo ===")
    
    try:
        import bluetooth
        
        print("Scanning for Bluetooth devices (this may take ~10 seconds)...")
        devices = bluetooth.discover_devices(duration=5, lookup_names=True)
        
        if devices:
            print(f"Found {len(devices)} devices:")
            for addr, name in devices:
                print(f"  📱 {name} ({addr})")
        else:
            print("No devices found. Make sure:")
            print("  1. Bluetooth is enabled")
            print("  2. Other devices are discoverable")
            print("  3. You're within range (~10 meters)")
        
    except ImportError:
        print("❌ PyBluez not available for demo")
    except Exception as e:
        print(f"❌ Bluetooth scan failed: {e}")
        print("This might be due to permissions or hardware issues.")
    
    print()

def run_performance_test():
    """Run a simple performance test"""
    print("=== Performance Test ===")
    
    try:
        import json
        import base64
        
        # Test JSON encoding/decoding speed
        test_data = {
            'type': 'message',
            'username': 'testuser',
            'content': 'Hello World!' * 100,  # Larger message
            'timestamp': '2025-01-01T00:00:00'
        }
        
        start_time = time.time()
        for _ in range(1000):
            json_str = json.dumps(test_data)
            decoded = json.loads(json_str)
        json_time = time.time() - start_time
        
        print(f"✅ JSON encode/decode: {json_time:.3f}s for 1000 operations")
        
        # Test base64 encoding speed
        test_bytes = b'Hello World!' * 1000  # 12KB of data
        
        start_time = time.time()
        for _ in range(100):
            encoded = base64.b64encode(test_bytes)
            decoded = base64.b64decode(encoded)
        b64_time = time.time() - start_time
        
        print(f"✅ Base64 encode/decode: {b64_time:.3f}s for 100 operations (12KB each)")
        
        # Estimate file transfer speed
        chunk_size = 1024
        chunks_per_second = 100 / b64_time  # Based on our test
        estimated_speed_kbps = (chunks_per_second * chunk_size) / 1024
        
        print(f"📊 Estimated max file transfer speed: ~{estimated_speed_kbps:.1f} KB/s")
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
    
    print()

def check_permissions():
    """Check for necessary permissions"""
    print("=== Permission Check ===")
    
    # Check if we can create files in downloads directory
    try:
        from config_manager import config
        downloads_dir = config.get_downloads_dir()
        
        test_file = downloads_dir / "permission_test.txt"
        with open(test_file, 'w') as f:
            f.write("test")
        
        test_file.unlink()  # Delete test file
        print(f"✅ Write permissions OK: {downloads_dir}")
        
    except Exception as e:
        print(f"❌ Write permission test failed: {e}")
    
    # Check Bluetooth permissions (platform-specific hints)
    if sys.platform == "darwin":  # macOS
        print("ℹ️  macOS: Check System Preferences > Security & Privacy > Privacy > Bluetooth")
    elif sys.platform.startswith("linux"):  # Linux
        import os
        if os.geteuid() != 0:  # Not running as root
            print("ℹ️  Linux: You may need to run with sudo or add user to bluetooth group")
    elif sys.platform == "win32":  # Windows
        print("ℹ️  Windows: Ensure Bluetooth drivers are installed and services are running")
    
    print()

def main():
    """Run all tests"""
    print("🧪 Terminal Chat Bluetooth - Test Suite")
    print("=" * 50)
    
    test_imports()
    test_config()
    test_file_operations()
    test_network()
    check_permissions()
    run_performance_test()
    
    print("=" * 50)
    print("🔍 For Bluetooth device scanning, run:")
    print("   python3 test.py --scan")
    print()
    print("💡 If all tests pass, your system is ready!")
    print("   Run: python3 launcher.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        demo_bluetooth_scan()
    else:
        main()
