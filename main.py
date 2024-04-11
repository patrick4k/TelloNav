import asyncio
from tello_asyncio import Tello
import simple_pid
import time

max_velocity = 50
z_target = 100

Kp = 2
Ki = 30
Kd = 2

z_pid = simple_pid.PID(
    Kp=Kp,
    Ki=Ki,
    Kd=Kd,
    output_limits=(-max_velocity, max_velocity),
    setpoint=z_target
)

class Timer:
    ti = None
    
    def start(self): self.ti = time.time_ns()
    def reset(self): self.ti = None
    def is_running(self): return self.ti is not None
    def elapse_s(self): return (time.time_ns() - self.ti)/1e9
    def has_been(self, sec) -> bool:
        if self.ti is None:
            print("Timer Error: Unset Timer cannot be checked")
        return self.elapse_s() >= sec
    

async def main():
    try:
        drone = Tello()
        await drone.connect()
        print(f"-- height = {drone.state.height}")
        await drone.takeoff()
        init_height = drone.state.height
        print(f"-- inital height = {init_height}")
        await asyncio.sleep(1)
             
        print(f"-- starting PID targeting height = {z_target}")
        success_timer = Timer()
        is_success = False
        runtime_timer = Timer()
        runtime_timer.start()
        f = open(f"./data/Kp{Kp}_Ki{Ki}_Kd{Kd}.csv", "w")
        f.write("elapse_s,height_cm,vel_setpoint_cm_s\n")
        while True:
            if runtime_timer.has_been(20): 
                print("-- Timeout")
                break
            
            height = drone.state.height
            
            if abs(z_target - height) < 10:
                if not success_timer.is_running(): success_timer.start()
                if success_timer.has_been(3):
                    print("I found the correct height!")
                    is_success = True
                    break
            else: success_timer.reset()

            output = int(z_pid(height))
            if abs(output) < 10:
                output = 0
            
            await drone.remote_control(0, 0, output, 0)
            
            elapse = runtime_timer.elapse_s()
            
            print(f"-- elapse = {elapse}")
            print(f"-- height = {height}")
            f.write(f"{elapse},{height},{output}\n")
            
            await asyncio.sleep(0.1)
        
        # if is_success: await drone.flip_back()
        if is_success: await drone.turn_counterclockwise(360)
        await drone.land()
    except Exception as e:
        print(e)
        await drone.emergency_stop()
    finally:
        await drone.disconnect()
        f.close()

asyncio.run(main())
 