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

        # Set a northwards velocity
        await drone.set_velocity(VectorNED(5, 0, 0))

        # Wait for up to five minutes
        await asyncio.sleep(5 * 60)

        # Somewhere here the mavlink filter should stop us from exiting the geofence.

        # land
        await drone.land()
