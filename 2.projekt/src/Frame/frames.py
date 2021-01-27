import re
from Frame.frame import Frame
from Err.err import *

class Frames:
    arrayOfFrames = []              # array of frames
    globalFrame = Frame()           # inicialization of GLOBAL FRAME
    tempFrame = None                # TEMPORARY FRAME not defined at the start only global...

    '''
    :brief  function which creates temporary frame
    :param  self
    '''
    def createFrame(self):
        self.tempFrame = Frame()                                        # creating temporrary frame...

    '''
    :brief  function which pushs temporary frame ---> local frame
    :param  self
    :param  frame
    '''
    def pushFrame(self, myFrame):
        if myFrame is not None:                                         # if tempporary frames
            self.arrayOfFrames.append(myFrame)                          # append == push ----> pushing new frame to frames
            self.tempFrame = None
        elif myFrame is None:
            retMessageAndValue("Temporary frame not defined...", 55)  # 55 - běhová chyba interpretace – rámec neexistuje (např. čtení z prázdného zásobníku rámců).
    '''
    :brief  function which pops local frame ---> temporary frame
    :param  self
    :param  frame
    '''
    def popFrame(self):
        if len(self.arrayOfFrames) != 0:
            self.tempFrame = self.arrayOfFrames.pop()             # from TF to local...
        else:
            retMessageAndValue("Local frame not defined...", 55)  # 55 - běhová chyba interpretace – rámec neexistuje (např. čtení z prázdného zásobníku rámců).

    '''
    :brief  function which add variable to the available frame
    :param  self
    :param  variable
    '''
    def addVariableToTheFrame(self, variable):
        if re.match('^GF@.*$', variable) is not None:                       # regular expression which matching everything which starts with GF@ and continue with others chars
            variableMatch = re.match("^(GF@)(.*)$", variable)               # store f.e: GF@ahoj
            variableName = variableMatch.group(2)                           # convert: GF@ahoj --> ahoj
            self.globalFrame.addVariable(variableName)                      # add global variable to the global frame
        elif re.match("^TF@.*$", variable) is not None:                     # regular expression which matching everything which starts with TF@ and continue with others chars
            if self.tempFrame is not None:                                  # if tempframe exists then...
                variableMatch = re.match("^(TF@)(.*)$", variable)           # store f.e: TF@ahoj
                variableName = variableMatch.group(2)                       # convert: ahoj
                self.tempFrame.addVariable(variableName)                    # add temp variable to the temp frame
            else:
                retMessageAndValue("Temporary frame not defined... ", 55)   # else temporary frame does not exists them error...
        else:
            if re.match("^LF@.*$", variable) is not None:                   # regular expression which matching everything which starts with LF@ and continue with others chars
                if self.isLocalFrame() is None:                             # if local frame does not exist...
                    retMessageAndValue("Local frame not defined...", 55)    # returning with competent value...
                else:                                                       # else if local frame exists
                    variableMatch = re.match("^(LF@)(.*)$", variable)       # store
                    variableName = variableMatch.group(2)                   # convert
                    self.isLocalFrame().addVariable(variableName)           # add.. local variable to the loca frame...
    '''
    :brief function which takes variable value 
    :param self
    :param
    '''
    def getVariableValue(self, variable):
        if re.match("^GF@.*$", variable) is not None:                                                           # regular expression which matching everything which starts with GF@ and continue with others chars
            variableMatch = re.match("^(GF@)(.*)$", variable)                                                   # store
            variableName = variableMatch.group(2)                                                               # convert
            if variableName in self.globalFrame.dictOfVariables:                                                # search for concreate variable in dictionary...
                return self.globalFrame.dictOfVariables.get(variableName)
            else:
                retMessageAndValue("Global frame has no variables... " + variable, 54)
        elif re.match('^TF@.*$', variable) is not None:                                                          # regular expression which matching everything which starts with TF@ and continue with others chars
            variableMatch = re.match("^(TF@)(.*)$", variable)                                                    # store
            variableName = variableMatch.group(2)                                                                # convert
            if self.tempFrame is None:                                                                           # if tempFrame exists
                retMessageAndValue("Temporary frame not defined... " + variable, 55)
            if variableName in self.tempFrame.dictOfVariables:                                                   # searching for tempVariable in dictionary...
                return self.tempFrame.dictOfVariables.get(variableName)
            else:
                retMessageAndValue("Temporary frame has no variables " + variable, 54)
        elif re.match('^LF@.*$', variable) is not None:                                                          # regular expression which matching everything which starts with LF@ and continue with others chars
            variableMatch = re.match("^(LF@)(.*)$", variable)                                                    # store
            variableName = variableMatch.group(2)                                                                # convert...
            if len(self.arrayOfFrames) == 0:                                                                     # if frame exits...
                retMessageAndValue("Local frame not defined... " + variable, 55)
            if variableName in self.isLocalFrame().dictOfVariables:                                              # searching for concrete variablen name in dictionary...
                return self.isLocalFrame().dictOfVariables.get(variableName)
            else:
                retMessageAndValue("Local frame has no variables " + variable, 54)

    '''
    :brief function which sets the variable value to the dict of variables
    :param self
    :param variable 
    :param value    
    '''
    def setVariableValue(self, variable, value):
        if re.match("^GF@.*$", variable) is not None:                                                       # regular expression which matching everything which starts with GF@ and continue with others chars
            variableMatch = re.match("^(GF@)(.*)$", variable)                                               # store
            variableName = variableMatch.group(2)                                                           # convert
            if variableName in self.globalFrame.dictOfVariables:                                            # search
                self.globalFrame.dictOfVariables[variableName] = value                                      # insert
            else:
                retMessageAndValue("Global frame has no variables " + variable, 54)
        elif re.match('^TF@.*$', variable) is not None:                                                      # regular expression which matching everything which starts with TF@ and continue with others chars
            if self.tempFrame is None:                                                                       # tempframe does not exists...
                retMessageAndValue("Temporary frame not defined... " + variable, 55)
            variableMatch = re.match("^(TF@)(.*)$", variable)                                                # store
            variableName = variableMatch.group(2)                                                            # convert
            if variableName in self.tempFrame.dictOfVariables:                                               # search
                self.tempFrame.dictOfVariables[variableName] = value                                         # insert
            else:
                retMessageAndValue("Temporary frame has no variables " + variable, 54)
        elif re.match('^LF@.*$', variable) is not None:                                                     # regular expression which matching everything which starts with LF@ and continue with others chars
            if len(self.arrayOfFrames) == 0:                                                                # checking if frame exits...
                retMessageAndValue("Local frame not defined... " + variable, 55)
            variableMatch = re.match("^(LF@)(.*)$", variable)                                               # store
            variableName = variableMatch.group(2)                                                           # convert
            if variableName in self.isLocalFrame().dictOfVariables:                                         # search
                self.isLocalFrame().dictOfVariables[variableName] = value                                   # insert
            else:
                retMessageAndValue("Local frame has no variables " + variable, 54)
    '''
    :brief  function which give variable type if it is inicialized
    :param  self
    :param  variable
    :use    getVariableValue
    '''
    def getVariableType(self, variable):
        variableValue = self.getVariableValue(variable)
        if variableValue is int:
            retMessage('int')
        elif variableValue is bool:
            retMessage('bool')
        elif variableValue is None:
            retMessageAndValue('You do not inicialized variable: ' + variable, 56)
        else:
            return 'string'

    '''
    :brief  function which tell if local frame exist or not...
    :param  self 
    '''
    def isLocalFrame(self):
        if len(self.arrayOfFrames) != 0:                                             # we have local frame...
            return self.arrayOfFrames[len(self.arrayOfFrames) - 1]
        else:                                                                        # we do not have local frame....
            return None
    # helpful function
    '''
    :brief  function which tells us if is variable in global frame or not
    :param  self
    :param  variable
    '''
    def isVarInGlobalFrame(self, variable):
        if re.match('^GF@.*$', variable):                                           # matching GF@..
            retMessageAndValue("Variable is in global frame ->" + variable, 1)
        else:
            retMessageAndValue("No variable in global frame.", -1)

    '''
    :brief  function which tells us if is variable in temporary frame or not
    :param  self
    :param  variable
    '''
    def isVarInTempFrame(self, variable):
        if re.match('^TF@.*$', variable):                                               # matching TF@..
            retMessageAndValue("Variable is in temporary frame ->" + variable, 1)
        else:
            retMessageAndValue("No variable in temporary frame.", -1)

    '''
    :brief  function which tells us if is variable in temporary frame or not
    :param  self
    :param  variable
    '''
    def isVarInLocalFrame(self, variable):
        if re.match('^LF@.*$', variable):                                               # matching LF@..
            retMessageAndValue("Variable is in local frame ->" + variable, 1)
        else:
            retMessageAndValue("No variable in local frame", -1)
    '''
    :brief function which give len of frame
    :param  self
    '''
    def getLenFrames(self):
        if len(self.arrayOfFrames) < 0:                                         # If length of array is less than 0 ret error...
            retMessageAndValue("Number of frame is incorrect", -1)
        else:
            print(len(self.arrayOfFrames))

    # def getLenVarInGlobalFrame(self):
    # def getLenVarInTempFrame(self):
    # def getLenVarInLocalFrame(self):
