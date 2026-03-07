"""
Test reservation script - quick test for configuration
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from reserve_seat import load_config
import requests
import urllib3

def test_config():
    """Test if configuration is correct"""
    print("=" * 60)
    print("Library Reserve - Configuration Test")
    print("=" * 60)
    
    # Load configuration
    try:
        config = load_config()
        print("\n[1/4] Configuration loading... [OK]")
    except Exception as e:
        print(f"\n[1/4] Configuration loading... [ERROR] {e}")
        return False
    
    # Check authentication
    print("\n[2/4] Checking authentication...")
    auth = config.get('auth', {})
    cookie = auth.get('cookie', '')
    code = auth.get('code', '')
    
    if not cookie:
        print("  [ERROR] Cookie is empty")
        return False
    if not code:
        print("  [ERROR] Code is empty")
        return False
    
    print(f"  [OK] Cookie: {cookie[:50]}...")
    print(f"  [OK] Code: {code[:50]}...")
    
    # Check seats
    print("\n[3/4] Checking seat configuration...")
    seats = config.get('reserve', {}).get('seats', [])
    
    if not seats:
        print("  [ERROR] No seats configured")
        return False
    
    print(f"  [OK] Found {len(seats)} seats:")
    for i, seat in enumerate(seats, 1):
        status = "[ENABLED]" if seat.get('enabled', True) else "[DISABLED]"
        print(f"    {i}. {seat['id']} - {status}")
    
    # Check expiration
    print("\n[4/4] Checking configuration expiration...")
    from datetime import datetime
    last_update_str = auth.get('last_update', '')
    
    if last_update_str:
        try:
            last_update = datetime.fromisoformat(last_update_str)
            days_passed = (datetime.now() - last_update).days
            days_remaining = auth.get('expires_days', 10) - days_passed
            
            if days_remaining <= 0:
                print(f"  [ERROR] Configuration expired {abs(days_remaining)} days ago!")
            elif days_remaining <= 3:
                print(f"  [WARNING] Configuration will expire in {days_remaining} days!")
            else:
                print(f"  [OK] Configuration valid for {days_remaining} more days")
        except:
            print("  [WARNING] Unable to parse last update time")
    
    # Test connection (optional)
    print("\n[5/5] Testing API connection...")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        test_url = "https://libwx.hunnu.edu.cn/apim/seat/SeatDateHandler.ashx"
        response = requests.get(test_url, timeout=5, verify=False)
        print(f"  [OK] Server reachable (status: {response.status_code})")
    except requests.exceptions.Timeout:
        print("  [WARNING] Connection timeout (server may be slow)")
    except requests.exceptions.ConnectionError:
        print("  [WARNING] Cannot connect to server (check network)")
    except Exception as e:
        print(f"  [WARNING] Connection test failed: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Configuration test completed!")
    print("=" * 60)
    print("\nTo run the reservation script:")
    print("  python reserve_seat.py")
    print("\nOr manage configuration via web interface:")
    print("  http://localhost:5173")
    
    return True

if __name__ == "__main__":
    try:
        success = test_config()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
