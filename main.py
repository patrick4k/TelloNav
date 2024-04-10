import asyncio
from tello_asyncio import *
import simple_pid
import math

max_velocity = 100
z_target = 100

z_pid = simple_pid.PID(
    Kp=1,
    Ki=0.1,
    Kd=0.05,
    output_limits=(-max_velocity, max_velocity),
    setpoint=z_target
)

async def main():
    drone = Tello()
    try:
        await drone.connect()
        print(f"-- height = {drone.state.height}")
        await drone.takeoff()
        print(f"-- height = {drone.state.height}")
        await asyncio.sleep(1)

        print(f"-- starting PID targeting height = {z_target}")
        while True:
            height = drone.state.height
            print(f"-- height = {height}")
            if abs(height - z_target) < 10:
                print("-- hit target height")
                break

            output = z_pid(height)
            if abs(output) < 10:
                output = 0
            await drone.remote_control(0, 0, output, 0)
            await asyncio.sleep(0.5)

        await drone.turn_clockwise(360)
        await drone.land()
        print(f"-- height = {drone.state.height}")

    except Exception as e:
        print(e)
        await drone.emergency_stop()
    finally:
        await drone.disconnect()

asyncio.run(main())
