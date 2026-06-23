import pytest
from selenium import webdriver
import allure


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                web_driver = item.funcargs["driver"]

                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="failed_test_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"ERROR,Failed to capture a screenshot for Allure: {e}")