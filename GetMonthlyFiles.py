from datetime import datetime
import csv, gspread, requests, time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GetFiles():
    def __init__(self):
        self.__initial_msg()
        #https://red-hat-l10n.pages.redhat.com/CLinfra-reports/2023/07/daily_source_updates_ja_2023-07-07.csv
        #https://red-hat-l10n.pages.redhat.com/CLinfra-reports/2023/09/monthly_docs_localization_report_ja_2023-09.csv

        self.__base_url = "https://red-hat-l10n.pages.redhat.com/CLinfra-reports/"
        #self.__test_url = "https://red-hat-l10n.pages.redhat.com/CLinfra-reports/2023/07/daily_source_updates_ja_2023-07-07.csv"
        self.__sheet_name = "monthly_docs_localization_report_ja_"
        self.__extension = ".csv"
        self.__date = datetime.today().strftime("%Y-%m-%d")
        self.__year = datetime.today().strftime("%Y")
        self.__month = datetime.today().strftime("%m")
        self.__day = datetime.today().strftime("%d")
        self.__runsheet_key = '1SU3myyfzFIirzRmR4Vo5uYbSR_vBCAzER0oE0_ENx0o'
        self.__credential = 'credential.json'
        self.__runsheet_sheet = 'Documentation'

        self.en_mfile = self.__date + "_en" + self.__extension
        self.jp_mfile = self.__date + "_jp" + self.__extension

        self.__monthly_en = self.__base_url + self.__year + "/" + self.__month + "/" + self.__sheet_name + self.__year + "-" + self.__month + self.__extension
        
        self.download_csv_from_gitlab() ## save file as 
        self.download_csv_from_jp_runsheet()
    
    def __initial_msg(self):
        msg = '.'
        print("Make sure you are connected to VPN...")
        for c in range(5):
            if c < 6:
                print(msg)
                time.sleep(1)
                msg += "."
        
        # Load the credentials from the JSON key file
    def download_csv_from_jp_runsheet(self):
        gc = gspread.service_account(filename=self.__credential)
        # Open the Japanese RunSheet
        spreadsheet = gc.open_by_key(self.__runsheet_key)
        # Get the first sheet in the spreadsheet
        worksheet = spreadsheet.worksheet(self.__runsheet_sheet)
        # Get all values from the sheet
        values = worksheet.get_all_values()
        data = values[1:]
        ##convert to csv format
        jp_data = '\n'.join([','.join(row) for row in data])
        with open(self.jp_mfile, 'w+', encoding='utf-8') as jp_file:
            jp_file.write(jp_data)

    def download_csv_from_gitlab(self):
        response = requests.get(self.__monthly_en, verify=False)
        response.raise_for_status()

        with open(self.en_mfile, 'w+') as en_file:
            en_file.write(response.text)
    
