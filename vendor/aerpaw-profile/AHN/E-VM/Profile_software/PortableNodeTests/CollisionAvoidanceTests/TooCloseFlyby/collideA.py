import asyncio

from aerpawlib.runner import StateMachine, state
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone

FLIGHT_ALT = 40  # m


# Runs on Vehicle 1
class CollideA(StateMachine):
    @state(name="start", first=True)
    async def start(self, drone: Drone):
        print("taking off")
        await drone.takeoff(FLIGHT_ALT)
        await drone.set_groundspeed(20)
        self.home = drone.position
        print("taken off")
        return "start_position"

    @state(name="start_position")
    async def start_position(self, drone: Drone):
        print("Moving to start position")
        await drone.goto_coordinates(self.home + VectorNED(0, -9.2))
        await asyncio.sleep(34)  # Wait for the other drone
        return "collide"

    @state(name="collide")
    async def collide(self, drone: Drone):
        print("Colliding now!")
        await drone.set_velocity(VectorNED(0, -20))
        await asyncio.sleep(100)
        return "rtl"

    @state(name="rtl")
    async def rtl(self, drone: Drone):
        print("returning home")
        await drone.goto_coordinates(self.home)
        print("landing")
        await drone.land()
        print("done!")
