from typing import Any
import threading
import cv2

class CustomThread (threading.Thread):
	def __init__(self, args: dict[str, Any], start_fn, *start_args):
		threading.Thread.__init__(self)
		self.args = args
		self.start_fn = start_fn
		self.start_args = start_args

	def run(self):
		self.start_fn(*self.start_args, self.args)
