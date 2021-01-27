from Err.err import *
import re

class Args:
    text = ''               # it could be string , bool , interger , variable , type
    type = ''               # it could be string , bool , type
    argElement = ''         # it is argument element of concrete instructiom

    '''
    :brief function which inicilize needed data...
    :param self
    :param argElement
    '''
    def inicialize(self,argElement):
        self.argElement = argElement

    '''
    :brief  functions which are helpul to parse instruction arguments...
    :param  self
    :param  argElement
    '''

    def argInt(self,argElement):
        if argElement.text is None:
            retMessageAndValue('Error: expected integer value...', 32)
        if re.match('^[+-]?[0-9]+$', argElement.text) is None:
            retMessageAndValue('Error: expected interger value...', 32)
        self.text = int(argElement.text)

    def argString(self,argElement):
        if argElement.text is not None:
            stringVal = argElement.text
            if re.match('[#\s]', argElement.text) is not None:
                retMessageAndValue('Error: invalid character in string.', 32)
            self.text = stringVal
        else:
            self.text = ''

    def argBool(self, argElement):
        if argElement.text != 'false' and argElement.text != 'true':
            retMessageAndValue('Error: expected bool value...', 32)
        if argElement.text == 'true':
            self.text = True
        else:
            self.text = False

    def argVar(self, argElement):
        if argElement.text is None:
            retMessageAndValue('Error: expected variable name...', 32)
        if re.match('^(GF@|LF@|TF@)[|A-Z|a-z|\-|\$|\*]+[\%|A-Z|a-z|0-9|_|\-|\$|\*]*$',
            argElement.text) is None:  # variable name lexical check
            retMessageAndValue('Error: variable...', 32)
        self.text = argElement.text

    def argLabel(self, argElement):
        if argElement.text is None:
            retMessageAndValue('Error: expected labem name', 32)
        if re.match('^[\%|A-Z|a-z|_|\-|\$|\*]+[\%|A-Z|a-z|0-9|_|\-|\$|\*]*$',
                    argElement.text) is None:  # label name lexical check
            retMessageAndValue('Error: label...', 32)
        self.text = argElement.text

    def argType(self, argElemnt):
        if argElemnt.text != 'bool' and argElemnt.text != 'int' and argElemnt.text != 'string':
            retMessageAndValue('Error: expected type name', 32)
        self.text = argElemnt.text

    '''
    :brief  function which parse instruct arguments
    :param  self
    :param  argElement
    '''
    def parseInstructArgument(self,argElement):
        if argElement.attrib['type'] == 'int':
            self.argInt(argElement)
        elif argElement.attrib['type'] == 'bool':
            self.argBool(argElement)
        elif argElement.attrib['type'] == 'string':
            self.argString(argElement)
        elif argElement.attrib['type'] == 'label':
            self.argLabel(argElement)
        elif argElement.attrib['type'] == 'type':
            self.argType(argElement)
        elif argElement.attrib['type'] == 'var':
            self.argVar(argElement)
        else:
            retMessageAndValue('Error: type attribute i do not know... ', 31)

        self.type = argElement.attrib['type']




