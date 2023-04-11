import gspread, json

daily_update_file_id = ''
#source_file+_id

runsheet_id = ''
#runsheet id

key_file = ''
#json keyfile

runsheet_worksheet = "Documentation"
update_worksheet = '0407'

class gspreadObj():
    def __init__(self, spreadsheet_id, key_file, worksheet):
        self.spreadsheet_id = spreadsheet_id

        self.key_file = key_file
        self.worksheet = worksheet

        self.worksheet_obj = self.get_worksheet_obj()

        self.data_dict = self.get_data_dict()

        self.data_lsit = self.get_data_list()

        #daily
        #['product0', 'version1', 'title2', 'Phrase project3', 'Phrase job4',
        #  'Total words5, 'Approx net words6', 'Hours estimated7', 'Hours used8',
        #  'Notes', 'Translator', '% filled from TM', 'Pantheon', 'en url', 'ja url']

        #runsheet 0, 1, 
        #'Categories', 'product', 'version', 'title', 'ja url', 'Phrase project', 'Phrase job',
        #  'Ver.', 'TEAM', 'Total words', 'Approx net words', 'Hours estimated', 'Quality', 'Hours used',
        #  'Translator', 'ComDate', 'Status', 'LastUpdate', '% filled from TM', 'Pantheon', 'en url', 'en date',
        #  '2614541'

        #

    def get_worksheet_obj(self):
        gc = gspread.service_account(filename=self.key_file)
        sh = gc.open_by_key(self.spreadsheet_id) # or by sheet name: gc.open("TestList")
        return sh.worksheet(self.worksheet)   

    def get_data_dict(self) -> list:
        data = self.worksheet_obj.get_all_records()
        return [{**d, 'idx': i+2} for i, d in enumerate(data)]
    
    def get_data_list(self) -> list:
        return self.worksheet_obj.get_all_values()

class Updater():
    check_list = ['product', 'version', 'title', 'Phrase job']
    update_list = ['Total words', 'Approx net words', '% filled from TM', 'idx']
    update_dict = {'Total words': 10, 'Approx net words': 11, '% filled from TM' : 19}
    def __init__(self) -> None:
        self.daily_update_obj = gspreadObj(daily_update_file_id, key_file, update_worksheet)
        self.runsheet_obj = gspreadObj(runsheet_id, key_file, runsheet_worksheet)

        self.runsheet_data = self.runsheet_obj.data_dict
        self.daily_data = self.daily_update_obj.data_dict
        self.runsheet_list = self.runsheet_obj.data_lsit

        self.list_of_update = self.get_list_of_update()
        self.new_list = self.decoy()

    def row_match(self, daily_row, runsheet_row) -> bool:
        #takes each row to compare if they are the match
        return all(daily_row[item] == runsheet_row[item] for item in self.check_list)
    
    def get_info2update(self, daily_row) -> dict:
       #take daily_row and get info that to be inserted to runsheet row
       return {item: daily_row[item] for item in self.update_list}


    def decoy(self) -> list:
        new_list = []
        for d_column in self.daily_data:
            del d_column['idx']
            for r_column in self.runsheet_data:
                if self.row_match(d_column, r_column):
                    new_r_column = r_column
                    new_r_column.update(d_column)
                    new_list.append(new_r_column)
        return new_list
    
    def update_cell(self) -> list:
        for item in self.new_list:
            insert_item = [value for value in item.values()]
            insert_item_list = [insert_item[:-2]]
            
            s_idx = 'A'+ str(item['idx'])
            e_idx = 'W' + str(item['idx'])
            idx = s_idx + ':' + e_idx
            #print(insert_item_list)
            self.runsheet_obj.worksheet_obj.update(idx, insert_item_list)


    def get_list_of_update(self) -> list:
        return [self.get_info2update(d_row) for d_row in self.daily_data for r_row in self.runsheet_data if self.row_match(d_row, r_row)]
    
    def get_list_of_new(self) -> list:
        return [self.get_info2update(d_row) for d_row in self.daily_data for r_row in self.runsheet_data if not self.row_match(d_row, r_row)]
    
    def values2list(self, row_dict) -> list:
        return [item for item in row_dict.values()]
    



                    

with open('output.txt', 'w', encoding='UTF-8') as output:
    update = Updater()

    sheet = gspreadObj(runsheet_id, key_file, runsheet_worksheet)
    #print(update.get_list_of_update())
    print(update.update_cell())

