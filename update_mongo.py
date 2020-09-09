import os
import json

def load_json(directory):
    for file in os.listdir(directory):
        with open('{}/{}'.format(directory, file)) as f:
            file_data = json.load(f)
            update_json(file_data)
        with open('{}/{}'.format(directory, file),'w', encoding='utf8') as f:
            json.dump(file_data, f, indent=4, ensure_ascii=False)


def update_json(json_list):
    for i in json_list:
        if "Avsender(e)" not in i:
            try:
                brev_dato = i["Brevdato"]
                arkiv_sak = i["Arkivsak"]
                i["Brevdato"] = arkiv_sak
                i["Arkivsak"] = brev_dato
            except Exception:
                print(i)



load_json("scraping_reports")