"""
Example of a script that has a single entry point that doesn't use any kind of
special Runner.

"""

import asyncio

from aerpawlib.runner import BasicRunner, entrypoint
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone


class MyScript(BasicRunner):
    @entrypoint
    async def do_stuff(self, drone: Drone):
        # take off to 30m
        await drone.takeoff(30)

        # Go north a bit
        await drone.goto_coordinates(drone.position + VectorNED(25, 0, 0))

        await asyncio.sleep(1)

        await drone.goto_coordinates(drone.position + VectorNED(5, 5, 0))

        await asyncio.sleep(1)

        await drone.goto_coordinates(drone.position + VectorNED(0, 10, 0))

        await asyncio.sleep(1)

        # Exit the geofence to the right.
        await drone.goto_coordinates(drone.position + VectorNED(0, 2000, 0))

        # The filter should stop us from continuing.

        # land
        await drone.land()
