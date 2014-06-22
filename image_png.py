#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import zlib
import struct
import argparse


class PNGWrongHeaderError(Exception):
	"""Exceptions informing that loaded file is probably not PNG image."""
	pass


class PNGNotImplementedError(Exception):
	"""Exception informing that PNG image has structure which is not supported."""
	pass


class PngReader():
	"""Process PNG images."""
	    
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
		"""Convert 4 bytes to intiger value."""
		try:
			r = bytes[0] << 24
			r += bytes[1] << 16
			r += bytes[2] << 8
			r += bytes[3]
		except:
			return 0;

		return r;

	def decode(self):
		"""Save pixels according to used filetrs."""
		self.parse_png()
		i=0
		for row in range(0,self.heigh):
			png_filter=self.idat[i]
			i+=1
			line=[]
			a=(0,0,0)
			b=(0,0,0)
			c=(0,0,0)
			for col in range(0,self.width):
				pixel=(self.idat[i],self.idat[i+1],self.idat[i+2])
				i+=3

				if png_filter==0:
					line+=[pixel]

				elif png_filter==1:
					if col!=0:
						a=((pixel[0] + a[0] + 256)%256, (pixel[1] + a[1] + 256)%256, (pixel[2] + a[2] + 256)%256)
					else:
						a=pixel

					line+=[a]
				elif png_filter==2:
					if row!=0:
						b=self.rgb[row - 1][col]
						a=((pixel[0] + b[0] + 256)%256, (pixel[1] + b[1] + 256)%256, (pixel[2] + b[2] + 256)%256)
					else:
						a=pixel
					
					line+=[a]
				elif png_filter==3:
					if row != 0:
						b = self.rgb[row - 1][col]
					if col != 0:
						a = line[col - 1]
					
					pixel = ((pixel[0] + (a[0] + b[0]) // 2 + 256) % 256, (pixel[1] + (a[1] + b[1]) // 2 + 256) % 256,
                             (pixel[2] + (a[2] + b[2]) // 2 + 256) % 256)

					line += [pixel]


				elif png_filter==4:
					if row!=0 and col!=0:
						c=self.rgb[row-1][col-1]

					if row!=0:
						b=self.rgb[row-1][col]

					if col!=0:
						a=line[col-1]

					R = (pixel[0] + self.paeth(a[0], b[0], c[0]) + 256) % 256
					G = (pixel[1] + self.paeth(a[1], b[1], c[1]) + 256) % 256
					B = (pixel[2] + self.paeth(a[2], b[2], c[2]) + 256) % 256
					pixel = (R, G, B)
					line+=[pixel]
				else:
					raise PNGNotImplementedError("Loaded image uses filter which is not supported")
			self.rgb+=[line]
	def paeth(self,a, b, c):
		"""Paeth predictor, part of 4th filter."""
		p = a + b - c
		pa = abs(p - a)
		pb = abs(p - b)
		pc = abs(p - c)
		if pa <= pb and pa <= pc:
			return a
		elif pb <= pc:
			return b
		else:
			return c
if __name__ == '__main__':
	PngReader(sys.argv[1])
