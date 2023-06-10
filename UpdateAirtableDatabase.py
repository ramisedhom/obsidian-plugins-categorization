"""Update Airtable base with online github json file.

Update "P-Obsidian Plugins Categorization" Airtable database with
"Obsidian.md Community Plugins" maintained by plugins contributors into
https://github.com/obsidianmd/obsidian-releases.
Check: https://forum.obsidian.md/t/13565
"""

# Import python libraries

## For environment variables
import os

## For Airtable API
from pyairtable import Table

## For processing json from url
import urllib.request, json

## For comparison using Pandas library
import pandas as pd

## For waiting timer
import time

__author__ = "Rami Sedhom"
__copyright__ = "Copyright 2021, Rami Sedhom"
__credits__ = ["Rami Sedhom"]
__license__ = "GNU GPLv3"
__version__ = "1.0"
__maintainer__ = "Rami Sedhom"
__email__ = "rami.sedhom@gmail.com"
__status__ = "Development"

# Get plugins information from Airtable database

api_key = os.environ.get('AIRTABLE_API_KEY')
base_id = 'appyfMsHdYxRsHPoX'
table_name = 'Plugins Categorized'
obsidian_airtable_plugins = Table(api_key, base_id, table_name)

## Retrieve columns: id, createdTime, fields.Name, fields.Description, fields.Github Link, fields.ID
lst_airtable = obsidian_airtable_plugins.all(fields=['ID', 'Name', 'Description', 'Github Link'])

## Convert list to Pandas dataframe using json_normalize to flatten the list
df_airtable = pd.json_normalize(lst_airtable)


# Get plugins information from obsidianmd/community-plugins.json

with urllib.request.urlopen("https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json") as url:
  obsidian_community_plugins = json.loads(url.read().decode())

## Convert list to Pandas dataframe using json_normalize to flatten the list
## Columns: id, name, author, description, repo, branch 
df_community = pd.json_normalize(obsidian_community_plugins)


# Prepare data frames for comparison

## Drop unnecessary columns
df_airtable.drop(columns=['id', 'createdTime'], inplace=True)
df_community.drop(columns=['author'], inplace=True)

## Rename Airtable data frame columns to be the same as df_community column names
df_airtable.rename(columns={'fields.Name': 'name', 'fields.Description': 'description', 'fields.Github Link': 'repo', 'fields.ID': 'id'}, inplace=True)

## Re-index using column: 'id'
df_airtable.set_index('id', inplace=True)
df_community.set_index('id', inplace=True)

## Modify repo column
df_community['repo'] = df_community['repo'].replace('^','https://github.com/', regex=True)

## Add 'source' column to differenciate the 2 datasets
df_airtable['source']='airtable'
df_community['source']='community'


# Compare the 2 dataframes by concat and drop duplications
# on columns: 'name','description','repo'; keeping community records only
df_diff = pd.concat([df_airtable,df_community]).drop_duplicates(subset=['name','description','repo'],keep=False)
df_diff = df_diff[df_diff['source'] == 'community']


# Update Airtable with differences

for index, row in df_diff.iterrows():
  ## Convert Series 'row' to dictionary
  fields = row.to_dict()
  
  ## Drop unnecessary columns
  fields.pop('source')
  
  ## Rename dictionary keys to be the same as Airtable column names
  fields['Name'] = fields.pop('name')
  fields['Description'] = fields.pop('description')
  fields['Github Link'] = fields.pop('repo')

  for record in lst_airtable:
    ## Update record in airtable
    if record['fields']['ID'] == index:
      print('Updating airtable record: ' + index)
      obsidian_airtable_plugins.update(record['id'], fields)
    break
  
  ## Create new records for new plugins
  print('Inserting new airtable record for new plugin: ' + index)
  fields['ID'] = index
  obsidian_airtable_plugins.create(fields)
  time.sleep(1) # Sleep for 1 seconds to respect airtable rate limit 5 calls/sec
