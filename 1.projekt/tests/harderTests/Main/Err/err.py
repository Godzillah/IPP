import sys

# IMITATING CLASS OF ERR #

def retMessageAndValue(infoMessage , retValue ):
    sys.stderr.write(infoMessage)
    exit(retValue)

def retErrMessage(infoMessage):
    sys.stderr.write(infoMessage)

def retMessage(infoMessage):
    return infoMessage

def retValue(retValue):
    exit(retValue)

