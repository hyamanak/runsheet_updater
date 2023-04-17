import gspread, json, time
from datetime import datetime   

daily_update_file_id = ''
#source update file id
runsheet_id = ''
#spreadsheet id
key_file = ''
#json format bot key file

runsheet_worksheet = "Documentation"
update_worksheet = '0417'

date = datetime.today().strftime("%Y-%m-%d")

class GspreadObj():
    def __init__(self, spreadsheet_id, key_file, worksheet):
        self.date = date
        self.backup_tab_name = self.date + 'Backup'

        self.spreadsheet_id = spreadsheet_id

        self.key_file = key_file
        self.worksheet = worksheet

        self.worksheet_obj = self.get_worksheet_obj(spreadsheet_id, worksheet)

        self.data_dict = self.get_data_dict()

        self.data_list = self.get_data_list()

        self.nums_cols = self.set_nums_cols()
        self.nums_rows = self.set_nums_rows()

        #daily
        #['product0', 'version1', 'title2', 'Phrase project3', 'Phrase job4',
        #  'Total words5, 'Approx net words6', 'Hours estimated7', 'Hours used8',
        #  'Notes', 'Translator', '% filled from TM', 'Pantheon', 'en url', 'ja url']

        #runsheet 0, 1, 
        #'Categories', 'product', 'version', 'title', 'ja url', 'Phrase project', 'Phrase job',
        #  'Ver.', 'TEAM', 'Total words', 'Approx net words', 'Hours estimated', 'Quality', 'Hours used',
        #  'Translator', 'ComDate', 'Status', 'LastUpdate', '% filled from TM', 'Pantheon', 'en url', 'en date',
        #  '2614541'

    def backup_sheet(self):
        try:
            copy = self.get_worksheet_obj(self.spreadsheet_id, self.backup_tab_name)
            print('Worksheet ' + self.backup_tab_name + ' already exists, skipping backup.')

        except gspread.exceptions.WorksheetNotFound:
            self.worksheet_obj.duplicate(new_sheet_name=self.backup_tab_name, insert_sheet_index=4)
            print("Backup worksheet " + self.backup_tab_name + " has been created!")

    def set_nums_cols(self):
        self.cols = self.worksheet_obj.col_count
    
    def set_nums_rows(self):
        self.rows = self.worksheet_obj.row_count

    def get_worksheet_obj(self, spreadsheet_id, worksheet_id):
        gc = gspread.service_account(filename=self.key_file)
        sh = gc.open_by_key(spreadsheet_id) # or by sheet name: gc.open("TestList")
        return sh.worksheet(worksheet_id)   

    def get_data_dict(self) -> list:
        data = self.worksheet_obj.get_all_records()
        return [{**d, 'idx': i+2} for i, d in enumerate(data)]
    
    def get_data_list(self) -> list:
        return self.worksheet_obj.get_all_values()

class Updater():
    check_list = ['product', 'version', 'title', 'Phrase job']
    update_list = ['Total words', 'Approx net words', '% filled from TM', 'idx']
    update_dict = {'Total words': 10, 'Approx net words': 11, '% filled from TM' : 19}
    
    adjust_data_list = ['ComDate', 'Hours used', 'Translator', 'LastUpdate', 'Status']

    def __init__(self) -> None:
        self.daily_update_obj = GspreadObj(daily_update_file_id, key_file, update_worksheet)
        self.runsheet_obj = GspreadObj(runsheet_id, key_file, runsheet_worksheet)

        self.runsheet_data = self.runsheet_obj.data_dict
        self.daily_data = self.daily_update_obj.data_dict
        self.runsheet_list = self.runsheet_obj.data_list
        
        self.no_match_new_list = self.no_match_list()

        self.list_of_update = self.get_list_of_update()
        self.new_list = self.newlist_2b_updated()
        self.adjust_data() ## takes data from decoy, info to be updated, change status to UPD, remove tr name (if necessary), add last updated
        
    def row_match(self, daily_row, runsheet_row) -> bool:
        #takes each row to compare if they are the match
        return all(daily_row[item] == runsheet_row[item] for item in self.check_list)
    
    def get_info2update(self, daily_row) -> dict:
       #take daily_row and get info that to be inserted to runsheet row
       return {item: daily_row[item] for item in self.update_list}

    def newlist_2b_updated(self) -> list:
        ##returns new list that to be updated
        new_list = [] 
        for d_column in self.daily_data:
            del d_column['idx']
            for r_column in self.runsheet_data:
                if self.row_match(d_column, r_column):
                    new_list.append(self.update_column(d_column, r_column))
                if r_column['Status'] == "Done":
                    r_column = self.clearning_update(r_column)
                    new_list.append(r_column)
        return new_list
    
    def get_check_list_data(self, row_data):
        #check_list = ['product', 'version', 'title', 'Phrase job']
        return [str(row_data[item]) for item in self.check_list]

    def no_match_list(self):
        no_match_list = []
        matched_list = []

        for d_data in self.daily_data:
            d_list = self.get_check_list_data(d_data)
            #print(d_list)
            matched = False
            for r_data in self.runsheet_data:
                r_list = self.get_check_list_data(r_data)
                #print(r_list)
                if d_list == r_list:
                    matched = True
                    matched_list.append(d_list)
                    #print(d_list, r_list)

            if matched == False:
                no_match_list.append(d_list)
        return no_match_list

    def clearning_update(self, r_column):
        r_column['Status'] = ''
        r_column['Translator'] = ''
        r_column['Hours used'] = ''
        r_column['ComDate'] = ''
        return r_column

    def update_column(self, d_column, r_column):
        new_r_column = r_column
        new_r_column.update(d_column)
        return new_r_column

    def adjust_data(self) -> None:
        #takes data from decoy, info to be updated, change status to UPD, remove tr name (if necessary), add last updated
        for item in self.new_list:
            item['Status'] = 'UPD'
            item['LastUpdate'] = date
            item['version'] = str(item['version'])
    
    def update_cell(self) -> list:
        counter = 0
        for item in self.new_list:
            insert_item = [value for value in item.values()]
            insert_item_list = [insert_item[:-2]]
            
            s_idx = 'A'+ str(item['idx'])
            e_idx = 'W' + str(item['idx'])
            idx = s_idx + ':' + e_idx
            #print(insert_item_list)
            self.runsheet_obj.worksheet_obj.update(idx, insert_item_list)
            counter += 1
            if counter == 59:
                time.sleep(62)
                print("request limit exceeded, waiting for a minute...")
                counter = 0

    def get_list_of_update(self) -> list:
        return [self.get_info2update(d_row) for d_row in self.daily_data for r_row in self.runsheet_data if self.row_match(d_row, r_row)]
    
    def get_list_of_new(self) -> list:
        return [self.get_info2update(d_row) for d_row in self.daily_data for r_row in self.runsheet_data if not self.row_match(d_row, r_row)]
    
    def values2list(self, row_dict) -> list:
        return [item for item in row_dict.values()]

    def print_no_match_list(self):
        for item in self.no_match_new_list:
            result = ', '.join(item)
            print(result)
                
with open('output.txt', 'w', encoding='UTF-8') as output, open('new_list.csv', 'w', encoding='UTF-8') as new_list:
    update = Updater()
    
    sheet = GspreadObj(runsheet_id, key_file, runsheet_worksheet)
    #print(update.get_list_of_update())
    #print(update.new_list)
    #print(len(update.print_no_match_list()), file=new_list)
    for item in update.no_match_new_list:
        a_list = ','.join(item) 
        print(a_list, file=new_list)
    #update.update_cell()

