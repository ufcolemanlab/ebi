#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:40:35 2019

@author: jcoleman
"""

import urllib2
import re
from lxml import etree
import StringIO


#page = urllib.urlopen("https://encorbio.com/product/mca-2a5/").read()

webp=urllib2.urlopen("https://encorbio.com/product/mca-2a5/").read()
tempweb = webp.find("Cat#")

#%%
# OR?:
#from urllib2 import urlopen
#page = urlopen('http://www.example.com').read()

# from: https://docs.python-guide.org/scenarios/scrape/
from lxml import html
import requests

#page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
page = requests.get('https://encorbio.com/product/mca-2a5/')
tree = html.fromstring(page.content)

#This will create a list of buyers:
#buyers = tree.xpath('//div[@title="buyer-name"]/text()')
buyers = tree.xpath('//*[@id="product-3444"]/text()')
#This will create a list of prices
prices = tree.xpath('//span[@class="item-price"]/text()')

print 'Buyers: ', buyers
print 'Prices: ', prices

# The best method yet to get the table data:
import pandas as pd

# Need a list of all product links, use to iterate links
remove_chars = ":"
product_link = "https://encorbio.com/product/mca-2a5/"
tables = pd.read_html(product_link)

print(tables[1])

print(tables[1][1][0])

# vendor name

# sku/catalog number

# product description/product name
print(tables[1][0][1])
#print(tables[1][0][1].replace(remove_chars, ""))
print(tables[1][1][1])

# product page url
print(product_link)

# vendor tested application
print(tables[1][0][9])
#print(tables[1][0][9].replace(remove_chars, ""))
print(tables[1][1][9])

# reactivity
print(tables[1][0][6])
#print(tables[1][0][6].replace(remove_chars, "").replace("Species Cross-", ""))
print(tables[1][1][6])

# host
print(tables[1][0][4])
#print(tables[1][0][4].replace(remove_chars, ""))
print(tables[1][1][4])

# clonality ?

# clone_id ?

# conjugate ?

# specificity ?

# post translational modification (ex) phospho ser 179, acetyl, etc) ?

# epitope sequence

# immunogen
print(tables[1][0][1])
#print(tables[1][0][1].replace(remove_chars, ""))
print(tables[1][1][1])

# immunogen type (peptide, recombinant protein etc)

# concentration (mg/ml)
print("concentration (ug/ul): ")
print("1")

# purity (serum vs purified)
print(tables[1][0][8])
print(tables[1][1][8])

# Ab formulation (azide-free, low endotoxin, bsa-free, LEAF etc)
print(tables[1][0][8])
print(tables[1][1][8])

# Ab Isotype/ Fab fragment

# molecular weight

# binding affinity

# UniProt/Accession Number

# Size (ug)

# discontinued?

# OEM

# Validation Image url link

# PMID/References

# Datasheet url

# MSDS url

#%% Beautiful Soup 4
import requests
website_url = requests.get('https://en.wikipedia.org/wiki/List_of_Asian_countries_by_area').text

from bs4 import BeautifulSoup
soup = BeautifulSoup(website_url,'lxml')
#print(soup.prettify())

# use the 'find_all' function to bring back all instances of the 'table' tag in the HTML and store in 'all_tables' variable
My_table = soup.find('table',{'class':'wikitable sortable'})
My_table

links = My_table.findAll('a')
links

Countries = []
for link in links:
    Countries.append(link.get('title'))
    
print(Countries)

import pandas as pd
df = pd.DataFrame()
df['Country'] = Countries

df

"""
Get data from the Table oin product pages:

<table>
      		<tr><!-- Row 1 -->
      			<td><b>Name:</b></td><!-- Col 1 -->
      			<td>Mouse monoclonal antibody to GFAP</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 2 -->
      			<td><b>Immunogen:</b></td><!-- Col 1 -->
      			<td>GFAP isolated biochemically from pig spinal cord</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 3 -->
      			<td><b>HGNC Name:</b></td><!-- Col 1 -->
      			<td><a href=http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:4235>GFAP</a></td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 4 -->
      			<td><b>Molecular Weight:</b></td><!-- Col 1 -->
      			<td>50kDa</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 5 -->
      			<td><b>Host:</b></td><!-- Col 1 -->
      			<td>Mouse</td><!-- Col 2 -->
      		</tr>
      		<tr class="isotype"><!-- Row 6 -->
      			<td><b>Isotype: </b> </td><!-- Col 1 -->
      			<td>IgG1</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 7 -->
      			<td><b>Species Cross-Reactivity:</b></td><!-- Col 1 -->
      			<td>Human, rat, mouse, cow, pig</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 8 -->
      			<td><b>RRID:</b></td><!-- Col 1 -->
      			<td><a href=http://antibodyregistry.org/search?q=SCR_016364>AB_2732880</a></td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 9 -->
      			<td><b>Format: </b>  </td><!-- Col 1 -->
      			<td>Purified antibody at 1mg/mL in 50% PBS, 50% glycerol plus 5mM NaN<sub>3</sub></td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 10 -->
      			<td><b>Applications:</b></td><!-- Col 1 -->
      			<td>WB, IF/ICC, IHC</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 11 -->
      			<td><b>Recommended Dilutions: </b></td><!-- Col 1 -->
      			<td>WB: 1:10,000. IF/ICC and IHC: 1:1,000.</td><!-- Col 2 -->
      		</tr>
      		<tr><!-- Row 12 -->
      			<td><b>Storage:</b></td><!-- Col 1 -->
      			<td>Stable at 4°C for one year, for longer term store at -20°C</td><!-- Col 2 -->
      		</tr>
      	</table>
          
"""

