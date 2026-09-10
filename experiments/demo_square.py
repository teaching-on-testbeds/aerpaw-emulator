"""Run a small square mission on either the UAV or UGV demo node."""

import os

from aerpawlib.runner import BasicRunner, entrypoint
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone, Rover, Vehicle


class DemoSquare(BasicRunner):
    @entrypoint
    async def run_square(self, vehicle: Vehicle):
        size = float(os.environ.get("SQUARE_SIZE", "10"))
        if isinstance(vehicle, Drone):
            await vehicle.takeoff(float(os.environ.get("FLIGHT_ALT", "5")))
        elif not isinstance(vehicle, Rover):
            raise TypeError("demo_square supports Drone and Rover")

        for north, east in ((size, 0), (0, -size), (-size, 0), (0, size)):
            await vehicle.goto_coordinates(vehicle.position + VectorNED(north, east), tolerance=2.5)

        if isinstance(vehicle, Drone):
            await vehicle.land()
