
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self,driver):
        self.driver=driver
        self.wait=WebDriverWait(driver,10)

    def click_element(self,locator):
        element=self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def input_text(self,locator,text):
        element=self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_element_text(self,locator):
        element=self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def find_elements(self,locator):
         self.wait.until(EC.presence_of_element_located(locator))
         return self.driver.find_elements(*locator)

