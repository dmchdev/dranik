#! usr/bin/env python
#####################################################################
# This program was created by Dmitriy Chernoshey                    #
# The official name for this tool is Dranik                         #
# It is available for free use under the GNU license.               #
# You may contact the developer at GitHub under dmchdev             #
# You may introduce modifications to this program for your own      #
# projects, however, if you wish to publish your modified version,  #
# I ask that you keep this header intact for copyright purposes,    #
# and indicate that it has been modified from its original version, #
# which can be found on GitHub at dmchdev.                          #
# I would greatly appreciate you getting in touch with me and       #
# sending me the modifications, so that I can integrate them into   #
# the original version and give you proper collaborator credit.
# Forking this project is encouraged!
# Enjoy testing!                                                    #
##################################################################### 

#---------------USAGE INSTRUCTIONS----------------------------------#
#
# 1. Create your scenarios as .txt or .py files in the following  format:
# Scenario: Name of scenario: @   for no tags OR @tagname if tag desired
#	Select element A from table B
#	Verify A is more than B
#
# NOTE: tags are optional but you must put the @ sign after Name of scenario
# because the @ sign is used as a marker for the scenario parsing function and if absent,
# dranik will generate invalid scenario code and your tests will fail.
#
# For example, scenario without tags will begin like this:
# Scenario: Name of scenario: @
# With tags, it will begin like this:
# Scenario: Name of scenario: @tagname
#
# You may use tab or space indentation or no indentation in method calls, but should not
# indent the 'Scenario: Name of scenario: @' line
#
# 2. Create your methods.py file. This is the permanent hardcoded name for every project.
# Although you may, of course modify the dranik.py to choose some other name, but
# for consistency and portability of test suites it is not recommended.
#
#  Your methods must look like this (stay consistent with indentation!! Python does not forgive inconsistency!!):
# 
#  def (Select element ^x from table ^y):
#  		Method code

#  def (Verify ^x is more than ^y):
#  		Method code
#
# ^x and ^y are variables. Use any number of variables desired. You may use them later to insert into 
# function calls or xpaths using Python's format() function. Please note that the scenario parser assigns
# string values to these variables. You must do any necessary data type conversions within 
# your method definitions.
# 3. In the same directory as your methods.py file, create a file named testheader.py looking like this:
# Before:
# Some Python code to execute before each scenario
# After:
# Some Python code to execute after each scenario


"""This program is designed to mimic to some degree the behavior of Cucumber and Lettuce testing tools. It is
definitely a simplified version of those tools. It does not include the Gherkin language parser, as it is not
really necessary for majority of web application tests. It uses the 'just tell the computer what to do' approach
step-by-step. You simply write your scenarios in proper format and Dranik will generate and execute Python code,
which will run your tests and provide output with tracebacks. Dranik also makes use of Python's ctypes module to
provide Windows users with colored output--UNIX-green text, yellow tracebacks, red errors, blue lines. 
Beside running tests, the user gets a summary of the test run--how many tests failed and passed and specific names
of failed tests. There is an option to create a test log file. Although designed with Selenium Webdriver in mind, 
Dranik can be used to execute regular Python code, as well. """
import time
import sys, traceback, ctypes
from sys import platform as _platform

STD_OUTPUT_HANDLE= -11
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED  = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.
BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED  = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
colorFlag=0
logFlag = 0

if _platform == "linux" or _platform == "linux2":
	pass
elif _platform == "darwin":
	pass
elif _platform == "win32":
	# print("Platform:", _platform)
	colorFlag = 1

def set_color(color, handle=std_out_handle):
    """(color) -> BOOL
    
    Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    """
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool
def colorRed():
	if colorFlag==1:
		set_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
def colorGreen():
	if colorFlag==1:
		set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
def colorBlue():
	if colorFlag==1:
		set_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
def yellowOnBlue():
	if colorFlag==1:
		set_color(BACKGROUND_BLUE|FOREGROUND_GREEN|FOREGROUND_RED|FOREGROUND_INTENSITY)
def colorYellow():
	if colorFlag==1:
		set_color(FOREGROUND_RED|FOREGROUND_GREEN|FOREGROUND_INTENSITY)


class UserInterface():
	"""Asks user to input scenario file and methods file"""
	def __init__(self):
		colorGreen()
		self.scFileChoice=input('Please enter name of scenario file: ')
		self.parsArgs(self.scFileChoice)
		self.tagChoice=input('Please enter any tags separated by blank space: ')

	def parsArgs(self, fileChoice):
		try:
			f=open(fileChoice, 'r')
		except:
			colorRed()
			print("ERROR: Unable to locate file named {0} in current directory".format(fileChoice))
			colorGreen()
			sys.exit()
		self.textOfFile=f.read()
		try:
			m=open('methods.py', 'r')
		except:
			colorRed()
			print("ERROR: Unable to locate file 'methods.py' in current directory")
			colorGreen()
			sys.exit()
		self.textOfMethods=m.read()
		try:
			h=open('testheader.py', 'r')
		except:
			colorRed()
			print("ERROR: Unable to locate file 'testheader.py' in current directory. \n You now must invoke an instance of your browser in every method definition.")
			colorGreen()
			sys.exit()
		self.header=h.read()



