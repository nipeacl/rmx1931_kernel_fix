#!/usr/bin/env python3
"""Pass-through gcc wrapper - just calls the real compiler without any -Werror conversion"""
import sys, subprocess
sys.exit(subprocess.call(sys.argv[1:]))
