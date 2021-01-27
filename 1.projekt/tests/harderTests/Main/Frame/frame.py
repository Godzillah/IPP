
class Frame:
    dictOfVariables = {}      # dictionary which will store defined variables in frame...

    '''
    :brief function which can add variable to the dictionary...
    :param self
    :param variable
    '''
    def addVariable(self, variable):
        self.dictOfVariables[variable] = None
    '''
    :brief  function which gets the variable type
    :param  self
    :param  variableName
    '''
    def getVariableValue(self, variableName):
        return self.dictOfVariables[variableName]

    '''
    :brief  function which sets the variable type
    :param  self
    :param  variableName
    :param  value
    '''
    def setVariableValue(self, variableName , value):
        self.dictOfVariables[variableName] = value

    '''
    :brief function which prints the variable type
    :param  self
    :param  variableName
    '''
    def printVariableValue(self, variableName):
        print(self.getVariableValue(variableName))