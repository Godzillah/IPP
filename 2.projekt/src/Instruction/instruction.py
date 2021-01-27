from Frame.frame import Frame
from Err.err import *

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

    '''
    :brief function which firstly choice operator , then calculate competent value to the instruction...
    :param  myFrame
    :param  operator
    '''

    def choiceOperator(self, myFrame , operator):
        if operator == '+' or operator == '-' or operator == '*' or operator == '/':
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'int':
                retMessageAndValue('Failed parameters of instruction -> ' + self.nameOfInstruction, 52)
            if self.arguments[1].type == 'var':
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
                if myFrame.getVariableType(self.arguments[1].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction, 53)
            else:
                firstValue = self.arguments[1].text

            if self.arguments[2].type == 'var':
                secondValue = myFrame.getVariableValue(self.arguments[2].text)
                if myFrame.getVariableType(self.arguments[2].text) != 'int':
                    retMessageAndValue('Failed parameters of instruction --> ' + self.nameOfInstruction , 53)
            else:
                secondValue = self.arguments[2].text

            if operator == '+':
                finalValue = firstValue + secondValue
                return finalValue
            elif operator == '-':
                finalValue = firstValue - secondValue
                return finalValue
            elif operator == '*':
                finalValue = firstValue * secondValue
                return finalValue
            elif operator == '/':
                if secondValue == 0:
                    retMessageAndValue('Dividing by zero value..', 57)
                finalValue = firstValue // secondValue
                return finalValue
        elif operator == '>' or operator == '<' or operator == "=":
            if self.arguments[2].type != 'var' and self.arguments[2].type != 'bool' and self.arguments[2].type != 'int' and self.arguments[2].type != 'string':
                retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
            if self.arguments[0].type != 'var' or (
                    self.arguments[1].type != 'int' and self.arguments[1].type != 'var' and self.arguments[1].type != 'bool' and self.arguments[1].type != 'string'):
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

            if operator == '<':
                if firstValue < secondValue:
                    myFrame.setVariableValue(self.arguments[0].text, False)

                else:
                    myFrame.setVariableValue(self.arguments[0].text, True)

            elif operator == '>':
                if firstValue > secondValue:
                    myFrame.setVariableValue(self.arguments[0].text, False)

                else:
                    myFrame.setVariableValue(self.arguments[0].text, True)
            elif operator == '=':
                if firstValue == secondValue:
                    myFrame.setVariableValue(self.arguments[0].text, True)
                else:
                    myFrame.setVariableValue(self.arguments[0].text, False)
        elif operator == '&' or operator == '|':
            if self.arguments[2].type != 'bool' and self.arguments[2].type != 'var':
                retMessageAndValue('Failed arguments of function ->', 52)
            if self.arguments[0].type != 'var' or (
                    self.arguments[1].type != 'bool' and self.arguments[1].type != 'var'):
                retMessageAndValue('Failed arguments of function ->', 52)

            if self.arguments[1].type == 'var':
                firstType = myFrame.getVariableType(self.arguments[1].text)
                firstValue = myFrame.getVariableValue(self.arguments[1].text)
            else:
                firstValue = self.arguments[1].text
                firstType = 'bool'

            if self.arguments[2].type == 'var':
                secondType = myFrame.getVariableType(self.arguments[2].text)
                secondValue = myFrame.getVariableValue(self.arguments[2].text)
            else:
                secondType = self.arguments[2].type
                secondValue = 'bool'

            if firstType != secondType:
                retMessageAndValue('Failed arguments of function ->'+ self.nameOfInstruction , 53)

            if operator == '&':
                if firstValue == True and secondValue == True:
                    myFrame.setVariableValue(self.arguments[0].text, True)
                else:
                    myFrame.setVariableValue(self.arguments[0].text, False)
            elif operator == '|':
                if firstValue == True or secondValue == True:
                    myFrame.setVariableValue(self.arguments[0].text, True)
                elif firstValue == True or secondValue == False:
                    myFrame.setVariableValue(self.arguments[0].text, True)
                elif firstValue == False or secondValue == True:
                    myFrame.setVariableValue(self.arguments[0].text, True)
                else:
                    myFrame.setVarValue(self.arguments[0].text, False)

    '''
    :brief  function which parse whole instructions ->FSM<-
    :param  self
    :param  myFrame 
    '''
    def parseInstructions(self,myFrame):
        if self.nameOfInstruction == options.get(0):        # MOVE
            self.instMove(myFrame)
        elif self.nameOfInstruction == options.get(1):      # CREATEFRAME
            self.instCreateframe(myFrame)
        elif self.nameOfInstruction == options.get(2):      # PUSHFRAME
            self.instPushframe(myFrame)
        elif self.nameOfInstruction == options.get(3):      # POPFRAME
            self.instPopframe(myFrame)
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
            self.instAnd(myFrame)
        elif self.nameOfInstruction == options.get(17):     # OR
            self.instOr(myFrame)
        elif self.nameOfInstruction == options.get(18):     # NOT
            self.instNot(myFrame)
        elif self.nameOfInstruction == options.get(19):     # INT2CHAR
            self.instInt2Char()
        elif self.nameOfInstruction == options.get(20):     # STRI2INT
            self.instStri2Int()
        elif self.nameOfInstruction == options.get(21):     # READ
            self.instRead(myFrame)
        elif self.nameOfInstruction == options.get(22):     # WRITE
            self.instWrite(myFrame)
        elif self.nameOfInstruction == options.get(23):     # CONCAT
            self.instConcat(myFrame)
        elif self.nameOfInstruction == options.get(24):     # STRLEN
            self.instStrlen(myFrame)
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
            retMessageAndValue("Error: Unknow Instruction"+ self.nameOfInstruction , 32)

    '''
    :brief  MOVE INSTRUCTION
    :param  self
    :param  myFrame
    '''
    def instMove(self, myFrame):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'var' and self.arguments[1].type != 'int' and self.arguments[1].type != 'bool' and self.arguments[1].type != 'string'):
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
        if self.arguments[1].type == 'var':
            variableValue = myFrame.getVariableValue(self.arguments[1].text)
            if variableValue is None:
                retMessageAndValue('Variable does not have defined value', 56)
            myFrame.setVariableValue(self.arguments[0].text, variableValue)
        else:
            myFrame.setVariableValue(self.arguments[0].text, self.arguments[1].text)

    '''
    :brief CREATEFRAME INSTRUCTION
    :param  myFrame
    '''
    def instCreateframe(self, myFrame):
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        else:
            myFrame.tempFrame = Frame()  # creating tempororary frame

    '''
    :brief PUSHFRAME INSTRUCTION
    :param  myFrame
    '''
    def instPushframe(self, myFrame):
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        myFrame.pushFrame(myFrame.tempFrame)

    '''
    :brief POPFRAME INSTRUCTION
    :param  myFrame
    '''
    def instPopframe(self, myFrame):
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        myFrame.popFrame()                                                                          # from local frame --> temporary frame

    '''
    :brief DEFVAR INSTRUCTION
    :param  myFrame
    '''
    def instDefVar(self, myFrame):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)
        myFrame.addVariableToTheFrame(self.arguments[0].text)

    '''
    :brief CALL INSTRUCTION
    '''
    def instCall(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'label':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

        # NO TIME :(

    '''
    :brief RETURN INSTRUCTION
    '''
    def instReturn(self):
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

    '''
    :brief PUSHS INSTRUCTION
    '''
    def instPushs(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' and self.arguments[0].type != 'int' and self.arguments[0].type != 'bool' and self.args[
            0].type != 'string':
            retMessageAndValue('Failed arguments of function ->' + self.instructName, 52)

    '''
    :brief POPS INSTRUCTION
    '''
    def instPops(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0] != 'var':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

    '''
    :brief ADD INSTRUCTION
    :param  myFrame
    '''
    def instAdd(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

        operator = '+'
        finalValue = self.choiceOperator(myFrame, operator)
        myFrame.setVariableValue(self.arguments[0].text, finalValue)

    '''
    :brief SUB INSTRUCTION
    :param  myFrame
    '''
    def instSub(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '-'
        finalValue = self.choiceOperator(myFrame, operator)

        myFrame.setVariableValue(self.arguments[0].text, finalValue)


    '''
    :brief MUL INSTRUCTION
    :param  myFrame
    '''
    def instMul(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

        operator = '*'
        finalValue = self.choiceOperator(myFrame, operator)
        myFrame.setVariableValue(self.arguments[0].text, finalValue)


    '''
    :brief IDIV INSTRUCTION
    :param  myFrame
    '''
    def instIdiv(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '/'
        finalValue = self.choiceOperator(myFrame, operator)
        myFrame.setVariableValue(self.arguments[0].text, finalValue)


    '''
    :brief LT INSTRUCTION
    :param  myFrame
    '''
    def instLt(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '<'
        self.choiceOperator(myFrame , operator)

    '''
    :brief GT INSTRUCTION
    :param  myFrame
    '''
    def instGt(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '>'
        self.choiceOperator(myFrame, operator)


    '''
    :brief EQ INSTRUCTION
    :param  myFrame
    '''
    def instEq(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '='
        self.choiceOperator(myFrame, operator)

    '''
    :brief ADD INSTRUCTION
    :param  myFrame
    '''
    def instAnd(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '&'
        self.choiceOperator(myFrame, operator)

    '''
    :brief OR INSTRUCTION
    :param  myFrame
    '''
    def instOr(self, myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        operator = '|'
        self.choiceOperator(myFrame, operator)

    '''
    :brief NOT INSTRUCTION
    :param  myFrame
    '''
    def instNot(self, myFrame):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'bool' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of function ->', 52)

        if self.arguments[1].type == 'var':
            firstValue = myFrame.getVariableValue(self.arguments[1].text)
            firstType = myFrame.getVariableType(self.arguments[1].text)
        else:
            firstType = 'bool'
            firstValue = self.arguments[1].text

        if firstType != 'bool':
            retMessageAndValue('Failed arguments of function ->', 52)

        if firstValue == True:
            myFrame.setVariableValue(self.arguments[0].text, False)
        else:
            myFrame.setVariableValue(self.arguments[0].text, True)

    '''
    :brief INT2CHAR INSTRUCTION
    '''
    def instInt2Char(self):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type  != 'var' or (self.arguments[1].type != 'int' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of function ->', 52)

    '''
    :brief STRI2INT INSTRUCTION
    '''
    def instStri2Int(self):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type  != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var') or (self.arguments[2].type != 'string' and self.arguments[2].type != 'var'):
            retMessageAndValue('Failed arguments of function ->', 52)
    '''
    :brief READ INSTRUCTION
    :param  myFrame
    '''
    def instRead(self, myFrame):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or self.arguments[1].type != 'type':
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)

        myFrame.setVariableValue(self.arguments[0].text, 0)

    '''
    :brief WRITE INSTRUCTION
    :param  myFrame
    '''
    def instWrite(self, myFrame):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)

        if self.arguments[0].type != 'var' and self.arguments[0].type != 'int' and self.arguments[0].type != 'string' and self.arguments[
            0].type != 'bool':
            retMessageAndValue('Failed arguments of function ->' + self.nameOfInstruction, 52)

        if self.arguments[0].type == 'var':
            stringRet = myFrame.getVariableValue(self.arguments[0].text)
            typeRet = myFrame.getVariableType(self.arguments[0].text)
            if typeRet == 'bool':
                print('true') if stringRet else print('false')
            else:
                print(stringRet)
        else:
            if self.arguments[0].type == 'bool':
                if self.arguments[0].tex:
                    print('true')
                else:
                    print('false')
            else:
                print(self.arguments[0].text)

    '''
    :brief CONCAT INSTRUCTION
    :param  myFrame
    '''
    def instConcat(self,myFrame):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var' ) or (
                self.arguments[1].type != 'string' and self.arguments[2].type != 'var'):
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)

        if self.arguments[1].type == 'var':
            firstValue = myFrame.getVariableValue(self.arguments[1].text)
            if myFrame.getVariableType(self.arguments[1].text) != 'string':
                retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 53)
        else:
            firstValue = self.arguments[1].text

        if self.arguments[2].type == 'var':
            secondValue = myFrame.getVariableValue(self.arguments[2].text)
            if myFrame.getVarType(self.args[2].text) != 'string':
                retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 53)
        else:
            secondValue = self.arguments[2].text

        myFrame.setVariableValue(self.arguments[0].text, firstValue + secondValue)

    '''
    :brief STRLEN INSTRUCTION
    :param  myFrame
    '''
    def instStrlen(self, myFrame):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)

        if self.arguments[1].type == 'var':
            if myFrame.getVariableType(self.arguments[1].text) != 'string':
                retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 53)
            firstValue = myFrame.getVariableValue(self.arguments[1].text)
            myFrame.setVariableValue(self.arguments[0].text, len(firstValue))
        else:
            myFrame.setVariableValue(self.arguments[0].text, len(self.arguments[1].text))

    '''
    :brief GETCHAR INSTRUCTION
    '''
    def instGetchar(self):
        print("SOM V Getchar")
        print("Toto je hodnota argumentov --->", len(self.arguments))
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)
    '''
    :brief SETCHAR INSTRUCTION
    '''
    def instSetchar(self):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)

    '''
    :brief TYPE INSTRUCTION
    '''
    def instType(self):
        if len(self.arguments) != 2:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'var' or (self.arguments[1].type != 'string' and self.arguments[1].type != 'var'):
            retMessageAndValue('Failed arguments of instruction --> :' + self.nameOfInstruction, 52)

    '''
    :brief LABEL INSTRUCTION
    '''
    def instLabel(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'label':
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 52)
        return

    '''
    :brief JUMP INSTRUCTION
    '''
    def instJump(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'label':
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 52)

    '''
    :brief JUMPIFEQ INSTRUCTION
    '''
    def instJumpifeq(self):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'label' or (
                self.arguments[1].type != 'string' and self.arguments[1].type != 'var') or (
                self.arguments[1].type != 'string' and self.arguments[2].type != 'var'):
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 52)

    '''
    :brief JUMPIFNEQ INSTRUCTION
    '''
    def instJumpifneq(self):
        if len(self.arguments) != 3:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'label' or (
                self.arguments[1].type != 'string' and self.arguments[1].type != 'var') or (
                self.arguments[1].type != 'string' and self.arguments[2].type != 'var'):
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 52)
    '''
    :brief DPRINT INSTRUCTION
    '''
    def instDprint(self):
        if len(self.arguments) != 1:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
        if self.arguments[0].type != 'string' and self.arguments[0].type != 'var':
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 52)

    '''
    :brief BREAK INSTRUCTION
    '''
    def instBreak(self):
        if len(self.arguments) != 0:
            retMessageAndValue("Failed arguments of function ->" + self.nameOfInstruction, 31)
