import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

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
    dropdown_menu=(By.XPATH, "//ul[contains(@class, 'jobs_index_dropdown')]")
    clear_all_filters=(By.ID,"order_form_reset")
    job_counter_number=(By.CSS_SELECTOR,"span[data-show='total_orders']")

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
        self.wait.until(EC.invisibility_of_element_located(self.dropdown_menu))
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

    def check_text_matches_any_expected(self, expected_list):
        cards = self.find_elements(self.job_cards)
        if not cards:
            return False

        real_cards_checked = 0

        for card in cards:
            card_text = card.text.strip()
            has_letters = bool(re.search(r'[א-תa-zA-Z]', card_text))

            if not card.is_displayed() or not card_text or len(card_text) < 20 or not has_letters:
                continue

            real_cards_checked += 1

            match_found = any(region in card_text for region in expected_list) or "ארצי" in card_text

            if not match_found:
                print(f"\n=== AN UNEXPECTED CARD FOUND ===")
                print(card_text)
                print(f"Something from this list was expected: {expected_list}")
                print("===============================\n")
                return False

        if real_cards_checked == 0:
            print("\n The test filtered everything and didn't find a single real vacancy!")
            return False

        return True

    def click_clear_filters(self):
        self.click_element(self.clear_all_filters)

    def get_jobs_count(self):
        try:
            count_text=self.get_element_text(self.job_counter_number)
            return int(count_text.strip()) if count_text.strip().isdigit() else 0
        except:
            return 0













