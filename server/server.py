import asyncio
import websockets
import json
import pyautogui

PORT = 9000

async def handle_connection(websocket):
    print("📡 Client connected")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")

                if action == "move":
                    dx = data.get("dx", 0)
                    dy = data.get("dy", 0)
                    pyautogui.moveRel(dx, dy)

                elif action == "click":
                    button = data.get("type", "left")
                    pyautogui.click(button=button)

                elif action == "keypress":
                    key = data.get("key")
                    pyautogui.press(key)

                else:
                    print(f"⚠️ Unknown action: {action}")
            except Exception as e:
                print(f"❌ Error: {e}")
    except websockets.exceptions.ConnectionClosed:
        print("🔌 Client disconnected")

async def main():
    print(f"🚀 Server running on port {PORT}")
    async with websockets.serve(handle_connection, "0.0.0.0", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
