import math
import websockets
import asyncio


# Server data
PORT = 7890
print("Server listening on Port " + str(PORT))
# A set of connected ws clients
connected = set()
# The main behavior function for this server
async def echo(websocket, path):
    print("A client just connected")
    # Store a copy of the connected client
    connected.add(websocket)
    # Handle incoming messages
    i = 0
    try:
        for conn in connected:
            while True:
                # print(i%100)
                i += 0.00001
                data = '{"raw_data": [{"SensorIndex":	0, ' \
                       f'"AccelX":	{math.sin(i * math.pi)}, ' \
                       f'"AccelY":	{math.cos(i * math.pi)}, ' \
                       f'"AccelZ":	{2 * math.cos(i * math.pi)}, ' \
                       f'"GyroX":	{math.floor(i)} ,' \
                       f'"GyroY":	{math.floor(i + 1)} ,' \
                       f'"GyroZ":	{math.floor(i + 2)}, ' \
                       f'"MagX":	1, ' \
                       f'"MagY":	1 ,' \
                       f'"MagZ":	1, ' \
                       f'"Quat1":	{math.cos(i * math.pi) + math.sin(i * math.pi)},' \
                       f'"Quat2":	{2 * math.cos(i * math.pi) + math.sin(i * math.pi)}, ' \
                       f'"Quat3":	{math.cos(i * math.pi) + 2 * math.sin(i * math.pi)},' \
                       f'"Quat4":	{2 * math.cos(i * math.pi) + 2 * math.sin(i * math.pi)} ,' \
                       f'"Sampletime":	{i}, ' \
                       '"Package": 1}]}'

                await conn.send(bytes(data, "utf-8"))
                await asyncio.sleep(0.01)

    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print(f"A client just disconnected {e}")
    finally:
        connected.remove(websocket)

# Start the server
start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
