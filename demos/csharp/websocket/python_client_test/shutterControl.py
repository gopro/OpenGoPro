import asyncio
import websockets

async def shutterController(uri, toggle=1):
    """
    toggle 1=On
    toggle 0=Off
    """
    async with websockets.connect(uri) as websocket:
        await websocket.send(str(toggle))
        print(f"(client) send to server")
        name = await websocket.recv()
        print(f"(client) recv from server {name}")

asyncio.get_event_loop().run_until_complete(
    shutterController('ws://localhost:5678',1))

# asyncio.get_event_loop().run_until_complete(
#     shutterController('ws://localhost:5678',0))