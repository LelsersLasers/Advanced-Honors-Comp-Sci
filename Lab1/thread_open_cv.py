"""
    Description: CUstom Thread to allow the OpenCV and Pygame windows to run at the same time
    Author: Millan and Jerry
    Date: 9/27/2023
"""

from typing import Any
import threading

class CustomThread (threading.Thread):
	def __init__(self, args: dict[str, Any], start_fn, *start_args):
		threading.Thread.__init__(self)
		self.args = args
		self.start_fn = start_fn
		self.start_args = start_args

	def run(self):
		self.start_fn(*self.start_args, self.args)
