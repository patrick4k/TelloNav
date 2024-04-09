import asyncio
from tello_asyncio import *

async def main():
    drone = Tello()
    try:
        await drone.connect()
        print(f"-- height = {drone.state.height}")
        await drone.takeoff()
        print(f"-- height = {drone.state.height}")
        await asyncio.sleep(5)
        await drone.remote_control(0, 0, 50, 0)
        await asyncio.sleep(5)
        await drone.remote_control(0, 0, 0, 0)
        print(f"-- height = {drone.state.height}")
        await drone.land()
        print(f"-- height = {drone.state.height}")
    finally:
        await drone.disconnect()

asyncio.run(main())
