import csv


class DataExporter:
    @staticmethod
    def save_to_csv(data, csv_file_path):
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["txt_fund_compare1", "txt_fund_compare2", "percentage of common stocks"])
            csv_writer.writerows(data)
        print(f"CSV file created: {csv_file_path}")
