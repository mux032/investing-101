from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class DataAggregator:
    def __init__(self, webdriver_path):
        self.webdriver_path = webdriver_path
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--webdriver-path={self.webdriver_path}')
        return webdriver.Chrome(options=chrome_options)

    def load_website(self, website_url):
        self.driver.get(website_url)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def select_option_from_dropdown(self, dropdown_id, option_value):
        dropdown_element = self.driver.find_element(By.ID, dropdown_id)
        dropdown = Select(dropdown_element)
        dropdown.select_by_value(option_value)

    def select_all_types_of_funds(self):
        modal_locator = (By.ID, 'sel_schemeCategories')
        self.wait_for_element(modal_locator)
        self.select_option_from_dropdown('sel_schemeCategories', 'All')

    def clear_form_data(self, form_data):
        for field, value in form_data.items():
            if "txt_fund" in field:  # Skip clearing dropdown fields
                locator = (By.ID, field)
                self.driver.find_element(*locator).clear()

    def fill_form_data(self, form_data):
        for field, value in form_data.items():
            locator = (By.ID, field)
            self.driver.find_element(*locator).send_keys(value)

    def click_submit_button(self, submit_button_locator, timeout=10):
        submit_button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(submit_button_locator)
        )
        submit_button.click()

    def extract_data(self):
        try:
            common_stocks = int(self.driver.find_element(By.ID, 'span_common_stocks').text)
            uncommon_stocks_scheme1 = int(self.driver.find_element(By.ID, 'span_uncommon_stocks_scheme1').text)
            uncommon_stocks_scheme2 = int(self.driver.find_element(By.ID, 'span_uncommon_stocks_scheme2').text)
        except (ValueError, NoSuchElementException):
            return None
        return StockHoldings(common_stocks, uncommon_stocks_scheme1, uncommon_stocks_scheme2)

    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except TimeoutException:
            print("Page loading timed out. Refreshing the page.")
            self.driver.refresh()
            self.wait_for_page_load()

    def compare_funds(self, fund1, fund2):
        form_data = {"txt_fund_compare1": fund1, "txt_fund_compare2": fund2}
        self.clear_form_data(form_data)
        self.fill_form_data(form_data)
        submit_button_locator = (By.XPATH, '//a[@class="btn btn-warning mutual-funds-submit-anchor btn-orange"]')
        self.click_submit_button(submit_button_locator)
        self.wait_for_page_load()
        return self.extract_data()

    def quit_driver(self):
        self.driver.quit()


class StockHoldings:
    def __init__(self, common_stocks, uncommon_stocks_first_fund, uncommon_stocks_second_fund):
        self.common_stocks = common_stocks
        self.uncommon_stocks_first_fund = uncommon_stocks_first_fund
        self.uncommon_stocks_second_fund = uncommon_stocks_second_fund
