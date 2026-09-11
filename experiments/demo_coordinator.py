"""Coordinator half of the UAV/UGV coordinated-square demo.

Waits for both vehicles to report ready, dispatches each through its square,
and finishes when both report done. Run with VEHICLE_TYPE=none and
ZMQ_IDENTIFIER=coordinator.
"""

from aerpawlib.runner import ZmqStateMachine, state

UAV = "uav"
UGV = "ugv"


class SquareCoordinator(ZmqStateMachine):
    _uav_ready = False
    _ugv_ready = False
    _uav_done = False
    _ugv_done = False

    @state(name="await_ready", first=True)
    async def state_await_ready(self, _):
        if not (self._uav_ready and self._ugv_ready):
            return "await_ready"
        return "dispatch"

    @state(name="callback_uav_ready")
    async def callback_uav_ready(self, _):
        self._uav_ready = True
        return "await_ready"

    @state(name="callback_ugv_ready")
    async def callback_ugv_ready(self, _):
        self._ugv_ready = True
        return "await_ready"

    @state(name="dispatch")
    async def state_dispatch(self, _):
        print("coordinator: starting coordinated squares")
        await self.transition_runner(UAV, "fly_square")
        await self.transition_runner(UGV, "drive_square")
        return "await_done"

    @state(name="await_done")
    async def state_await_done(self, _):
        if not (self._uav_done and self._ugv_done):
            return "await_done"
        print("coordinator: coordinated squares complete")

    @state(name="callback_uav_done")
    async def callback_uav_done(self, _):
        self._uav_done = True
        return "await_done"

    @state(name="callback_ugv_done")
    async def callback_ugv_done(self, _):
        self._ugv_done = True
        return "await_done"
