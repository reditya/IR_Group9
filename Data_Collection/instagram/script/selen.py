from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/usr/local/bin/geckodriver')

driver = webdriver.Firefox(firefox_binary=binary)
url = "https://www.instagram.com/explore/locations/1006877751/?__a=1&max_id="
geturl = driver.get(url)
print geturl
