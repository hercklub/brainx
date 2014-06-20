#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

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
        

        #self.input=self.find_input()
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
                self.memory[self.memory_pointer]+=1

                if self.memory[self.memory_pointer] > 255:
                    self.memory[self.memory_pointer]=0

            if command=="-":
                self.memory[self.memory_pointer]-=1
                if self.memory[self.memory_pointer]<0:
                    self.memory[self.memory_pointer]=255

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
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


if __name__ == '__main__':
     BrainFuck(sys.argv[1])
