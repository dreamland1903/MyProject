from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC

from tests.conftest import driver


class CareerPage(BasePage):
    cookie_close_button=(By.ID,"cookie_msg_close")
    region_button=(By.XPATH,'//button[@data-default="איזורים"]' )
    areas_button=(By.XPATH,'//button[@data-default="תחומים"]')
    sub_fields_button = (By.XPATH, '//button[@data-default="תתי תחומים"]')
    search_input=(By.ID,"freeText")
    search_button=(By.CSS_SELECTOR,"button.submit_search.green_btn")
    no_results_message = (By.ID, "no_jobs_found_title")
    all_jobs_link=(By.LINK_TEXT,"לכל המשרות")
    job_cards = (By.XPATH, "//div[@id='jobs_list']/div[contains(@class, 'jobs_list_order_wrap')]")

    item_in_open_dropdown_xpath = "//ul[contains(@class, 'jobs_index_dropdown')]//*[text()='{0}' or contains(text(), '{0}')]"

    def __init__(self,driver):
        super().__init__(driver)

    def close_cookie_banner(self):
        self.click_element(self.cookie_close_button)

    def open_regions(self):
        self.click_element(self.region_button)

    def open_areas(self):
        self.click_element(self.areas_button)

    def open_subfields(self):
        self.click_element(self.sub_fields_button)

    def enter_search_text(self,text):
        self.input_text(self.search_input,text)

    def click_search(self):
        self.click_element(self.search_button)

    def select_item_with_scroll(self, item_name):
        xpath=self.item_in_open_dropdown_xpath.format(item_name)
        target_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)   #Java
        target_element.click()

    def get_no_results_text(self):
        return self.get_element_text(self.no_results_message)

    def click_all_jobs_link(self):
        self.click_element(self.all_jobs_link)

    def cards_list_visible(self):
        try:
            cards = self.find_elements(self.job_cards)
            return len(cards)
        except:
            return 0

    def check_text_in_all_results(self,expected_text):
        cards= self.find_elements(self.job_cards)
        if not cards:
            return False
        for card in cards:
            card_text=card.text.strip()
            if not card_text:
                continue
            if expected_text not in card_text and "ארצי" not in card_text:
                print("\n=== AN UNEXPECTED CARD FOUND ===")
                print(card.text)
                print("====================================\n")
                return False
        return True








