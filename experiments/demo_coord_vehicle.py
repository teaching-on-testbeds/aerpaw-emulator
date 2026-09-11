"""Vehicle half of the UAV/UGV coordinated-square demo.

One module serves both vehicles: the runner announces readiness until the
coordinator dispatches it, then flies or drives a small square and reports
completion. Run with ZMQ_IDENTIFIER=uav or ZMQ_IDENTIFIER=ugv.
"""

from aerpawlib.runner import ZmqStateMachine, sleep, state
from aerpawlib.util import VectorNED
from aerpawlib.vehicle import Drone, Rover

COORDINATOR = "coordinator"
SQUARE_SIZE = 10.0
FLIGHT_ALT = 5.0


def _role(vehicle) -> str:
    if isinstance(vehicle, Drone):
        return "uav"
    if isinstance(vehicle, Rover):
        return "ugv"
    raise TypeError("this demo supports only Drone and Rover vehicles")


class CoordinatedSquare(ZmqStateMachine):
    @state(name="report_ready", first=True)
    async def state_report_ready(self, vehicle):
        await self.transition_runner(COORDINATOR, f"callback_{_role(vehicle)}_ready")
        return "announce_ready"

    @state(name="announce_ready")
    async def state_announce_ready(self, vehicle):
        # keep announcing until the coordinator answers, so process start
        # order does not matter (ZeroMQ pub/sub has no replay)
        await self.transition_runner(COORDINATOR, f"callback_{_role(vehicle)}_ready")
        await sleep(0.5)
        return "announce_ready"

    @state(name="fly_square")
    async def state_fly_square(self, vehicle: Drone):
        print("uav: taking off")
        await vehicle.takeoff(FLIGHT_ALT)
        for north, east in ((SQUARE_SIZE, 0), (0, -SQUARE_SIZE), (-SQUARE_SIZE, 0), (0, SQUARE_SIZE)):
            await vehicle.goto_coordinates(vehicle.position + VectorNED(north, east), tolerance=2.5)
        print("uav: square complete")
        await self.transition_runner(COORDINATOR, "callback_uav_done")
        return "land"

    @state(name="land")
    async def state_land(self, vehicle: Drone):
        await vehicle.land()

    @state(name="drive_square")
    async def state_drive_square(self, vehicle: Rover):
        print("ugv: driving")
        for north, east in ((SQUARE_SIZE, 0), (0, -SQUARE_SIZE), (-SQUARE_SIZE, 0), (0, SQUARE_SIZE)):
            await vehicle.goto_coordinates(vehicle.position + VectorNED(north, east), tolerance=2.5)
        print("ugv: square complete")
        await self.transition_runner(COORDINATOR, "callback_ugv_done")
