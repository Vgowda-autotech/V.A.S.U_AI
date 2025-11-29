#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def main():
    try:
        print("🚀 Launching V.A.S.U - Phase 3 Integration Test")
        # Import the NEW integrated GUI
        from phase2_vision_system.gui_part5_integrated import main as gui_main
        gui_main()
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())