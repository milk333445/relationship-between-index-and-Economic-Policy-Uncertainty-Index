from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://www.google.com")
element = driver.find_element_by_class_name('gLFyf.gsfi')
element.send_keys('Selenium Python')
button = driver.find_element_by_class_name('gNO89b')
button.click()