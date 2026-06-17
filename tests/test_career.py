from pages.career_page import CareerPage

def test_career_filters(driver):
    career_page=CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()

    career_page.open_regions()
    career_page.select_item_with_scroll("מרכז")
    career_page.open_regions()

    career_page.open_areas()
    career_page.select_item_with_scroll("כספים")
    career_page.open_areas()

    career_page.open_subfields()
    career_page.select_item_with_scroll("עוזר חשב מתחיל")
    career_page.open_subfields()

    career_page.enter_search_text("כלכלה")
    career_page.click_search()

    assert career_page.cards_list_visible() > 0

def test_career_regions_only_center(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()

    career_page.open_regions()
    career_page.select_item_with_scroll("מרכז")
    career_page.click_search()
    assert career_page.check_text_in_all_results("מרכז") ==True

def test_career_search_no_results(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()
    career_page.enter_search_text("qwerty")
    career_page.click_search()

    error_text=career_page.get_no_results_text()
    assert "לא נמצא" in error_text

    career_page.click_all_jobs_link()
    assert "user_page=1&freeText=gvgvxfgf" not in driver.current_url

def test_career_search_special_characters(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()
    career_page.enter_search_text("@#$%^&*()")
    career_page.click_search()

    error_text=career_page.get_no_results_text()
    assert "לא נמצא" in error_text

def test_empty_career_search(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()
    career_page.enter_search_text("   ")
    career_page.click_search()

    assert career_page.cards_list_visible() > 0

def test_long_conversational_search(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()
    career_page.enter_search_text("אני רוצה משהו שקשור למחשבים ואפשר לעבוד מהבית כמה פעמים בשבוע")
    career_page.click_search()

    error_text = career_page.get_no_results_text()
    assert "לא נמצא" in error_text


def test_input_search_hebrew_keyword(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()
    career_page.close_cookie_banner()
    search_word="מרכז"
    career_page.enter_search_text("מרכז")
    career_page.click_search()

    assert career_page.cards_list_visible()>0

def test_career_search_english_keyword(driver):
    career_page = CareerPage(driver)
    driver.get("https://www.strauss-group.co.il/career/")
    driver.maximize_window()

    career_page.close_cookie_banner()











































