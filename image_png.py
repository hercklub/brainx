#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import zlib

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
		self.decode()

	def check_header(self):
		"""Check header and cut it off"""
		if self.binary[:8] != b"\x89PNG\r\n\x1a\n":
			raise PNGWrongHeaderError("Loaded file is probably not a PNG image.")
		self.binary=self.binary[8:]
		return self


	def parse_png(self):
		"""From raw binary data, get chunks and save them.."""
		self.check_header()
		p = 0
		self.data = []
		while p < len(self.binary):
			#lenght
			l = self.bytes_to_num(self.binary[p:p+4])
			p += 4    
			self.data += [{'head':self.binary[p:p+4], 'data':self.binary[p+4:p+l+4]}]      
			p += l+8
		
		#Finds IHDR
		for chunk in self.data:
			if (chunk['head']==b'IHDR'):
				self.ihdr=chunk['data']
				break
		
		#Check IHDR
		if self.ihdr[8:13] != b'\x08\x02\x00\x00\x00':
			raise PNGNotImplementedError("Loaded image has a structure that cannot be processed.")
		
		#Get size
		self.width=self.bytes_to_num(self.ihdr[0:4])
		self.heigh=self.bytes_to_num(self.ihdr[4:8])

		#Finds all IDATs
		self.idat=b''
		for chunk in self.data:
			if (chunk['head']==b'IDAT'):
				self.idat+=chunk['data']
		#Decompress them
		self.idat=zlib.decompress(self.idat)

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

	def decode(self):
		self.parse_png()
		i=0
		for row in range(0,self.heigh):
			png_filter=self.idat[i]
			i+=1
			line=[]
			for columm in range(0,self.width):
				pixel=(self.idat[i],self.idat[i+1],self.idat[i+2])
				i+=3
				if png_filter==0:
					a=pixel
					line+=[pixel]
				else:
					raise PNGNotImplementedError("Loaded image uses filter which is not supported")
			self.rgb+=line
if __name__ == '__main__':
	PngReader(sys.argv[1])
