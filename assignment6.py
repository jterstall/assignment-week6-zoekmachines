from __future__ import division
from bs4 import BeautifulSoup
from collections import Counter
import MySQLdb
import glob
import os
import re

# Tycho Koster, David Stap, Jeroen Terstall

def index_collection(folder):
    ministerie_lijst = []
    for infile in glob.glob( os.path.join(folder, '*.xml') ): # loop over each file
        with open(infile, 'r') as f:  # open file
            soup = BeautifulSoup(f.read(), "html.parser")  # get the text out
            items = soup.find_all("item", {"attribuut" : "Afkomstig_van"})
            for i in items:
                # Normalize by removing the abbreviations between parentheses
                ministerie = re.sub('\(.*?\)','', i.string).rstrip()
                ministerie_lijst.append(ministerie)
    return Counter(ministerie_lijst)

if __name__ == '__main__':
    folder = "doc/KVR/"
    counter = index_collection(folder)
    print counter
