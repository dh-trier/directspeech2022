"""
Script to visualize annotation results over time. 
"""

# === Imports === 

import pandas as pd
from pandas_ods_reader import read_ods
import pygal
import numpy as np
from pygal.style import BlueStyle
from pygal.style import CleanStyle
from pygal.style import LightSolarizedStyle
import re

# === Parameters === 

annotationsfile = "eltec-fra_samplesents_2022-Apr-11-08-36_annotated.ods" 


# === Functions === 

def read_file(annotationsfile): 
    data = read_ods(annotationsfile)
    #print(data.head())
    num = int(sum(data["annotation"].value_counts()))
    return data, num


def simple_viz(data, num): 
    data = data.drop(["filename", "year", "sentence", "sentnum"], axis=1)
    overall = data["annotation"].value_counts()
    overall_pc = np.around(np.divide(overall, np.sum(overall))*100,1)
    pie = pygal.Pie(inner_radius=.4, legend_at_bottom=True, legend_at_bottom_columns=4, style=CleanStyle, print_values=True)
    pie.title = "Types of sentences across all novels (percentages; n="+str(num)+")"
    pie.add("narrator speech", overall_pc["n"])
    pie.add("character speech", overall_pc["c"])
    pie.add("mixed speech", overall_pc["x"])
    pie.add("other", overall_pc["u"])
    pie.render_to_file("sentence-types_overall.svg")
    print("-- Saved visualization for overall data.")
    

def decade_viz(data, num): 
    data = data.drop(["filename", "year", "sentence", "sentnum"], axis=1)
    data = data.fillna("na")
    decdata = data.groupby(by="decade")
    n = []
    c = []
    x = []
    u = []
    na = []
    for name,group in decdata: 
        decade = group["annotation"].value_counts()
        decade_pc = np.around(np.divide(decade, np.sum(decade))*100,0)
        try: 
            n.append(decade_pc["n"])
        except: 
            n.append(0)
        try: 
            c.append(decade_pc["c"])
        except: 
            c.append(0)
        try: 
            x.append(decade_pc["x"])
        except: 
            x.append(0)
        try: 
            u.append(decade_pc["u"])
        except: 
            u.append(0)
        try: 
            na.append(decade_pc["na"])
        except: 
            na.append(0)
    bar = pygal.StackedBar(legend_at_bottom=True, legend_at_bottom_columns=4, style=CleanStyle, print_values=True)
    bar.title = "Types of sentences per decade (percentages; n="+str(num)+")"
    bar.y_title = "Percentages"
    bar.x_labels = ["1840s","1850s","1860s","1870s","1880s","1890s","1900s","1910s"]
    bar.add("narrator", n)
    bar.add("character", c)
    bar.add("mixed", x, formatter=lambda x: "".format(x))
    bar.add("other", u, formatter=lambda x: "".format(x))
    #bar.add("not annotated yet", na, formatter=lambda x: "".format(x))
    bar.render_to_file("sentence-types_decades.svg")
    print("-- Saved visualization for data by decade.")
        


def sentlen_viz(data, num): 
    data = data.drop(["filename", "decade", "year", "sentnum"], axis=1)

    # Data preparation
    types = data.groupby(by="annotation")
    sentlendata = {}
    for name, group in types: 
        sentlist = list(group["sentence"])
        sentlens = []
        for sent in sentlist: 
            sentlens.append(len(re.split("\W+", sent)))
        sentlendata[name] = np.mean(sentlens)
    #print(sentlendata)
    
    # Visualization
    bar = pygal.Bar(legend_at_bottom=True, legend_at_bottom_columns=4, style=CleanStyle, print_values=True)
    bar.y_title = "Number of tokens"
    bar.title = "Average sentence length by type of sentence (tokens; n="+str(num)+")"
    bar.add("narrator", np.around(sentlendata["n"],1))
    bar.add("character", np.around(sentlendata["c"],1))
    bar.add("mixed", np.around(sentlendata["x"],1))
    bar.add("other", np.around(sentlendata["u"],1))
    bar.render_to_file("sentence-length-by-type.svg")
    print("-- Saved visualization for sentence length by type.")
    
            
        
        

   
    


# === Main ===

def main(annotationsfile): 
    print("\nLaunched.")
    data, num = read_file(annotationsfile)
    simple_viz(data, num)
    decade_viz(data, num)
    sentlen_viz(data, num)

main(annotationsfile)