class testSuite():
	"""Entire test suite"""

	def __init__(self):
		self.interface = UserInterface()
		self.allScenariosList = self.parseScenarios(self.interface.textOfFile)
		self.allMethodsList = self.formCodeStr(self.interface.textOfMethods)
		self.tagchoice = self.interface.tagChoice
		# self.header = """#! usr/bin/env python\nimport time\nfrom selenium import webdriver """
		self.header = self.interface.header
		self.totalScCount=str(len(self.allScenariosList))
		self.executedScCount=0
		self.successCount=0
		self.failedScenarios=[]
		self.headerfooter = self.parseHeader(self.header)
		self.logfilename='sessionlog-'+time.strftime('%d%b%Y-%H-%M-%S')+'.log' #day, month name, year, hour, minutes, seconds
		if logFlag ==1:
			self.log=open(self.logfilename, 'a')

	def parseHeader(self, headerfile):
		"""Parses the testheader.py file and separates the contents of Before: and After: sections
			to be added later"""

		before = headerfile[0:headerfile.index('After')]
		before = before.replace('Before:\n', '')
		after = headerfile[headerfile.index('After'):]
		after = after.replace('After:\n', '')
		return (before, after)


	def parseScenarios(self, scenarios):

		"""Takes the scenario file text, changes incorrect spelling of 'scenario' to correct,
		then splits the text into list where every elementi is similar to:

		ScenarioName @tag1 @tag2 
		Do something
		Do something else

		INPUT: string
		OUTPUT: list
		"""

			#---changing possibly incorrectly spelled 'Scenario:' into proper form for later splitting

		wrongWords=['Scenario:','\nScenario','\nscenario', '\nscenario:', '\nsenario', '\nSenario:',
			'\nSenario', '\nsenario:']
		for word in wrongWords:
			if word in scenarios:
				scenarios=scenarios.replace(word, '\nScenario:')

		#---Splitting into individual scenarios
		scenarios=scenarios.replace(':','') #removing the ':'sign
		if '\t' in scenarios:
			scenarios=scenarios.replace('\t','') #removing tabs
		scList=scenarios.split('\nScenario')
		for i in range(0,len(scList)):
			scList[i]=scList[i].strip(' \n')
		if '' in scList:
			scList.remove('')

		return scList		

	def formCodeStr (self, filestring):
		"""Takes a python source file as one big string and returns a list of strings
		each of which is a separate function definition
		INPUT: the entire methds file as string
		OUTPUT: list of function definitions """

		chunks = filestring.split('\ndef')
		codeStrings=[]
		for i in range(0, len(chunks)):
			if i>0:
				codeStrings.append('def'+ ' zxfname'+chunks[i])
			if i==0:
				chunks[i] = chunks[i].replace('def','')
				codeStrings.append('def'+' zxfname'+chunks[i])

		return codeStrings

		
	def doTest(self, tagchoice):
		if '@' not in tagchoice:
			self.testAll()
		else:
			self.testByTag(self.allScenariosList,tagchoice)

	def testAll(self):
		toprint = 'EXECUTING ALL TESTS WITHOUT TAGS...'
		self.output(toprint)
		self.executor(self.allScenariosList)

	def output(self, *arguments):
		print(''.join(arguments))
		if logFlag == 1:
			sys.stdout = self.log
			print(''.join(arguments))
			sys.stdout = sys.__stdout__


	def executor(self, listOfScenarios):
		for eachScenario in listOfScenarios:
			scList=eachScenario.split('\n')
			scName=scList[0][0:scList[0].index('@')-1]
			colorBlue()
			self.output('=================================================')
			#print('=================================================')
			colorGreen()
			self.output('Executing Scenario Named: ', scName)
			
			del scList[0]
			try:
				self.executedScCount += 1
				self.execScenario(scList)
				
			except Exception:

				errmessage = 'TEST FAILED for scenario {0}: \n'.format(scName)
				
				colorRed()
				self.output(errmessage)
				#print(errmessage)
				colorGreen()
				colorYellow()

				exc_type, exc_value, exc_traceback=sys.exc_info()
				#change the 'limit' attribute of the following function to 0 or some integer to get the number of traceback lines desired
				# choosing 0 will give you just the type and value of error, no traceback
				traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None) 
				colorGreen()
				# traceList = traceback.extract_tb(exc_traceback, limit=None)
				# traceString = '\n'.join(traceList)
				# self.output(str(exc_type), str(exc_value), traceString)
				if logFlag ==1:
					sys.stderr = self.log
					traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None)
					sys.stderr = sys.__stderr__
				#print(' Traceback:\n')
				#traceback.print_exc()#(sys.exc_info()[2], limit=1, file=sys.stdout)
				self.failedScenarios.append(scName)

				continue
		
		yellowOnBlue()

		self.output('TEST STATISTICS')

		colorGreen()
		testspassed = '\n    '+ str(self.executedScCount-len(self.failedScenarios))+ ' tests PASSED'
		self.output(testspassed)
		testsfailed = '    '+ str(len(self.failedScenarios))+' tests FAILED'
		self.output(testsfailed)

		yellowOnBlue()
		self.output('FAILED TESTS:')
		colorGreen()

		for i in self.failedScenarios:
			self.output('    ', i)
		self.output('\n')

		

	def testByTag(self, scenariosList, tagchoice):
		"""Handles testing with tags. 
		INPUT: list, string
		OUTPUT: ordering test execution
		"""

		testDict=self.scenByTag(scenariosList, tagchoice) #get the list of tests by tag name
		for tagName,value in testDict.items():
			self.output('\nEXECUTING TESTS MARKED WITH TAG: ', tagName, '\n')
			self.executor(value)

	#========================================================================================================
	def scenByTag(self, scenariosList, tagchoice):
		"""From list of scenarios and tag choice, this creates a dictionary where every elements value is a
			list of scenarios by tag specified in tagchoice.
			INPUT: list, string
			OUTPUT: dictionary

			"""

		tagchoicelist=tagchoice.split()
		tempscdict={}
		for eachTag in tagchoicelist:
			scForTag=[]
			if eachTag != ' ':
				for eachScenario in scenariosList:
					if eachTag in eachScenario:
						scForTag.append(eachScenario)
			tempscdict[eachTag]=scForTag

		return tempscdict

	def compose(self, cases, methods):

		"""Composes code for a scenario"""

		methodList=[]

		
		for eachCase in cases:

			sigTestCase = eachCase.split()
			
			for eachMethod in methods:
				# toAdd=compSignature(eachCase, eachMethod) 
				toAdd=compSig(eachCase, eachMethod)
				newMethodList = []
				methodConst = toAdd[1]
				methodConst[0]=methodConst[0].capitalize()
				sigMethod=getArgList(eachMethod)


				if toAdd[0]==True and sigTestCase != getArgList(eachMethod):
					# since the program got to this point, both method and testcase have same number of constants in same sequence

					for eachWord in sigTestCase:

						if eachWord in methodConst:
							newMethodList.append(eachWord)

							#creates next list element so that it can be modified if the follwing element is not a constant

							if len(newMethodList)<len(sigMethod):  #this prevents list out of bounds error
								if sigTestCase[len(newMethodList)] not in methodConst:
									newMethodList.append('')

						elif len(newMethodList)<=len(sigMethod) and eachWord not in methodConst: 
							newMethodList[len(newMethodList)-1] = newMethodList[len(newMethodList)-1]+' '+eachWord
							newMethodList[len(newMethodList)-1] = newMethodList[len(newMethodList)-1].strip() #removing leading space
					
					# print('NEW METHOD LIST: ', newMethodList)
					newSigArr=[]
					
					funcName=''.join(sigMethod)
					funcName=funcName.replace('^','')
					
					for i in range(0,len(sigMethod)):
						if '^' in sigMethod[i]:
							sigMethod[i]=sigMethod[i].replace('^','')
							sigMethod[i]= sigMethod[i]+'='+'"'+newMethodList[i]+'"'
							newSigArr.append(sigMethod[i])

					newSig = ','.join(newSigArr)
					finalmethod=finalizeMethod(newSig, eachMethod, funcName)
					finalmethod=finalmethod.strip()
					methodList.append(finalmethod)
					
					# print('FINAL METHOD: \n', finalmethod)

				elif toAdd[0]==True and sigTestCase == sigMethod:
					funcName=''.join(sigMethod)
					finalmethod = finalizeMethod('', eachMethod, funcName)
					methodList.append(finalmethod)
					# if len(methodList)<len(cases):
					# 	error = "colorRed() \nprint('NOT ALL CASES HAVE MATCHING METHODS. CANNOT RUN SCENARIO')\ncolorGreen()"
					# 	return error
					# print('FINAL METHOD IF EQUAL: \n', finalmethod)

		if len(methodList)<len(cases):
			raise Exception('NOT ALL CASES HAVE MATCHING METHODS. CANNOT RUN SCENARIO')
			if logFlag==1:
				sys.stdout = self.log
				print("NOT ALL CASES HAVE MATCHING METHODS. CANNOT RUN SCENARIO") 
				sys.stdout = sys.__stdout__
			

		allmethods='\n'.join(methodList)
		return allmethods

	def execScenario(self, scenario):

		"""Collects and executes generated scenario code"""

		preFinalCode=self.compose(scenario, self.allMethodsList)
		finCode = finishComposing(preFinalCode, self.headerfooter[0], self.headerfooter[1])
		#uncomment the following, re-save this file, and run again to see generated code in command line console
		#print(finCode)

		exec(finCode, globals())


