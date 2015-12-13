def (Open Food Network main page):
	driver.get('http://www.foodnetwork.com')
	handleAlert()
	#time.sleep(3)

def (Select ^x from header menu):
	handleAlert()
	element = driver.find_element_by_xpath("//ul//span[contains(text(), '{0}')]".format(x))
	element.click()
	#time.sleep(3)
	

def(Select first item from category ^x):
	handleAlert()
	try:
		element = driver.find_element_by_xpath("//header[@class='hr']/h5[contains(text(),'{0}')]/../following-sibling::div[@class='tab-content'][1]//ul[@class='slat section'][1]//div[@class='group'][1]/h6[1]/a".format(x))
	except Exception:
		element = driver.find_element_by_xpath("//header[@class='hr']/h5[contains(text(),'{0}')]/../following-sibling::div[@class='tab-content'][1]//ul[@class='slat section'][1]//div[@class='group'][1]/h6[1]/a".format(x))
	element.click()