import asyncio
import time

import websockets

"""
async def echo(websocket):
    async for message in websocket:
        print(f'echo... {message}')
        await websocket.send(message)


async def main():
    async with websockets.serve(echo, "localhost", 8765) as server:
        server.send('alex')
        await asyncio.Future()  # run forever


asyncio.run(main())
"""

import asyncio
import websockets


async def recognise_faces(websocket, path):
    while True:
        """
        TODO CV2 + FACE RECOGNATION
        """
        message = "Hello from server!"
        await websocket.send(message)
        await asyncio.sleep(1)


server = websockets.serve(recognise_faces, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
