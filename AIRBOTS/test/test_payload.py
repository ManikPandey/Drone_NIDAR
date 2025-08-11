import os
import sys
import unittest

# Ensure that the parent directory is in sys.path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from payload.servo_controller import PayloadSystem

class TestPayloadSystemSimulation(unittest.TestCase):
    def setUp(self):
        os.environ["AIRBOTS_SIM"] = "1"

    def test_release_package_sim(self):
        payload_system = PayloadSystem()
        # This should just print simulation logs
        payload_system.release_package()
        # If needed, capture stdout to assert log output

if __name__ == '__main__':
    unittest.main()
