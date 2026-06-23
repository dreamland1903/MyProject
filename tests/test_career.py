import time
import pytest
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.career_page import CareerPage


@allure.epic("QA Automation Final Project")
@allure.feature("Job Search and Filtering Module")
class TestStraussCareer:

    @allure.story("Apply combined complex filters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_career_filters(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Select 'Center' region (מרכז)"):
            career_page.open_regions()
            career_page.select_item_with_scroll("מרכז")
            career_page.open_regions()

        with allure.step("3. Select 'Finance' area (כספים)"):
            career_page.open_areas()
            career_page.select_item_with_scroll("כספים")
            career_page.open_areas()

        with allure.step("4. Select profession 'Junior Assistant Controller' (עוזר חשב מתחיל)"):
            career_page.open_subfields()
            career_page.select_item_with_scroll("עוזר חשב מתחיל")
            career_page.open_subfields()

        with allure.step("5. Enter text 'Economics' (כלכלה) and trigger search"):
            career_page.enter_search_text("כלכלה")
            career_page.click_search()

        with allure.step("6. Verify that job cards are visible"):
            assert career_page.cards_list_visible() > 0

    @allure.story("Filter jobs by single region")
    @allure.severity(allure.severity_level.NORMAL)
    def test_career_regions_only_center(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Filter by 'Center' region (מרכז) and search"):
            career_page.open_regions()
            career_page.select_item_with_scroll("מרכז")
            career_page.click_search()

        with allure.step("3. Verify all results contain 'Center' text"):
            assert career_page.check_text_in_all_results("מרכז") is True

    @allure.story("Filter jobs by multiple regions combined")
    @allure.severity(allure.severity_level.NORMAL)
    def test_career_multiple_regions_combined(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Select and apply 'Center' region (מרכז)"):
            career_page.open_regions()
            career_page.select_item_with_scroll("מרכז")
            career_page.open_regions()
            career_page.click_search()

        with allure.step("3. Select and apply 'North' region (צפון)"):
            career_page.open_regions()
            career_page.select_item_with_scroll("צפון")
            career_page.open_regions()
            career_page.click_search()

        with allure.step("4. Verify results match any of the allowed regions"):
            allowed_region = ["מרכז", "ארצי", "צפון"]
            assert career_page.check_text_matches_any_expected(allowed_region) is True

    @allure.story("Search with keyword that yields no results")
    @allure.severity(allure.severity_level.MINOR)
    def test_career_search_no_results(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Search for invalid keyword 'qwerty'"):
            career_page.enter_search_text("qwerty")
            career_page.click_search()

        with allure.step("3. Verify 'No results found' error message appears"):
            error_text = career_page.get_no_results_text()
            assert "לא נמצא" in error_text

        with allure.step("4. Click 'All Jobs' link and verify URL reset state"):
            career_page.click_all_jobs_link()
            assert "user_page=1&freeText=gvgvxfgf" not in driver.current_url

    @allure.story("Search using special characters")
    @allure.severity(allure.severity_level.MINOR)
    def test_career_search_special_characters(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Search for special symbols string"):
            career_page.enter_search_text("@#$%^&*()")
            career_page.click_search()

        with allure.step("3. Verify error message appears"):
            error_text = career_page.get_no_results_text()
            assert "לא נמצא" in error_text

    @allure.story("Search with empty spaces")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_career_search(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Input empty spaces into search field"):
            career_page.enter_search_text("   ")
            career_page.click_search()

        with allure.step("3. Verify that standard job cards list is still displayed"):
            assert career_page.cards_list_visible() > 0

    @allure.story("Search using long conversational sentences")
    @allure.severity(allure.severity_level.MINOR)
    def test_long_conversational_search(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Search with a long conversational sentence"):
            career_page.enter_search_text("אני רוצה משהו שקשור למחשבים ואפשר לעבוד מהבית כמה פעמים בשבוע")
            career_page.click_search()

        with allure.step("3. Verify that system handles long queries by showing no results message"):
            error_text = career_page.get_no_results_text()
            assert "לא נמצא" in error_text

    @allure.story("Search using a valid Hebrew keyword")
    @allure.severity(allure.severity_level.NORMAL)
    def test_input_search_hebrew_keyword(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to career page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Search for keyword 'Center' (מרכז)"):
            career_page.enter_search_text("מרכז")
            career_page.click_search()

        with allure.step("3. Verify relevant job results are returned"):
            assert career_page.cards_list_visible() > 0

    @allure.story("Verify resetting active region filters back to initial counts")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_clear_search_filters(self, driver):
        career_page = CareerPage(driver)

        with allure.step("1. Navigate to Strauss Group careers page"):
            driver.get("https://www.strauss-group.co.il/career/")
            career_page.close_cookie_banner()

        with allure.step("2. Fetch total active available jobs count"):
            career_page.click_search()
            WebDriverWait(driver, 10).until(lambda d: career_page.get_jobs_count() > 0)
            initial_count = career_page.get_jobs_count()
            print(f"\n[INFO] Initial jobs count: {initial_count}")
            assert initial_count > 0, "Error: Initial jobs count should be greater than 0!"

        with allure.step("3. Select 'Center' region (מרכז) from dropdown filters"):
            career_page.open_regions()
            career_page.select_item_with_scroll("מרכז")
            career_page.open_regions()
            career_page.click_search()

        with allure.step("4. Wait for counter decrease verification"):
            WebDriverWait(driver, 10).until_not(
                EC.text_to_be_present_in_element(career_page.job_counter_number, str(initial_count))
            )
            time.sleep(2)
            filtered_count = career_page.get_jobs_count()
            print(f"[INFO] Jobs count after filtering: {filtered_count}")
            assert 0 < filtered_count < initial_count, "Error: Filter count did not decrease properly!"

        with allure.step("5. Click clear filters button and refresh"):
            career_page.click_clear_filters()
            time.sleep(1)
            career_page.click_search()

        with allure.step("6. Confirm counter value successfully returned to initial amount"):
            WebDriverWait(driver, 10).until(lambda d: career_page.get_jobs_count() == initial_count)
            final_count = career_page.get_jobs_count()
            print(f"[INFO] Jobs after clearing filters: {final_count}")
            assert final_count == initial_count, f"Reset failed! Expected {initial_count}, but got {final_count}"












































