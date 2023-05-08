from datetime import datetime
## â€™
## Â
class DailyUpdate():
    date = datetime.today().strftime("%Y-%m-%d")
    
    daily_data_dict = {
        "product":"","version":"","title":"","Phrase project":"","Phrase job":"",
        "Total words":"","Approx net words":"","Hours estimated":"","Hours used":"","Notes":"",
        "Translator":"","% filled from TM":"",
        "Pantheon":"", "en url":"", "ja url":"", "en date":"",
    }

    jp_sheet_dict = {
        "Categories":"","product":"","version":"","title":"","ja url":"","Phrase project":"",
        "Phrase job":"","Ver.":"","TEAM":"","Total words":"","Approx net words":"","Hours estimated":"",
        "Quality":"","Hours used":"","Translator":"","ComDate":"","Status":"","LastUpdate":"",
        "% filled from TM":"","Pantheon":"","en url":"","en date":"","net_word":"", "Notes":"",
    }

    check2bsame = ["product", "version", "title"]
    copy_lst_from_daily = ["Total words", "Approx net words", "% filled from TM"]

    delete_lst = ["Translator", "ComDate", "Hours used"]

    def __init__(self, daily_update, jp_runsheet):
        self.daily_update = daily_update
        self.jp_runsheet = jp_runsheet

        ##TODO 1: get data from daily sheet to put in jp_sheet format (csv format)
        ## first map update info to daily_data dict then convert to jp format
        self.daily_update_csv = self.insert_jp_format(self.daily_update, self.daily_data_dict) 
        self.update2jp_format()
        self.daily_update_csv = self.add_single_quo(self.daily_update_csv)
        self.daily_update_csv = self.remove_break(self.daily_update_csv)
        
        ##TODO 2: get existing jp data from current documentation in jp_sheet format()
        self.jp_sheet_csv = self.insert_jp_format(self.jp_runsheet, self.jp_sheet_dict)
        self.jp_sheet_csv = self.add_single_quo(self.jp_sheet_csv)
        self.jp_sheet_csv = self.remove_break(self.jp_sheet_csv)
        
        self.newly_added = []

        ##TODO 3: iterate each jp date to en_date to compare, 
        # TODO 3.5: if product, version, title from jp sheet, 
        # are the same as rudi_info then copy  "Total words", "Approx net words", "% filled from TM", Phrase job from daily update to jpsheet
        self.overwrite_jp_info() ## for non_chage

        ##TODO 4: if product, version, titles are the same but
        # total words, approx networds are different, then copy those with Phrase job url then change status to UPD then change Lastupdate to currentdate,
        #self.update_monthly() 
        ##if product, version, titles are the same but total words, approx networds are different, 
        # then change the status to UPD then change Lastupdate to currentdate, if status is Done then delete Translator and CompDate
        #self.remove_linebreak()

        #self.csv_values()
        self.no_match_list = self.get_no_match_list()
        self.no_match_list = self.remove_break(self.no_match_list)
        self.stat_upd4no_match()

    def add_single_quo(self, lst_dict) -> list:
        ##add single quote for version to avoid losing zeros
        return [{k:"'"+ v if k == "version" else v for k, v in a_dict.items()} for a_dict in lst_dict]

    def conv2str(self, lst_dict) -> list:
        ##converts int to str to avoid florting zero to be removed, returns list of dictionaries
        return [{k: str(v) for k, v in a_dict.items()} for a_dict in lst_dict]
    
    def csv_values(self, csv):
        return [",".join(each_dict.values()) for each_dict in csv]
            
    def insert_jp_format(self, data, ref_sheet):
        return [dict(zip(ref_sheet.keys(), item.split(","))) for item in data]
    
    def update2jp_format(self):
        self.daily_update_csv = [{jp_key: upd_dict.get(jp_key, "") for jp_key in self.jp_sheet_dict.keys()} for upd_dict in self.daily_update_csv]
    
    def fix_last_data(self, lst_dict) -> list:
        return [{key: "" if key == "net_word" else value for key, value in each_dict.items()} for each_dict in lst_dict]

    def find_match(self, daily_dict, jp_dict, lst) -> bool:
        ##look for daily_dict and jp_dict match with list of items
        return all(daily_dict[item] == jp_dict[item] for item in lst)
              
    def copy_from_daily(self, daily_dict, jp_dict, lst):
        ##copy lst of items from daily update 
        for item in lst:
            jp_dict[item] = daily_dict[item]
        return jp_dict

    def delete_items(self, jp_dict, lst):
        for item in lst:
            jp_dict[item] = ""
        return jp_dict
        
    def overwrite_jp_info(self):
        ##if product, version, title from jp sheet, 
        # are the same as rudi_info then copy
        # "Total words", "Approx net words", "% filled from TM" from daily update to jpsheet
        for daily_dict in self.daily_update_csv:
            for jp_dict in self.jp_sheet_csv:
                if self.find_match(daily_dict, jp_dict, self.check2bsame):
                    if jp_dict["Status"] == "Done":
                        self.delete_items(jp_dict, self.delete_lst)
                        jp_dict["Status"] = "UPD"
                    self.copy_from_daily(daily_dict, jp_dict, self.copy_lst_from_daily)
                    jp_dict["Status"] = "UPD"
                    jp_dict["LastUpdate"] = self.date
    
    def get_no_match_list(self):
        return [daily_dict for daily_dict in self.daily_update_csv if not any(self.find_match(daily_dict, jp_dict, self.check2bsame) for jp_dict in self.jp_sheet_csv)]
    
    def stat_upd4no_match(self):
        for each_dict in self.no_match_list:
            each_dict["Status"] = "UPD"
            each_dict["LastUpdate"] = self.date
    
    def remove_break(self, dict_lst):
        return [{k: v.replace("\n", "") for k, v in each_dict.items()} for each_dict in dict_lst]


with open("0508_en.csv", "r") as daily_data, open("0505_jp.csv", "r") as jp_data, open("updated_daily.csv", "w") as updated, open("nomatch.csv", "w") as nomatch:
    daily_update = DailyUpdate(daily_data, jp_data)
    
    for item in daily_update.csv_values(daily_update.jp_sheet_csv):
        print(item, file=updated)
    
    for item in daily_update.csv_values(daily_update.no_match_list):
        print(item, file=nomatch)
