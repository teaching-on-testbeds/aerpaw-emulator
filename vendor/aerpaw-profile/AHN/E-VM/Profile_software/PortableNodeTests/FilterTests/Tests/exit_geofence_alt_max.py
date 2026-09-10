"""
Example of a script that has a single entry point that doesn't use any kind of
special Runner.

"""

from aerpawlib.runner import BasicRunner, entrypoint
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone


class MyScript(BasicRunner):
    @entrypoint
    async def do_stuff(self, drone: Drone):
        # take off to 30m
        await drone.takeoff(30)

        # Go too high.
        await drone.goto_coordinates(drone.position + VectorNED(0, 0, -122))

        # The filter should stop us from continuing.

        # land
        await drone.land()
