#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

class PNGWrongHeaderError(Exception):
	"""Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
	pass


class PNGNotImplementedError(Exception):
	"""Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
	pass


class PngReader():
	"""Třída pro práci s PNG-obrázky."""
	    
	def __init__(self, filepath):
        
		# RGB-data obrázku jako seznam seznamů řádek,
		#   v každé řádce co pixel, to trojce (R, G, B)
		self.rgb = []
		with open(filepath, mode='rb') as raw:
			self.binary = raw.read()
		self.check_header()
	def check_header(self):
		"""Check header and cut it off"""
		if self.binary[:8] != b"\x89PNG\r\n\x1a\n":
			raise PNGWrongHeaderError("Loaded file is probably not a PNG image.")
		self.binary = self.binary[8:]

		return self;

if __name__ == '__main__':
	PngReader(sys.argv[1])
