import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
from tqdm import tqdm

def id_label(var_list):
    if 'hhid' in var_list:
        id_flag = 0

    elif 'psu' in var_list and 'hh' in var_list:
        id_flag = 0
        if 'id' in var_list or 'idcode' in var_list:
            id_flag = 1
    else:
        id_flag = -1

    return id_flag


# Albania URL
URL = "https://microdata.worldbank.org/index.php/catalog/1970/data-dictionary"

print("Extracting module names and descriptions...")
response = requests.get(URL)
df_list = pd.read_html(response.content) #Extracts all tables on page as a single df
df = df_list[0] # Selects only df in list as df

# Descriptive information in first column "Data file", string indexing to get module name and description
# Store each module as row in main_df
df["module_name"] = df["Data file"].apply(lambda x: x.split(" ")[0]) 
#df["module_description"] = df["Data file"].apply(lambda x: (" ").join(x.split("_")[1:]))
df["module_description"] = df["Data file"].apply(lambda x: (" ").join(x.split(" ")[1:]))
df.drop(columns=["Data file"], inplace=True)
main_df = df.copy() 

#Edge case for module 6D with missing underscore
main_df.loc[main_df["module_name"] == "Modul_6D_Shocks", ["module_name", "module_description"]] = ["Modul_6D_Shocks_to_the_household", "Module 6D - Household Shocks"]



all_dics = []
print("Extracting variable names, descriptions, and types...")
for i in range(len(main_df)):
#for i in range(1):
#for i in range(17,18):
    print("Extracting from module {}...".format(main_df["module_name"][i]))

    #Extract information about each module from main_df
    module = main_df["module_name"][i] 
    module_description = main_df["module_description"][i]

    #Edge case for module 6D with missing underscore
    if module != "Modul_6D_Shocks_to_the_household":
        #Edge case for module 17 onwards, url naming changed
        if i + 1 > 30:
            i += 1
        #Navigate to data site for each module and capture it as beautifulsoup object 
        module_url = URL + f"/F{i + 1}?file_name={module}"
    else:
        module_url = URL + f"/F{i + 1}?file_name=Modul_6D_Shocks%20%to%20the%20household"

    response = requests.get(module_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Search for containers that have the info we want -- which is variable name and link to variable webpage
    var_ids = soup.find_all("a", class_="var-id text-break")
    list_of_dics = []    
    var_list = [] # Create a list to capture variables from module

    for var_id in var_ids:
        #Handling edge cases for Module 10 with misnamed variable
        if module == 'Modul_10_Fertility':
            text = var_id.text.lower()
            if text == 'm0_q00':
                text = 'psu'
            elif text == 'm0_q01':
                text = 'hh'
            
            list_of_dics.append({"variable_name": text, "variable_link": var_id["href"]})
            var_list.append(text)

        else:
            list_of_dics.append({"variable_name": var_id.text.lower(), "variable_link": var_id["href"]})
            var_list.append(var_id.text.lower())

    

    """ 
    Create an id flag,
    0 = household id present, individual id absent
    1 = household identifier 'hhid' present or proxy household 'psu','hh' present, individual id present
    """
    id_flag = id_label(var_list)
    id_mapping = {
        0: 'hhid',
        1: 'id',
    }
    unique_id = id_mapping.get(int(id_flag))
    rem_id = []
     
    # For every variable in the module, extract variable description and variable type by going to the variable webpage
    for j in tqdm(range(len(list_of_dics))):
    #for j in tqdm(range(2)):
        # Select dictionary associated with module
        dic = list_of_dics[j] 
 
        if dic["variable_name"] in ["psu","hh","idcode", "id", "hhid"]:
            del dic["variable_link"]
            rem_id.append(j)
            continue

        # Find data by parsing through link for each variable and creating beautiful soup object
        var_link = dic["variable_link"]
        var_response = requests.get(var_link)
        var_soup = BeautifulSoup(var_response.content, 'html.parser')
        var_data = var_soup.find_all("div", class_="variable-container")

        # Fill up output dictionary based on data
        del dic["variable_link"]
        var_description_raw = var_data[0].find("h2").text.strip()
        var_description = (" ").join(var_description_raw.split(" ")[:-1])
        var_type = var_data[0].find("div", class_="fld-inline sum-stat sum-stat-var_intrvl").text.split(":")[1].strip()
        dic["variable_description"] = var_description
        dic["module_name"] = module
        dic["module_description"] = module_description
        dic["data_type"] = var_type
        dic["unique_id"] = unique_id

    pruned_list_of_dics = []
    for k, dic in enumerate(list_of_dics):
        if k not in rem_id:
            pruned_list_of_dics.append(dic)

    all_dics += pruned_list_of_dics

pd.DataFrame(all_dics).to_csv("output/albania_metadata.csv", index=False)