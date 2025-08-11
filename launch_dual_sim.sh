#!/bin/bash
#
# The Definitive, Safety-Checked Dual-Drone Launch Script
# Based on the official PX4 documentation and our complete debugging history.
#

# ------------------- CONFIGURATION -------------------
# The absolute path to your PX4-Autopilot directory, which we have confirmed.
PX4_DIR="$HOME/PX4/PX4-Autopilot"


# ------------------- SCRIPT START -------------------
echo "DEFINITIVE LAUNCH SCRIPT INITIATED."
echo "This script will use the official PX4 tool: sitl_multiple_run.sh"
echo "------------------------------------------------"

# --- FIX for: Lingering old processes ---
echo "STEP 1: Terminating any previous simulations for a clean start..."
pkill -f 'px4|gazebo|gzserver|gzclient' >/dev/null 2>&1 || true
sleep 2
echo "Cleanup complete."


echo "------------------------------------------------"
# --- FIX for: Pathing issues ---
echo "STEP 2: Changing to the correct PX4 directory..."
cd "$PX4_DIR" || { echo "ERROR: PX4 directory not found at $PX4_DIR! Exiting."; exit 1; }


echo "------------------------------------------------"
# --- FIX for: All launch, positioning, and hijacking issues ---
echo "STEP 3: Launching 2 Iris drones using the official PX4 multi-vehicle script..."
# This single command is the documented and correct way to launch this simulation.
# It handles the Gazebo launch, model spawning, positioning, and running the
# PX4 instances on the correct ports automatically.
# -n 2: Spawns 2 vehicles.
# -m iris: Uses the 'iris' model for both.
Tools/simulation/gazebo-classic/sitl_multiple_run.sh -n 2 -m iris


echo "------------------------------------------------"
echo "Launch script finished. The simulation should be running."
echo "You may need to manually close this terminal (Ctrl+C) when you are done."