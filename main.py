from skyroom import *
from dotenv import load_dotenv
import os

load_dotenv()

# Load API key from .env file
api_key = os.getenv('SKYROOM_API_KEY')
if not api_key:
    raise ValueError('SKYROOM_API_KEY not set in .env file')

api = SkyroomAPI(api_key)

try:
    # Example: Get all rooms
    print("=== Getting Rooms ===")
    rooms = api.getRooms()
    print(f"Found {len(rooms)} rooms")

    # Example: Get services (new method)
    print("\n=== Getting Services ===")
    services = api.getServices()
    print(f"Found {len(services)} services")

    # Example: Get room by ID (new parameter hints)
    if rooms:
        room_id = rooms[0]['id']
        print(f"\n=== Getting Room {room_id} ===")
        room = api.getRoom(room_id=room_id)
        print(f"Room: {room['name']} - {room['title']}")

    # Example: Create login URL (new method with full params)
    # Note: This would create a real URL if room_id exists
    print("\n=== Create Login URL Example ===")
    print("Usage: api.createLoginUrl(room_id=123, user_id='user123', nickname='Test User', access=1)")
    print("This creates a direct login link for a room without requiring user creation")

    # Example: Delete multiple users (new method)
    print("\n=== Delete Users Example ===")
    print("Usage: api.deleteUsers(users=[user_id1, user_id2, user_id3])")
    print("Returns: {'success': count, 'failure': count}")

    # Example: Create room (new parameter hints)
    print("\n=== Create Room Example ===")
    print("Usage: api.createRoom(name='test-room', title='Test Room', max_users=10)")

    # Example: Update user (new parameter hints)
    print("\n=== Update User Example ===")
    print("Usage: api.updateUser(user_id=123, nickname='New Name', status=1)")

except APIException as e:
    print(f"API Error: {e}")
except HTTPException as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")