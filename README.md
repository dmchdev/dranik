# dranik
Dranik is a Python testing tool like Cucumber

It is not only for Selenium. Being a code generator, Dranik allows testing of python code, as long as you format things properly. That said, it was designed during my work testing UI with Selenium WebDriver.

Please see the scenarios.txt file and methods.py file for how to format your scenarios and methods. Please note that, although the name of the scenario file is optional (it can be 'myscen' instead of 'scenarios'), as well as its extension (as long as it is essentially a plain text file like .txt or .py), the methods file MUST be called 'methods.py'. If you wish to modify that name, you would need to modify in the the program's source code itself. This is discouraged for the sake of uniformity. 

^x or ^y denotes a variable. Any number of variables is allowed. Make sure there are some non-variable words between variables. The test case--method matching engine will insert whatever it determines to be the appropriate variable. Please note that all variables are passed in as string values, so be sure to perform any necessary type conversions in your methods. 

If you wish to create a log, specify option 'makelog' (without quotes) when you launch Dranik.

For example: C:> python dranik.py makelog

Your log will be generated from the date/time you ran this instance of Dranik, to the second, so it's always going to be unique and easy to find by time executed. 

When you mark your scenarios with tags, multiple tags are allowed, just separate them with a space and keep in the same line.

To execute specific tags, enter the tag names separated with space when prompted such as @tagName. No spaces are allowed within tag names! Tag names such as '@My Tag' are illegal and will prevent test execution.

If you speficy tag name that doesn't exist, no tests will be executed for that tag. If it's the only tag you specified, no tests will be executed at all (so please specify existing tags to avoid confusion)

Please note that Dranik is a work in progress. Your input is welcome and forking is encouraged. 

KNOWN BUGS: sometimes Selenium stalls in an endless loop and so does the script. I am working on the problem. The timeout feature will be there asap.
