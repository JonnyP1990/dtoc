# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:44:04 2022

@author: jep39
"""

import os

os.chdir(r"C:\Users\jep39\Postdoc files\DTOC")
path = os.getcwd()
dataPath = os.path.join(path, r"Datasets")
plotPath = os.path.join(path, r"Plots")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.express as px
from plotly.offline import plot
from scipy.interpolate import make_interp_spline, BSpline

## load datasets
df = pd.read_csv(os.path.join(dataPath, "dtoc_full.csv"))
dfTotals = pd.read_csv(os.path.join(dataPath, "dtoc_totals.csv"))

## dtoc by time
# scatter
plt.figure(1)
plt.scatter(dfTotals["Y/M"], dfTotals["dtoc_total"])
plt.xticks(np.arange(9, 108, 12), np.arange(2012, 2021, 1))
plt.ylabel("Total delayed transfer days per month")
plt.savefig(os.path.join(plotPath, "dtocXtime.png"), dpi=300, bbox_inches="tight")

# line
plt.figure(2)
totals_by_month = (
    dfTotals.groupby(["Y/M"])
    .mean()
    .reset_index()
    .drop(["NHS_B", "SC_B", "Both_B", "Year"], axis=1)
)
plt.plot(totals_by_month["Y/M"], totals_by_month["dtoc_total"])
plt.xticks(np.arange(9, 108, 12), np.arange(2012, 2021, 1))
plt.ylabel("Average number of delayed transfer days per month")
plt.savefig(os.path.join(plotPath, "dtocXtime2.png"), dpi=300, bbox_inches="tight")

# smooth line
plt.figure(3)
x, y = (
    np.arange(1, len(totals_by_month["dtoc_total"]) + 1, 1),
    totals_by_month["dtoc_total"],
)
x2 = np.linspace(x.min(), x.max(), 300)
bSpline = make_interp_spline(x, y, k=3)
smoothY = bSpline(x2)
plt.plot(x2, smoothY)
plt.xticks(np.arange(9, 108, 12), np.arange(2012, 2021, 1))
plt.ylabel("Average number of delayed transfer days per month")
plt.savefig(os.path.join(plotPath, "dtocXtime3.png"), dpi=300, bbox_inches="tight")


## dtoc by region
# calculate dtoc per capita
ukpop_df = pd.read_csv(os.path.join(dataPath, "ukpop2020_by_age.csv"), thousands=",")
ukpop_df = ukpop_df.drop(["Name", "Geography"], axis=1)
ukpop_df = ukpop_df.iloc[:416, :92]
ukpop_totals = pd.DataFrame(
    [ukpop_df["Code"], ukpop_df.iloc[:, 1:92].sum(axis=1).astype(int)]
).transpose()
ukpop_totals.columns = ["areaCD", "population"]
code2pop = pd.Series(
    ukpop_totals.population.values, index=ukpop_totals.areaCD
).to_dict()
code2pop["E10000021"] = code2pop["E06000061"] + code2pop["E06000062"]

totals_by_region = (
    dfTotals.groupby(["areaCode", "areaName"])
    .sum()
    .reset_index()
    .drop(["NHS_B", "SC_B", "Both_B", "Year"], axis=1)
)
totals_by_region["population"] = [code2pop[i] for i in totals_by_region["areaCode"]]
totals_by_region["dtoc_rate"] = (
    totals_by_region["dtoc_total"] / totals_by_region["population"]
)

# map plots
with open(os.path.join(dataPath, "GeoData.geojson")) as fp:
    GeoData = json.load(fp)


def ukPlot(dataset, variable, label):
    fig = px.choropleth_mapbox(
        dataset,
        locations="areaName",
        featureidkey="properties.areaNM",
        geojson=GeoData,
        color=variable,
        hover_name="areaName",
        mapbox_style="carto-positron",
        zoom=4,
        center={"lat": 55, "lon": 0},
        labels={variable: label},
    )
    return fig


dtoc_total_map = ukPlot(totals_by_region, "dtoc_total", "Days (2011-2020)")
dtoc_rate_map = ukPlot(totals_by_region, "dtoc_rate", "Days per capita (2011-2020)")

plot(dtoc_rate_map)
