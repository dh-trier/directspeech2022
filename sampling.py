"""
Script to sample sentences from an ELTeC collection for annotation. 
"""


# === Imports === 

from random import randint
import pandas as pd 
from os.path import join
from datetime import datetime as dt
from os import listdir
import glob
from lxml import etree as ET
import re


# === Parameters === 

eltecfolder = join("/", "home", "christof", "Repositories", "Github", "eltec", "ELTeC-fra", "level2", "") 
sentspernovel = 10


# === Functions === 

def get_fileslist(eltecfolder): 
    fileslist = [f for f in listdir(eltecfolder)]
    print(len(fileslist), "files found")
    return fileslist
    

def get_numsentslist(eltecfolder, fileslist):
    numsentslist = {}
    ns = {'tei':'http://www.tei-c.org/ns/1.0',
          'eltec':'http://distantreading.net/eltec/ns'}  
    #ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    for xmlfile in fileslist:
        root = ET.parse(join(eltecfolder, xmlfile)).getroot()
        print("Getting number of sentences from:", xmlfile)
        boundaries = root.findall(".//tei:body//tei:w[@n='SENT']", ns)
        numsentslist[xmlfile] = len(boundaries)
    #print(len(numsentslist))
    return numsentslist


def get_samplesents(fileslist, numsentslist, sentspernovel):
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    samplesents = []
    for xmlfile in fileslist: 
        print("Extracting sentences from:", xmlfile)
        numsents = numsentslist[xmlfile]
        randomsentnums = [randint(0, numsents) for p in range(0, sentspernovel*5)]
        #print(randomsentnums)
        root = ET.parse(join(eltecfolder, xmlfile)).getroot()
        year = root.xpath(".//tei:bibl[@type='firstEdition']/tei:date/text()", namespaces=ns)[0]
        counter = 0
        for sentnum in randomsentnums: 
            precedingSENT = root.findall(".//tei:body//tei:w[@n='SENT']", ns)[sentnum-1]
            result = precedingSENT.xpath("following-sibling::*/text()")
            PUNC = [".", "!", "?"]
            sentence = []
            for token in result: 
                if token not in PUNC:   
                    sentence.append(token)
                else: 
                    sentence.append(token)
                    break
            sentence = " ".join(sentence)
            sentence = re.sub("\n", " ", sentence)
            sentence = re.sub(" \.", ".", sentence)
            sentence = re.sub(" ,", ",", sentence)
            sentence = re.sub(" '", "'", sentence)
            sentence = re.sub("' ", "'", sentence)
            sentence = re.sub(" ;", ";", sentence)
            if len(sentence) > 20: 
                sentencedata = [xmlfile, year, sentnum, sentence]
                samplesents.append(sentencedata)
                counter +=1
            if counter == 10: 
                break
    #print(samplesents)
    return(samplesents)


def save_samplesents(samplesents): 
    timestamp = dt.now().strftime("%Y-%b-%d-%H-%M")
    samplesentsfile = "eltec-fra_samplesents_"+timestamp+".tsv"
    samplesents = pd.DataFrame.from_records(samplesents, columns = ["filename", "year", "sentnum", "sentence"])
    samplesents.sort_values(by=["year", "filename"], ascending=True, inplace=True)
    with open(samplesentsfile, "w", encoding="utf8") as outfile: 
        samplesents.to_csv(outfile, sep="\t")




# === Main === 

def main(eltecfolder, sentspernovel): 
    fileslist = get_fileslist(eltecfolder) 
    numsentslist = get_numsentslist(eltecfolder, fileslist)
    samplesents = get_samplesents(fileslist, numsentslist, sentspernovel)
    save_samplesents(samplesents)   

main(eltecfolder, sentspernovel)







