import re
from Err.err import *
import xml.etree.ElementTree as ET
from Instruction.instructions import Instructions
from xml.etree.ElementTree import ParseError

# IMITATING THE CLASS ParseArgs #
myInstruction = Instructions()

def parseArgs():

    if len(sys.argv) != 2:
        retMessageAndValue("Wrong number of parameters\n" , 10)
    # --help || --source=file
    # for two arguments
    else:
        if sys.argv[1] == '--help':
                print(
                    "\t\t---> Usage: "
                    "interpret.py [options] <---\n"
                    "[*******************************************************************************]\n"
                    "[\tOptions:\t\t\t\t\t\t\t\t]\n"
                    "[\t\t--help            will show help\t\t\t\t]\n"
                    "[\t\t--source=file.txt \t\t\t\t\t\t]\n"
                    "[\tExample:\t\t\t\t\t\t\t\t]\n"
                    "[\t\tpython3.6 interpret.py --help \t\t\t\t\t]\n"
                    "[\t\tpython3.6 interpret.py --source=file.txt\t\t\t]\n"
                    "[*******************************************************************************]\n")
                retValue(0)


        elif re.match('(--source=)(.+)$', sys.argv[1]):
            fileName =  re.match('(--source=)(.+)$', sys.argv[1])
            fileName = fileName.group(2)
            print("This is file --> ", fileName)         # its the place where = begins so f.e --source=||||test1.xml|||| <- that test will have
            return fileName
        else:
            retMessageAndValue("You typed wrong arguments\n", 10)

def xmlParse(fileName):

    try:
        xmlFile = ET.parse(fileName)
    except ParseError:
        retMessageAndValue('Xml file not valid\n', 31)
    except FileNotFoundError:
        retMessageAndValue('File does not exist\n', 11)

    root = xmlFile.getroot()

    if(root.tag != 'program'):
        retMessageAndValue('Missing root.tag program\n', 31)

    # Control for header of xml...
    for rootAttr in root.attrib:
        # print(rootAttr)
        # print(root.attrib[rootAttr])
        if rootAttr != 'language' or root.attrib[rootAttr] != 'IPPcode18':
            retMessageAndValue('Missing language or IPpcode18', 31)
        elif rootAttr == 'language' and root.attrib[rootAttr] == 'IPPcode18':
            print("All is fine")
            continue            #all is fine you can continue

    for order in range(1, len(root)+1):
        for instructElement in root:
            if instructElement.tag != 'instruction':
                retMessageAndValue('No tag instruction in xml file', 31)
            if instructElement.attrib['order'] != str(order):
                continue
            # if instructElement.attrib['order'] == instructElement.attrib['order']:
            #     retMessageAndValue('Error: Same order value...', 31)

            myInstruction.parseInstruction(instructElement)             # PARSE INSTRUCTIONS....
            myInstruction.interpretInstructions()                       # INTERPRET INSTRUCTIONS....
            break