def getArgList(code):
	"""Takes source code as text for of each function and returns list from string between 
	the function's parameter parentheses"""

	argStr=code[code.index('(')+1:code.index(')')]
	if ',' in argStr:
		argStr=argStr.replace(',', ' ')

	argList=argStr.split()
	return argList


def compSig(testcase, method):

	"""Compares test case name with methods.py file methods based on exact match and sequence of non-variables.
	Set a permission for compose function to add individual method code"""

	sigTestCase = testcase.split()

	sigMethod = getArgList(method)
	if sigTestCase==sigMethod:
		return (True, sigMethod)

	methodConst = []
	caseConst = []
	sigMethod[0]=sigMethod[0].lower()
	sigTestCase[0] = sigTestCase[0].lower()

	for eachItem in sigMethod: #building a sequence of constants (non-variables) for the method
		if '^' not in eachItem:
			methodConst.append(eachItem)

# all constants from method must be present in the test case in the same sequence as in method. 
	for eachWord in sigTestCase: 
		if eachWord in methodConst:
			caseConst.append(eachWord)

# comparing testcase and method constant sequences. Must be equal or returns False
	if caseConst != methodConst: # cheking
		return (False, methodConst)
	else:
		if '^'in ''.join(sigMethod):
			return (True, methodConst)
		else:
			return (False, methodConst)


