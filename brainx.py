#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import math
from image_png import PngReader

class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""
        
        # inicializace proměnných
        self.memory = bytearray(memory)
        self.memory_pointer = memory_pointer

        try:
            with open(data, mode='r') as f:
                self.code = f.read()
        except:
            self.code = data
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''
        if self.code.count('[')!=self.code.count(']'):
            print ("Bad fromat")
            sys.exit(1)
        

        self.input=self.find_input()
        self.interpreter(self.code)
        

    def interpreter(self,code):
        """ Interprets brainfuck code"""
        code_ptr=0
        while code_ptr<len(code):
            command=code[code_ptr]
                
            if command==">":
                self.memory_pointer += 1

                if self.memory_pointer==len(self.memory):
                    self.memory+=bytearray([0])

            if command=="<":
                self.memory_pointer -= 1

                if self.memory_pointer<0:
                    self.memory_pointer=0

            if command=="+":
                self.memory[self.memory_pointer ] = (self.memory[self.memory_pointer ] + 1) % 256;

            if command=="-":
                if self.memory[self.memory_pointer]==0:
                    self.memory[self.memory_pointer]=255
                else:
                    self.memory[self.memory_pointer]-=1

            if command == ".":
                sys.stdout.write(chr(self.memory[self.memory_pointer]))
                towrite=chr(self.memory[self.memory_pointer])
                self.output+=towrite

            if command==",":
                self.memory[self.memory_pointer]=ord(self.read_char())

            if command=="[":
                loopcode = self.get_loopcode(code[code_ptr:])
                while self.memory[self.memory_pointer] != 0:
                    self.interpreter(loopcode)
                code_ptr += len(loopcode) + 1
            
            code_ptr += 1               

    def get_loopcode(self,code):
        
        end = 1
        while (code[0:end].count('[') != code[0:end].count(']')):
            end += 1
        
       
        return code[1:end-1]
    def find_input(self):
        if self.code.find('!')!=-1:
            pos=self.code.find('!')
            _input=self.code[pos+1:]
            self.code=self.code[:pos]

            return _input
        return 0

    def read_char(self):
        if self.input!=0:
            ret=self.input[0]
            self.input=self.input[1:]
            return ret
        else:
            return sys.stdin.read(1)
        
    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""
    
    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""
        self.img=PngReader(filename).rgb
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = self.decode(self.img)
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)

    
    def decode(self,data):
        x=0
        y=0
        self.direction=2
        code=''
        while True:

            if x<0 or y<0 or x>=len(data) or y >=len (data[0]):
                break
            op=self.operations(data[x][y])
            if op[0]:
                code+=op[0]
            self.direction=op[1]
            x,y=self.move(x,y,self.direction)



        return code


    def operations (self,color):
        command=''
        direction=self.direction
        if color == (255,0,0):
            command = '>'
        if color == (128,0,0):
            command = '<'
        if color == (0,255,0):
            command = '+'
        if color == (0,128,0):
            command = '-'
        if color == (0,0,255):
            command = '.'
        if color == (0,0,128):
            command = ','
        if color == (255,255,0):
            command = '['
        if color == (128,128,0):
            command = ']'
        if color == (0,255,255): # turn right
            direction=(direction+1)%4
        if color == (0,128,128): # turn left
            direction=(direction-1)%4

        return command,direction
    def move (self,x,y,d):
        if d==0:
            y-=1
        if d==1:
            x-=1
        if d==2:
            y+=1
        if d==3:
            x+=1
        return x,y

class BrainCopter(BrainLoller):
    """Třída pro zpracování jazyka braincopter."""
    
    def operations(self,color):
        command = ''
        direction=self.direction
        color_c = (-2*color[0] + 3*color[1] + color[2])%11
        bf = '><+-.,[]'
        if color_c < 8:
            command = bf[color_c]
        if color_c == 8: # turn right
            direction=(direction+1)%4
        if color_c == 9: # turn left
            direction=(direction-1)%4
        return command,direction



if __name__ == '__main__':
     #BrainFuck(sys.argv[1])
     BrainCopter(sys.argv[1])
