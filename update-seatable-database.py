__author__ = "Rami Sedhom"
__license__ = "GNU GPLv3"
__version__ = "1.0"
__email__ = "rami.sedhom@gmail.com"

# Import python libraries

## For environment variables
import os

## For Seatable API
from seatable_api import Base

## For processing json from url
import urllib.request, json

## For comparison using Pandas library
import pandas as pd


# Get plugins information from Seatable database

## Initialize connection to SeaTable
server_url = 'https://cloud.seatable.io'
api_token = os.environ.get('SEATABLE_API_TOKEN')
table_name = 'Plugins'
base = Base(api_token, server_url)
base.auth()

## Get rows from 'Plugins' table
lst_seatable = base.query('SELECT _id, ID, Name, Description, `Github Link` FROM `' + table_name + '` LIMIT 10000')

## Convert list to Pandas dataframe using json_normalize to flatten the list
df_seatable = pd.json_normalize(lst_seatable)


# Get plugins information from obsidianmd/community-plugins.json
with urllib.request.urlopen("https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json") as url:
  obsidian_community_plugins = json.loads(url.read().decode())

## Convert list to Pandas dataframe using json_normalize to flatten the list
## Columns: id, name, author, description, repo
df_community = pd.json_normalize(obsidian_community_plugins)


# Prepare data frames for comparison

## Drop unnecessary columns
df_community.drop(columns=['author'], inplace=True)

## Rename Seatable data frame columns to be the same as df_community column names
df_seatable.rename(columns={'ID': 'id', 'Name': 'name', 'Description': 'description', 'Github Link': 'repo'}, inplace=True)

## Re-index using column: 'id'
df_seatable.set_index('id', inplace=True)
df_community.set_index('id', inplace=True)

## Modify repo column
df_community['repo'] = df_community['repo'].replace('^','https://github.com/', regex=True)

## Add 'source' column to differentiate the 2 datasets
df_seatable['source']='seatable'
df_community['source']='community'


# Mark deleted plugins as not available

## Get deleted plugins that are not anymore in community dataframe
## from rows which are in seatable dataframe but NOT in community dataframe
df_seatable_only = df_community.merge(df_seatable.drop_duplicates(), on=['id'], how='right', indicator=True, suffixes=('_community', '_seatable'))

## Mark Plugin Available as False if the plugin is available only in Seatable
for index, row in df_seatable_only.iterrows():
  if row['_merge'] == 'right_only':
    base.update_row(table_name, row['_id'], {"Plugin Available": False})


# Update plugins in Seatable

## Compare the 2 dataframes by concat and drop duplications
## on column: 'name','description','repo'; keeping community records only
df_diff = pd.concat([df_seatable,df_community]).drop_duplicates(subset=['name','description','repo'],keep=False)
df_diff = df_diff[df_diff['source'] == 'community']

## Update Seatable
for index, row in df_diff.iterrows():
  ## Convert Series 'row' to dictionary
  fields = row.to_dict()
  
  ## Drop unnecessary columns
  fields.pop('source')
  
  ## Rename dictionary keys to be the same as Seatable column names
  fields['Name'] = fields.pop('name')
  fields['Description'] = fields.pop('description')
  fields['Github Link'] = fields.pop('repo')

  for record in lst_seatable:
    ## Update record in Seatable
    if record['ID'] == index:
      print('Updating seatable record: ' + index)
      base.update_row(table_name, row['_id'], fields)
    break
  
  ## Create new records for new plugins
  print('Inserting new seatable record for new plugin: ' + index)
  fields['ID'] = index
  fields['Plugin Available'] = True
  fields.pop('_id')
  base.append_row(table_name, fields)