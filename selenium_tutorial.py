import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# https://www.selenium.dev/documentation/webdriver/getting_started/first_script/

# (1) start session
driver = webdriver.Chrome()

# (2) take action on browser
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# (3) request browser info
# https://www.selenium.dev/documentation/webdriver/interactions/
title = driver.title

# (4) establish waiting strategy
driver.implicitly_wait(0.5)  # purpose: wait for page to load its elements (implicit wait isn't the greatest solution)

# (5) find an element
# https://www.selenium.dev/documentation/webdriver/elements/
text_box = driver.find_element(by=By.NAME, value="my-text")
# By.NAME refers to the name of an HTML element
# e.g. <input type="text" name="my-text">

submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# (6) take action on an element
# https://www.selenium.dev/documentation/webdriver/elements/interactions/
text_box.send_keys("Selenium")  # typing the string into the element
submit_button.click()

# (7) request element information
message = driver.find_element(by=By.ID, value="message")  # gets the text of an element
text = message.text
print(text)

# (8) end session
driver.quit()
