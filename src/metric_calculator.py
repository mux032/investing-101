from src.data_aggregator import StockHoldings


class MetricCalculator:
    @staticmethod
    def calculate_percentage_of_common_holdings(stock_holdings: StockHoldings):
        total_common_stocks = stock_holdings.common_stocks * 2
        combined_stocks_of_two_funds = (stock_holdings.uncommon_stocks_first_fund +
                                        stock_holdings.uncommon_stocks_second_fund + total_common_stocks)
        return (total_common_stocks / combined_stocks_of_two_funds) * 100
