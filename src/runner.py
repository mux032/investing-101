import traceback
from itertools import combinations
from src.data_aggregator import DataAggregator
from src.data_exporter import DataExporter
from src.metric_calculator import MetricCalculator


class Runner:

    def __init__(self, config):
        self.website_url = config.website_url
        self.webdriver_path = config.webdriver_path
        self.funds_file_path = config.funds_list_file_path
        self.output_file_path = config.output_file_path

    def read_fund_list(self):
        with open(self.funds_file_path, 'r') as file:
            return [line.strip() for line in file]

    def run(self):
        scraper = DataAggregator(self.webdriver_path)

        try:
            scraper.load_website(self.website_url)
            scraper.select_all_types_of_funds()

            all_data = []
            fund_list = self.read_fund_list()

            for pair in list(combinations(fund_list, 2)):
                retries = 3
                while retries > 0:
                    try:
                        stock_holdings = scraper.compare_funds(pair[0], pair[1])
                        common_stocks_percentage = MetricCalculator.calculate_percentage_of_common_holdings(
                            stock_holdings)
                        if common_stocks_percentage is not None:
                            all_data.append([pair[0], pair[1], common_stocks_percentage])
                            break
                        else:
                            print(f"Error comparing funds: {pair[0]}, {pair[1]}")
                            retries -= 1
                    except Exception as e:
                        print(f"Error: {e}")
                        print(traceback.format_exc())
                        retries -= 1

            DataExporter.save_to_csv(all_data, self.output_file_path)

        finally:
            scraper.quit_driver()
