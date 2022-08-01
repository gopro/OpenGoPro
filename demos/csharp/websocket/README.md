# GoProCSharpSample With WebsocketApi

Websocket Api to control multiple cam shutter

# Requirements

Visual Studio is required to run the solution. Visit https://visualstudio.microsoft.com/downloads/ to download.

The target .NET framework is v4.7.2

GoPro camera must be paired before any other operations will succeed. Put the camera in pairing mode before attempting pairing with the app.

# Usage

1. Open and run the demo in Visual Studio to show the GUI
2. `Scan` for GoPro devices
3. `Pair` to the discovered device that is not `GoPro Cam`. In the .gif below, this is `GoPro 0456` (Only needs to be done once, or if camera is factory reset)
4. After pairing is successful, `connect` to the same GoPro device
5. Now You Can Use Websocket to control cam shutter
```python
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
```

![Demo Steps](../../../docs/assets/images/demos/csharp_demo.gif)