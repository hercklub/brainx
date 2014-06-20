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
		
		with open(filepath, mode='rb') as f:
			self.binary = f.read()
		self.parse_png()

	def check_header(self):
		"""Check header and cut it off"""
		if self.binary[:8] != b"\x89PNG\r\n\x1a\n":
			raise PNGWrongHeaderError("Loaded file is probably not a PNG image.")
		self.binary=self.binary[8:]
		return self


	def parse_png(self):
		"""From raw binary data, get chunks and save them. Deletes raw data."""
		self.check_header()
		p = 0
		self.data = []
		while p < len(self.binary):
			#lenght
			l = self.bytes_to_num(self.binary[p:p+4])
			p += 4    
			self.data += [{'head':self.binary[p:p+4], 'data':self.binary[p+4:p+l+4]}]      
			p += l+8
		print (self.data)
		return self
	def bytes_to_num(self, bytes):
		try:
			r = bytes[0] << 24
			r += bytes[1] << 16
			r += bytes[2] << 8
			r += bytes[3]
		except:
			return 0;

		return r;


if __name__ == '__main__':
	PngReader(sys.argv[1])
