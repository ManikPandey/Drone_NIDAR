from mavsdk import System
import asyncio

class PX4Interface:
    def __init__(self, connection_string="udp://:14540"):
        """
        MODIFIED: Accepts a connection_string to connect to a specific drone.
        """
        self.drone = System()
        self.system_address = connection_string

    async def __aenter__(self):
        """
        KEPT FROM YOURS: Connects and includes the robust 'wait for version' check.
        """
        print(f"[PX4 CONNECT] Connecting to {self.system_address}...")
        await self.drone.connect(system_address=self.system_address)

        print("[PX4 CONNECT] Waiting for connection to be established...")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print(f"[PX4 CONNECT] Drone discovered on {self.system_address}!")
                break
        
        # This robust version check is from your original file and is very important.
        print("[PX4 CONNECT] Waiting for system version information...")
        version_received = False
        for _ in range(10):  # Try up to 10 times (10 seconds)
            try:
                info = await self.drone.info.get_version()
                print(f"[PX4 CONNECT] PX4 Version: {info.flight_sw_major}.{info.flight_sw_minor}.{info.flight_sw_patch}")
                version_received = True
                break
            except Exception:
                await asyncio.sleep(1)
        
        if not version_received:
            print("[PX4 CONNECT] WARNING: Version information not received. Continuing anyway.")
        
        return self.drone

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Standard context manager exit."""
        print(f"[PX4 DISCONNECT] Connection context for {self.system_address} exited.")

    async def set_flight_mode(self, mode: str):
        """
        KEPT FROM YOURS: A useful helper function for changing flight modes.
        """
        if mode.lower() == 'hold':
            await self.drone.action.hold()
        elif mode.lower() == 'rtl':
            await self.drone.action.return_to_launch()
        elif mode.lower() == 'takeoff':
            await self.drone.action.set_takeoff_altitude(15)
            await self.drone.action.takeoff()
        else:
            print(f"[PX4 MODE] Unknown mode: {mode}")