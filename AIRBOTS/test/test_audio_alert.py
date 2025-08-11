import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from payload.audio_alert import AlertSystem

class TestAlertSystemSimulation(unittest.TestCase):
    def setUp(self):
        os.environ["AIRBOTS_SIM"] = "1"

    def test_play_alert_sim(self):
        alert_system = AlertSystem()
        alert_system.play_alert(duration=2)
        # As above, you could use a StringIO to capture print output and assert on it

if __name__ == '__main__':
    unittest.main()
