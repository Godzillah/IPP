import itertools

from Err.err import retMessageAndValue
from Instruction.Args.args import Args
from Instruction.instruction import Instruction
from Frame.frames import Frames

class Instructions:

    arrayOfInstructions = [None]                                # array of instructions..
    stackOfInstructions = []                                    # stack of instruction...

    '''
    :brief  function which parse concrete instruction f.e : ADD etc.
    :param  self
    :param  instXml
    '''
    def parseInstruction(self, instXml):
        elementExists = False                                       # helpful variable whitch tell when element is defined
        orderOfArgument = 1                                         # order of arguments starts with 1
        arrayOfArguments= []                                        # array of argument...

        for number in range(0, len(instXml)):
            for argElement in instXml:
                if argElement.tag != str('arg' + str(orderOfArgument)):   # concat arg + number or orderArgument starts with 1
                    continue
                elementExists = True
                myArgs = Args()                                     # contructor of arguments
                myArgs.inicialize(argElement)                       # inicialize argument
                myArgs.parseInstructArgument(argElement)            # check what type is arg* int / string etc.
                arrayOfArguments.append(myArgs)
                orderOfArgument += 1                                # increment order
                break
            if elementExists == False:
                retMessageAndValue('Error: element arg in XML' + '\n', 31)
            elementExists = False

        myInstruction = Instruction()
        myInstruction.inicialization(arrayOfArguments, instXml.attrib['opcode'], instXml.attrib['order'])
        self.arrayOfInstructions.append(myInstruction)

    def interpretInstructions(self):
        ArrayOfFrames = Frames()                                                        # global frame created...
        self.stackOfInstructions.append(str(1))

        for x in itertools.repeat(1):                                                        # infinite loop
            pass
            if len(self.stackOfInstructions) == 0:
                retMessageAndValue('Instruction of reader is empty...' + '\n' , 56)
            orderOfInstructions = int(self.stackOfInstructions.pop())
            self.stackOfInstructions.append(str(orderOfInstructions + 1))

            if orderOfInstructions >= len(self.arrayOfInstructions):                       # interpretation of last instuction
                    break
            self.arrayOfInstructions[orderOfInstructions].parseInstructions(ArrayOfFrames)  # parse Instruction...