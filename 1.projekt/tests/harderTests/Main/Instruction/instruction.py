# TODO: you has to do this....
from Frame.frame import Frame
from Frame.frames import Frames
from Err.err import *
import re
import sys


options = {    0: 'MOVE',
               1: 'CREATEFRAME',
               2: 'PUSHFRAME',
               3: 'POPFRAME',
               4: 'DEFVAR',
               5: 'CALL',
               6: 'RETURN',
               7: 'PUSHS',
               8: 'POPS',
               9: 'ADD',
               10: 'SUB',
               11: 'MUL',
               12: 'IDIV',
               13: 'LT',
               14: 'GT',
               15: 'EQ',
               16: 'AND',
               17: 'OR',
               18: 'NOT',
               19: 'INT2CHAR',
               20: 'STRI2INT',
               21: 'READ',
               22: 'WRITE',
               23: 'CONCAT',
               24: 'STRLEN',
               25: 'GETCHAR',
               26: 'SETCHAR',
               27: 'TYPE',
               28: 'LABEL',
               29: 'JUMP',
               30: 'JUMPIFEQ',
               31: 'JUMPIFNEQ',
               32: 'DPRINT',
               33: 'BREAK',
               }

class Instruction:
    orderOfInstruction = 0
    nameOfInstruction = None
    arguments = []

    '''
    :brief  function which inicializates values...
    :param  self
    :param  pArguments
    :param  pNameOfInstrution
    :param  pOrderOfInstruction 
    '''
    def inicialization(self, pArguments , pNameOfInstruction , pOrderOfInstruction):
        self.arguments = pArguments
        self.nameOfInstruction = pNameOfInstruction
        self.orderOfInstruction = pOrderOfInstruction

    def choiceOperator(self, myFrame , operator):
        if (operator == '+'):
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'int':
                retMessageAndValue('Failed parameters of instruction -> ' + self.nameOfInstruction, 52)
            if self.arguments[1].type == 'var':
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
                if myFrame.getVariableType(self.arguments[1].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction, 53)
            else:
                firstValue = self.arguments[1].text

            if self.arguments[2].type == 'var':
                secondValue = myFrame.getVarValue(self.arguments[2].text)
                if myFrame.getVariableType(self.arguments[2].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction , 53)
            else:
                secondValue = self.arguments[2].text


            finalValue = firstValue + secondValue

        elif (operator == '-'):
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'int':
                retMessageAndValue('Failed parameters of instruction -> ' + self.nameOfInstruction, 52)
            if self.arguments[1].type == 'var':
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
                if myFrame.getVariableType(self.arguments[1].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction, 53)
            else:
                firstValue = self.arguments[1].text

            if self.arguments[2].type == 'var':
                secondValue = myFrame.getVarValue(self.arguments[2].text)
                if myFrame.getVariableType(self.arguments[2].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction , 53)
            else:
                secondValue = self.arguments[2].text

            finalValue = firstValue - secondValue

        elif (operator == '*'):
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'int':
                retMessageAndValue('Failed parameters of instruction -> ' + self.nameOfInstruction, 52)
            if self.arguments[1].type == 'var':
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
                if myFrame.getVariableType(self.arguments[1].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction, 53)
            else:
                firstValue = self.arguments[1].text

            if self.arguments[2].type == 'var':
                secondValue = myFrame.getVarValue(self.arguments[2].text)
                if myFrame.getVariableType(self.arguments[2].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction , 53)
            else:
                secondValue = self.arguments[2].text

            finalValue = firstValue * secondValue

        elif (operator == '/'):
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'int':
                retMessageAndValue('Failed parameters of instruction -> ' + self.nameOfInstruction, 52)
            if self.arguments[1].type == 'var':
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
                if myFrame.getVariableType(self.arguments[1].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction, 53)
            else:
                firstValue = self.arguments[1].text

            if self.arguments[2].type == 'var':
                secondValue = myFrame.getVarValue(self.arguments[2].text)
                if myFrame.getVariableType(self.arguments[2].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction , 53)
            else:
                secondValue = self.arguments[2].text
                if secondValue == 0:
                    retMessageAndValue('Dividing by zero value..', 57)

            finalValue = firstValue // secondValue

        return finalValue



    '''
    :brief  function which parse whole instructions
    :param  self
    :param  frames 
    '''
    def parseInstructions(self,myFrame):
        if self.nameOfInstruction == options.get(0):        # MOVE
            self.instMove(myFrame)
        elif self.nameOfInstruction == options.get(1):      # CREATEFRAME
            self.instCreateframe(myFrame)
        elif self.nameOfInstruction == options.get(2):      # PUSHFRAME
            self.instPushframe(myFrame)
        elif self.nameOfInstruction == options.get(3):      # POPFRAME
            self.instPopframe()
        elif self.nameOfInstruction == options.get(4):      # DEFVAR
            self.instDefVar(myFrame)
        elif self.nameOfInstruction == options.get(5):      # CALL
            self.instCall()
        elif self.nameOfInstruction == options.get(6):      # RETURN
            self.instReturn()
        elif self.nameOfInstruction == options.get(7):      # PUSHS
            self.instPushs()
        elif self.nameOfInstruction == options.get(8):      # POPS
            self.instPops()
        elif self.nameOfInstruction == options.get(9):      # ADD
            self.instAdd(myFrame)
        elif self.nameOfInstruction == options.get(10):     # SUB
            self.instSub(myFrame)
        elif self.nameOfInstruction == options.get(11):     # MUL
            self.instMul(myFrame)
        elif self.nameOfInstruction == options.get(12):     # IDIV
            self.instIdiv(myFrame)
        elif self.nameOfInstruction == options.get(13):     # LT
            self.instLt(myFrame)
        elif self.nameOfInstruction == options.get(14):     # GT
            self.instGt(myFrame)
        elif self.nameOfInstruction == options.get(15):     # EQ
            self.instEq(myFrame)
        elif self.nameOfInstruction == options.get(16):     # AND
            self.instAnd()
        elif self.nameOfInstruction == options.get(17):     # OR
            self.instOr()
        elif self.nameOfInstruction == options.get(18):     # NOT
            self.instNot()
        elif self.nameOfInstruction == options.get(19):     # INT2CHAR
            self.instInt2Char()
        elif self.nameOfInstruction == options.get(20):     # STRI2INT
            self.instStri2Int()
        elif self.nameOfInstruction == options.get(21):     # READ
            self.instRead(myFrame)
        elif self.nameOfInstruction == options.get(22):     # WRITE
            self.instWrite()
        elif self.nameOfInstruction == options.get(23):     # CONCAT
            self.instConcat()
        elif self.nameOfInstruction == options.get(24):     # STRLEN
            self.instStrlen()
        elif self.nameOfInstruction == options.get(25):     # GETCHAR
            self.instGetchar()
        elif self.nameOfInstruction == options.get(26):     # SETCHAR
            self.instSetchar()
        elif self.nameOfInstruction == options.get(27):     # TYPE
            self.instType()
        elif self.nameOfInstruction == options.get(28):     # LABEL
            self.instLabel()
        elif self.nameOfInstruction == options.get(29):     # JUMP
            self.instJump()
        elif self.nameOfInstruction == options.get(30):     # JUMPIFEQ
            self.instJumpifeq()
        elif self.nameOfInstruction == options.get(31):     # JUMPIFNEQ
            self.instJumpifneq()
        elif self.nameOfInstruction == options.get(32):     # DPRINT
            self.instDprint()
        elif self.nameOfInstruction == options.get(33):     # BREAK
            self.instBreak()
        else:
            retMessageAndValue("Error: Unknow Instruction", 32)


    '''
    :brief  MOVE INSTRUCTION
    :param  self
    :param  myFrame
    '''
    def instMove(self, myFrame):
        print("Som vo funckii MOVE")
        # print("Toto je prvy argument -->", self.arguments[0].type)
        # print("Toto je druhy argument -->", self.arguments[1].type)
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'var' and self.arguments[1].type != 'int' and self.arguments[1].type != 'bool' and self.arguments[1].type != 'string'):
            retMessageAndValue('Wrong type of parameter - function:' + self.nameOfInstruction, 52)
        if self.arguments[1].type == 'var':
            variableValue = myFrame.getVariableValue(self.arguments[1].text)
            if variableValue is None:
                retMessageAndValue('Variable does not have defined value', 56)
            myFrame.setVariableValue(self.arguments[0].text, variableValue)
        else:
            print("Toto je prvy argumente ---> ", self.arguments[0].text)
            print("Toto je druhy argumente ---> ", self.arguments[1].text)
            myFrame.setVariableValue(self.arguments[0].text, self.arguments[1].text)

    '''
    :brief CREATEFRAME INSTRUCTION
    '''
    def instCreateframe(self, myFrame):
        print("SOM V CREATEFRAME")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        else:
            myFrames = Frames()
            myFrames.createFrame()
            # myFrame.tempFrame = Frame()  # creating tempororary frame
            print("Frame was created....")

    '''
    :brief PUSHFRAME INSTRUCTION
    '''
    def instPushframe(self, myFrame):
        print("SOM V PUSHFRAME")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        myFrame.pushFrame(myFrame.tempFrame)
        print("Frame was pushed")

    '''
    :brief POPFRAME INSTRUCTION
    '''
    def instPopframe(self):
        print("SOM V POPFRAME")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief DEFVAR INSTRUCTION
    '''
    def instDefVar(self, myFrame):
        print("SOM V DEFVAR")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var':
            retMessageAndValue('Wrong type of parameter - function:' + self.nameOfInstruction, 52)
        myFrame.addVariableToTheFrame(self.arguments[0].text)
        print("Toto je v DEFVAR ----> ", self.arguments[0].text)

    '''
    :brief CALL INSTRUCTION
    '''
    def instCall(self):
        print("SOM V CALL")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief RETURN INSTRUCTION
    '''
    def instReturn(self):
        print("SOM V RETURN")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief PUSHS INSTRUCTION
    '''
    def instPushs(self):
        print("SOM V PUSHS")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief POPS INSTRUCTION
    '''
    def instPops(self):
        print("SOM V POPS")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief ADD INSTRUCTION
    '''
    def instAdd(self, myFrame):
        print("SOM V ADD")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

        operator = '+'
        finalValue = self.choiceOperator(myFrame, operator)
        print('Final value is --->', finalValue)

        myFrame.setVariableValue(self.arguments[0].text, finalValue)
        print("Toto je vysledna hodnota po ADD inst ---> ", finalValue)

    '''
    :brief SUB INSTRUCTION
    '''
    def instSub(self, myFrame):
        print("SOM V SUB")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '-'
        finalValue = self.choiceOperator(myFrame, operator)
        print('Final value is --->', finalValue)

        myFrame.setVariableValue(self.arguments[0].text, finalValue)
        print("Toto je vysledna hodnota po SUB inst ---> ", finalValue)

    '''
    :brief MUL INSTRUCTION
    '''
    def instMul(self, myFrame):
        print("SOM V MUL")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

        operator = '*'
        finalValue = self.choiceOperator(myFrame, operator)
        print('Final value is --->', finalValue)

        myFrame.setVariableValue(self.arguments[0].text, finalValue)
        print("Toto je vysledna hodnota po MUL inst ---> ", finalValue)

    '''
    :brief IDIV INSTRUCTION
    '''
    def instIdiv(self, myFrame):
        print("SOM V IDIV")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '/'
        finalValue = self.choiceOperator(myFrame, operator)
        print('Final value is --->', finalValue)

        myFrame.setVariableValue(self.arguments[0].text, finalValue)
        print("Toto je vysledna hodnota po IDIV inst ---> ", finalValue)

    '''
    :brief LT INSTRUCTION
    '''
    def instLt(self, myFrame):
        print("SOM V LT")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[2].type != 'var'  and self.arguments[2].type != 'bool' and self.arguments[2].type != 'int' and self.arguments[2].type != 'string':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'int' and self.arguments[1].type != 'var' and self.arguments[1].type != 'bool' and self.arguments[1].type != 'string'):
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

        if self.arguments[1].type == 'var':
            firstType = myFrame.getVariableType(self.arguments[1].text)
            firstValue= myFrame.getVariableValue(self.arguments[1].text)
        else:
            firstType = self.arguments[1].type
            firstValue = self.arguments[1].text
        if self.arguments[2].type == 'var':
            secondType = myFrame.getVariableType(self.arguments[2].text)
            secondValue = myFrame.getVariableValue(self.arguments[2].text)
        else:
            secondType = self.arguments[2].type
            secondValue = self.arguments[2].text

        if firstType != secondType:
            retMessageAndValue('Failed arguments of function -> ' + self.nameOfInstruction, 53)

        if firstValue < secondValue:
            myFrame.setVariableValue(self.arguments[0].text, False)
            print("Toto je vysledna premennej -->   je ---> ", myFrame.getVariableValue(self.arguments[0].text))
        else:
            myFrame.setVariableValue(self.arguments[0].text, True)
            print("Toto je vysledna hodnota -->  je ---> ", myFrame.getVariableValue(self.arguments[0].text))

    '''
    :brief GT INSTRUCTION
    '''
    def instGt(self, myFrame):
        print("SOM V GT")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[2].type != 'var'  and self.arguments[2].type != 'bool' and self.arguments[2].type != 'int' and self.arguments[2].type != 'string':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'int' and self.arguments[1].type != 'var' and self.arguments[1].type != 'bool' and self.arguments[1].type != 'string'):
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

        if self.arguments[1].type == 'var':
            firstType = myFrame.getVariableType(self.arguments[1].text)
            firstValue= myFrame.getVariableValue(self.arguments[1].text)
        else:
            firstType = self.arguments[1].type
            firstValue = self.arguments[1].text
        if self.arguments[2].type == 'var':
            secondType = myFrame.getVariableType(self.arguments[2].text)
            secondValue = myFrame.getVariableValue(self.arguments[2].text)
        else:
            secondType = self.arguments[2].type
            secondValue = self.arguments[2].text

        if firstType != secondType:
            retMessageAndValue('Failed arguments of function -> ' + self.nameOfInstruction, 53)

        if firstValue > secondValue:
            myFrame.setVariableValue(self.arguments[0].text, False)
            print("Toto je vysledna premennej -->   je ---> ", myFrame.getVariableValue(self.arguments[0].text))
        else:
            myFrame.setVariableValue(self.arguments[0].text, True)
            print("Toto je vysledna hodnota -->  je ---> ", myFrame.getVariableValue(self.arguments[0].text))

    '''
    :brief EQ INSTRUCTION
    '''
    def instEq(self, myFrame):
        print("SOM V EQ")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        print("SOM V GT")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[2].type != 'var' and self.arguments[2].type != 'bool' and self.arguments[2].type != 'int' and \
                self.arguments[2].type != 'string':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
        if self.arguments[0].type != 'var' or (
                self.arguments[1].type != 'int' and self.arguments[1].type != 'var' and self.arguments[
            1].type != 'bool' and self.arguments[1].type != 'string'):
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

        if self.arguments[1].type == 'var':
            firstType = myFrame.getVariableType(self.arguments[1].text)
            firstValue = myFrame.getVariableValue(self.arguments[1].text)
        else:
            firstType = self.arguments[1].type
            firstValue = self.arguments[1].text
        if self.arguments[2].type == 'var':
            secondType = myFrame.getVariableType(self.arguments[2].text)
            secondValue = myFrame.getVariableValue(self.arguments[2].text)
        else:
            secondType = self.arguments[2].type
            secondValue = self.arguments[2].text

        if firstType != secondType:
            retMessageAndValue('Failed arguments of function -> ' + self.nameOfInstruction, 53)

        if firstValue == secondValue:
            myFrame.setVariableValue(self.arguments[0].text, True)
            print("Toto je vysledna premennej -->   je ---> ", myFrame.getVariableValue(self.arguments[0].text))
        else:
            myFrame.setVariableValue(self.arguments[0].text, False)
            print("Toto je vysledna hodnota -->  je ---> ", myFrame.getVariableValue(self.arguments[0].text))

    '''
    :brief ADD INSTRUCTION
    '''
    def instAnd(self):
        print("SOM V AND")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief OR INSTRUCTION
    '''
    def instOr(self):
        print("SOM V OR")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief NOT INSTRUCTION
    '''
    def instNot(self):
        print("SOM V NOT")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief INT2CHAR INSTRUCTION
    '''
    def instInt2Char(self):
        print("SOM V INT2CHAR")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief STRI2INT INSTRUCTION
    '''
    def instStri2Int(self):
        print("SOM V Stri2Int")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief READ INSTRUCTION
    '''
    def instRead(self, myFrame):
        print("SOM V Read")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or self.arguments[1].type != 'type':
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)
        myFrame.setVariableValue(self.arguments[0].text, 0)
        print("Toto je hodnota v read --->", self.arguments[0].text)

    '''
    :brief WRITE INSTRUCTION
    '''
    def instWrite(self):
        print("SOM V Write")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief CONCAT INSTRUCTION
    '''
    def instConcat(self):
        print("SOM V Concat")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief STRLEN INSTRUCTION
    '''
    def instStrlen(self):
        print("SOM V Strlen")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief GETCHAR INSTRUCTION
    '''
    def instGetchar(self):
        print("SOM V Getchar")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief SETCHAR INSTRUCTION
    '''
    def instSetchar(self):
        print("SOM V Setchar")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief TYPE INSTRUCTION
    '''
    def instType(self):
        print("SOM V Type")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief LABEL INSTRUCTION
    '''
    def instLabel(self):
        print("SOM V Label")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief JUMP INSTRUCTION
    '''
    def instJump(self):
        print("SOM V Jump")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief JUMPIFEQ INSTRUCTION
    '''
    def instJumpifeq(self):
        print("SOM V Jumpifeq")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief JUMPIFNEQ INSTRUCTION
    '''
    def instJumpifneq(self):
        print("SOM V Jumpifneq")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
    '''
    :brief DPRINT INSTRUCTION
    '''
    def instDprint(self):
        print("SOM V Dprint")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief BREAK INSTRUCTION
    '''
    def instBreak(self):
        print("SOM V Break")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
