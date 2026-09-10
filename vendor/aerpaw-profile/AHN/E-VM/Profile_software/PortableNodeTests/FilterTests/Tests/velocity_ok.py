"""
Example of a script that has a single entry point that doesn't use any kind of
special Runner.

"""

import asyncio

from aerpawlib.aerpaw import AERPAW_Platform
from aerpawlib.runner import BasicRunner, entrypoint
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone


class MyScript(BasicRunner):
    @entrypoint
    async def do_stuff(self, drone: Drone):
        # take off to 30m
        await drone.takeoff(30)

        start_coord = drone.position

        # Set a northwards velocity
        await drone.set_velocity(VectorNED(5, 0, 0), duration=10)

        await asyncio.sleep(10)

        # After ten seconds, do some maneuvers

        await drone.set_velocity(VectorNED(0, 0, 0), duration=1)
        await asyncio.sleep(1)

        SPEED = 3
        TIME = 5

        for x in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            north, east = x
            AERPAW_Platform.log_to_oeo(f"Going {north, east} at {SPEED}")

            await drone.set_velocity(VectorNED(north * SPEED, east * SPEED, 0), duration=TIME)
            await asyncio.sleep(TIME)

            await drone.set_velocity(VectorNED(0, 0, 0), duration=1)
            await asyncio.sleep(1)

        await drone.goto_coordinates(start_coord)

        # We should successfully land
        await drone.land()
