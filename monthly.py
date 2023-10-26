from datetime import datetime
from GetMonthlyFiles import GetFiles
## â€™
## Â
# making status update for only total word and tm fill
class MonthlyUpdate():
    date = datetime.today().strftime("%Y-%m-%d")
    
    monthly_data_dict = {
        "product":"","version":"","title":"","Phrase project":"","Phrase job":"",
        "Total words":"","Approx net words":"","Hours estimated":"","Hours used":"","Notes":"",
        "Translator":"","% filled from TM":"",
        "Pantheon":"", "en url":"", "ja url":"", "en date":"",
    }

    jp_sheet_dict = {
        "product":"","version":"","title":"","ja url":"","Phrase project":"",
        "Phrase job":"","Ver.":"","Categories":"","Total words":"","Approx net words":"","Hours estimated":"",
        "Quality":"","Hours used":"","Translator":"","ComDate":"","Status":"","LastUpdate":"",
        "% filled from TM":"","Pantheon":"","en url":"","en date":"","net_word":"", "Notes":"",
    }

    check2bsame = ["product", "version", "title"]
    pre_release = ["pre-work", "prework"]
    copy_lst_from_daily = ["Total words", "Approx net words", "% filled from TM",
                           "Phrase job", "Phrase project", "en url", "ja url", "en date"]

    delete_lst = ["Translator", "ComDate", "Hours used"]

    def __init__(self, daily_update, jp_runsheet):
        self.daily_update = daily_update
        self.jp_runsheet = jp_runsheet

        ##TODO 1: get data from daily sheet to put in jp_sheet format (csv format)
        ## first map update info to daily_data dict then convert to jp format
        self.daily_update_csv = self.insert_jp_format(self.daily_update, self.monthly_data_dict) 
        self.update2jp_format()
        self.daily_update_csv = self.add_single_quo(self.daily_update_csv)
        self.daily_update_csv = self.remove_break(self.daily_update_csv)
        
        ##TODO 2: get existing jp data from current documentation in jp_sheet format()
        self.jp_sheet_csv = self.insert_jp_format(self.jp_runsheet, self.jp_sheet_dict)
        self.jp_sheet_csv = self.add_single_quo(self.jp_sheet_csv)
        self.jp_sheet_csv = self.remove_break(self.jp_sheet_csv)
        
        self.newly_added = []
        self.pre_work_changed = []
        ##TODO 3: iterate each jp date to en_date to compare, 
        # TODO 3.5: if product, version, title from jp sheet, 
        # are the same as rudi_info then copy  "Total words", "Approx net words", "% filled from TM", Phrase job from daily update to jpsheet
        self.overwrite_jp_info() ## for non_chage

        

        ##TODO 05-15, if jp_data has NA in dict object then check if daily update data has updated infor, URL, for that dict object.
        #check if there are NA in jp has_value 
        #get NAs from jp dict, has_value, list ex: ['ja url', 'en url']
        #compare that nas to new update object, 
        #if difference then copy from daily

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
        # for item in lst:
        #     if not self.key_exists(jp_dict, item):
        #         print(item, daily_dict, daily_dict[item])
        return all(daily_dict[item] == jp_dict[item] for item in lst)
    
    def key_exists(self, a_dict, a_key) -> bool:
        return a_key in a_dict


              
    def copy_from_daily(self, daily_dict, jp_dict, lst):
        ##copy lst of items from daily update 
        for item in lst:
            jp_dict[item] = daily_dict[item]
        return jp_dict

    def delete_items(self, jp_dict, lst):
        for item in lst:
            jp_dict[item] = ""
        return jp_dict
        
    def check_prer_change(self, en_dict, jp_dict, key, pre_work_list):
        return en_dict[key] not in pre_work_list and jp_dict[key] in pre_work_list

    def get_prer_change(self, en_dict):
        self.pre_work_changed.append(en_dict)

    def overwrite_jp_info(self):
        ##if product, version, title from jp sheet, 
        # are the same as rudi_info then copy
        # "Total words", "Approx net words", "% filled from TM" from daily update to jpsheet
        pre_work = []
        for daily_dict in self.daily_update_csv:
            for jp_dict in self.jp_sheet_csv:
                if not 'product' in jp_dict:
                    print(jp_dict)

                if self.find_match(daily_dict, jp_dict, self.check2bsame):
                    ##TODO: check if tm match in daily_dict is not 100%
                    ##TODO: if not 100%, then change jp_dict['Status'] to be "UPD" otherwise unchanged
                    # if jp_dict["Status"] == "Done":
                    #     self.delete_items(jp_dict, self.delete_lst)  #delete translator names, comp dates...
                    #     jp_dict["Status"] = "UPD"
                    if daily_dict['% filled from TM'] != "100" and daily_dict['% filled from TM'] != jp_dict['% filled from TM']:
                        self.copy_from_daily(daily_dict, jp_dict, self.copy_lst_from_daily)
                        jp_dict['Status'] = "UPD"
                        jp_dict["LastUpdate"] = self.date
                    
                    ##see if pre-work status has been changed; if so , then writes down to pre-work_change.csv
                    # if self.check_prer_change(daily_dict, jp_dict, "en date", self.pre_release):
                    #     pre_work.append(daily_dict)

                    # self.copy_from_daily(daily_dict, jp_dict, self.copy_lst_from_daily)
                    # jp_dict["Status"] = "UPD"
                    # jp_dict["LastUpdate"] = self.date
        self.pre_work_changed = pre_work
    
    def get_no_match_list(self):
        return [daily_dict for daily_dict in self.daily_update_csv if not any(self.find_match(daily_dict, jp_dict, self.check2bsame) for jp_dict in self.jp_sheet_csv)]
    
    def stat_upd4no_match(self):
        for each_dict in self.no_match_list:
            each_dict["Status"] = "UPD"
            each_dict["LastUpdate"] = self.date
    
    def remove_break(self, dict_lst):
        return [{k: v.replace("\n", "") for k, v in each_dict.items()} for each_dict in dict_lst]

getfile = GetFiles()
with open(getfile.en_mfile, "r", encoding='cp1252') as monthly_data, open(getfile.jp_mfile, "r", encoding='cp1252') as jp_data, open("updated_monthly.csv", "w", encoding='cp1252') as updated, open("nomatch_monthly.csv", "w") as nomatch, open("pre_work_change_monthly.csv", 'w') as pre_work:
    monthly_update = MonthlyUpdate(monthly_data, jp_data)
    
    for item in monthly_update.csv_values(monthly_update.jp_sheet_csv):
        print(item, file=updated)
    
    for item in monthly_update.csv_values(monthly_update.no_match_list):
        print(item, file=nomatch)

    for item in monthly_update.csv_values(monthly_update.pre_work_changed):
        print(item, file=pre_work)
