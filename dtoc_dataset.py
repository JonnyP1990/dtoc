# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:51:38 2022

@author: jonpr
"""

### Delayed Transfers of Care (DTOC) dataset
import os

os.chdir(r"C:\Users\jep39\Postdoc files\DTOC")
path = os.getcwd()
dataPath = os.path.join(path, r"Datasets")

import pandas as pd
import numpy as np

# load data and standardise format across years
newMths = ["JANUARY", "FEBRUARY", "MARCH"]
df = pd.DataFrame()
for root, dirs, files in os.walk(dataPath):
    for file in files:
        if file.endswith("dtoc.csv") & file.startswith("20"):
            newdf = pd.read_csv(os.path.join(dataPath, file))
            if newdf.iloc[0, 1] in newMths:
                newdf["Year"] = newdf.iloc[0, 0][:2] + newdf.iloc[0, 0][-2:]
            elif newdf.columns[0] == "Year":
                newdf["Year"] = newdf.iloc[0, 0][:4]
            elif newdf.iloc[0, 0].startswith("MSitDT"):
                pName = newdf["Period"].copy()
                newdf["Period"] = newdf.iloc[0, 0][-4:]
                newdf.insert(1, "A", np.empty(len(newdf["Period"])))
                newdf["A"] = pName[0][7:-5].upper()
            newdf.columns = [
                "Year",
                "Month",
                "Prov_code",
                "Prov_name",
                "Prov_org_code",
                "Prov_org_name",
                "LA_code",
                "LA_name",
                "CareType",
                "DelayReason",
                "NHS_A",
                "NHS_B",
                "SC_A",
                "SC_B",
                "Both_A",
                "Both_B",
            ]
            df = pd.concat([df, newdf])

# year/month variable
df["Y/M"] = df["Year"] + "_" + df["Month"]
TimeDict = dict(enumerate(df["Y/M"].unique()))

# drop data outside England
df = df[df["LA_name"] != "RESIDENT IN SCOTLAND"]
df = df[df["LA_name"] != "RESIDENT IN WALES"]
df = df[df["LA_name"] != "RESIDENT OUTSIDE GB"]

# fix Bournemouth
newBNMname = {
    "BOURNEMOUTH UA": "BOURNEMOUTH, CHRISTCHURCH AND POOLE",
    "POOLE UA": "BOURNEMOUTH, CHRISTCHURCH AND POOLE",
    "BOURNEMOUTH, CHRISTCHURCH AND POOLE UA": "BOURNEMOUTH, CHRISTCHURCH AND POOLE",
}
df["LA_name"] = df["LA_name"].replace(newBNMname)

# add standard region codes
regIDs = pd.read_csv(os.path.join(path, "regionIDs.csv"))
name2code = pd.Series(
    regIDs.areaCode.values, index=regIDs.areaName.str.upper()
).to_dict()
code2name = pd.Series(regIDs.areaName.values, index=regIDs.areaCode).to_dict()
code2numb = pd.Series(regIDs.areaNumb.values, index=regIDs.areaCode).to_dict()
numb2code = pd.Series(regIDs.areaCode.values, index=regIDs.areaNumb).to_dict()
numb2name = pd.Series(regIDs.areaName.values, index=regIDs.areaNumb).to_dict()

df["areaNumb"], df["areaCode"], df["areaName"] = df["LA_code"], "", ""
for i in range(len(df)):
    try:
        df.iloc[i, -2] = name2code[df.iloc[i, 7]]
    except:
        df.iloc[i, -2] = numb2code[int(df.iloc[i, -3])]
    df.iloc[i, -1] = code2name[df.iloc[i, -2]]
    df.iloc[i, -3] = code2numb[df.iloc[i, -2]]

df = df[
    [
        "areaCode",
        "areaNumb",
        "areaName",
        "Year",
        "Y/M",
        "Prov_org_code",
        "Prov_org_name",
        "CareType",
        "DelayReason",
        "NHS_A",
        "NHS_B",
        "SC_A",
        "SC_B",
        "Both_A",
        "Both_B",
    ]
]

# dtoc totals
dfTotals = (
    df.groupby(["Year", "Y/M", "areaCode", "areaName"])
    .sum()
    .reset_index()
    .drop(["NHS_A", "SC_A", "Both_A"], axis=1)
)
dfTotals["dtoc_total"] = dfTotals[["NHS_B", "SC_B", "Both_B"]].sum(axis=1)

# save dataset files
df.to_csv("dtoc_full.csv", index=False)
dfTotals.to_csv("dtoc_totals.csv", index=False)