def finalizeMethod(signature, method, funcname):
	"""Inserts function name, puts together each method for the compose function"""

	sigMethod=getArgList(method)
	sigString=' '.join(sigMethod)
	method=method.replace('zxfname', funcname)
	method=method[0:method.index('(')].replace('^', '')+method[method.index('('):len(method)]
	method=method.replace(sigString, signature)
	method = method + '\n'+funcname.replace('^', '') +'()'
	return method


def finishComposing(allmethods, header, footer):
	"""Adds a header to each scenario code"""
	finalcode= header+'\n'+allmethods+'\n'+footer
	return finalcode

def main():
	if len(sys.argv)==1:  #this means only the filename is in the sys.argv list
		t = testSuite()
		t.doTest(t.tagchoice)
		
		
	elif sys.argv[1]=='makelog':
		print('LOG WILL BE CREATED')
		global logFlag 
		logFlag = 1
		t = testSuite()
		t.doTest(t.tagchoice)
		t.log.close()



if __name__=="__main__":
	main()

#--This is the old signature comparison function that compares items one for one without multi-word arguments

# def compSignature(testcase, method):
# 	"""Compares signatures of methods and scenario"""

# 	sigTestCase = testcase.split()
# 	sigMethod=getArgList(method)
	
# 	if len(sigTestCase)!= len(sigMethod):
# 		return False

# 	if sigTestCase==sigMethod:
# 		return True
# 	else:
		
# 		for i in range(0,len(sigMethod)):

# 			if sigMethod[i]==sigTestCase[i]:
# 				continue

# 			if '^' in sigMethod[i]:
# 				continue

# 			if '^' not in sigMethod[i]:
# 				return False

# 		return True

#--THIS IS THE OLD COMPOSE FUNCTION  THAT WORKS WITH OLD compareSignature function 
# def compose(cases, methods):

# 	methodList=[]
	
# 	for eachCase in cases:

# 		for eachMethod in methods:
# 			toAdd=compSignature(eachCase, eachMethod)

# 			if toAdd==True:
# 				newSigArr=[]
# 				sigMethod=getArgList(eachMethod)
# 				funcName=''.join(sigMethod)
# 				sigTestCase = eachCase.split()
# 				for i in range(0,len(sigMethod)):
# 					if '^' in sigMethod[i]:
# 						sigMethod[i]=sigMethod[i].replace('^','')
# 						sigMethod[i]= sigMethod[i]+'='+'"'+sigTestCase[i]+'"'
# 						newSigArr.append(sigMethod[i])

# 				newSig = ','.join(newSigArr)
# 				finalmethod=finalizeMethod(newSig, eachMethod, funcName)
# 				methodList.append(finalmethod)

# 	allmethods='\n'.join(methodList)
# 	return allmethods
