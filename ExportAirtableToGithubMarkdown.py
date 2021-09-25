"""Export Airtable base to Github markdown.

Export "P-Obsidian Plugins Categorization" Airtable database to
Github's markdown format to be published on Awesome-Obsidian Github
repository. Check discussion on: 
https://discord.com/channels/686053708261228577/888107495233568778
"""

# Import python libraries

## For environment variables
import os

## For Airtable API
from pyairtable import Table

## For handling Airtable tables using Pandas library
import pandas as pd

__author__ = "Rami Sedhom"
__copyright__ = "Copyright 2021, Rami Sedhom"
__credits__ = ["Rami Sedhom"]
__license__ = "GNU GPLv3"
__version__ = "1.0"
__maintainer__ = "Rami Sedhom"
__email__ = "rami.sedhom@gmail.com"
__status__ = "Development"

# Set Airtable API key and database ID

api_key = os.environ.get["AIRTABLE_API_KEY"]
base_id = 'appyfMsHdYxRsHPoX'


# Get Plugins table from Airtable database

## Set plugins table
table_name = 'Plugins Categorized'
airtable_plugins = Table(api_key, base_id, table_name)

## Retrieve columns: id, createdTime, fields.Name, fields.Description, fields.Category, fields.Github Link
lst_plugins = airtable_plugins.all(fields=['Name', 'Description', 'Category', 'Github Link'])


# Get Categories table from Airtable database

## Set Categories table
table_name = 'Categories'
airtable_categories = Table(api_key, base_id, table_name)

## Retrieve columns: id, createdTime, fields.Category, fields.Description
lst_categories = airtable_categories.all(fields=['Category', 'Description'])


# Replace Categories ID with Categories Name in lst_plugins

## First, convert lst_categories to dictionary {'id':'category name'}
dic_categories = {}
for i in lst_categories:
  dic_categories[i['id']] = i['fields']['Category']

## Escape pipe character "|" in Name and Description fields
## Also replace categories IDs with categories name if plugin is categorized
for i in lst_plugins:
  i['fields']['Name'] = i['fields']['Name'].replace("|","\|")
  i['fields']['Description'] = i['fields']['Description'].replace("|","\|")
  if 'Category' in i['fields'].keys():
    lst_plugin_categories = i['fields']['Category']
    i['fields']['Category'] = [dic_categories.get(item,item) for item in lst_plugin_categories]
    i['fields']['Category'] = ', '.join(i['fields']['Category'])


# Export plugins list to markdown

## Convert plugins list as pandas data frame
df_plugins = pd.json_normalize(lst_plugins)

## Combine columns: (name and link) in 1 hyperlink column
df_plugins = df_plugins.assign(Name = '<a href="' + df_plugins['fields.Github Link'] + '">' + df_plugins['fields.Name'] + '</a>')

## Drop unnecessary columns
df_plugins.drop(columns=['id', 'createdTime', 'fields.Name', 'fields.Github Link'], inplace=True)

## Rename Airtable data frame columns to be more friendly
df_plugins.rename(columns={'fields.Description': 'Description', 'fields.Category': 'Categories'}, inplace=True)

## Rearrange columns order, getting Name in front
df_plugins = df_plugins[['Name', 'Description', 'Categories']]

## Generate markdown file in 'github' format
## require: tablue library to be installed 
df_plugins.to_markdown("plugins.md", tablefmt="github", index=False)
