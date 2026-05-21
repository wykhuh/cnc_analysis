import utils
import pandas as pd
import json

url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&project_id=260796'
taxa_csv_path = '../processed_data/San_Antonio_cnc_2026.csv'
json_path = '../raw_data/San_Antonio_cnc_2026.json'

url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&project_id=273661'
taxa_csv_path = '../processed_data/Taranaki_cnc_2026.csv'
json_path = '../raw_data/Taranaki_cnc_2026.json'

# url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&taxon_id=47120'
# taxa_csv_path = '../processed_data/arthropod.csv'
# json_path = '../raw_data/arthropod.json'

print('start fetching')
# taxonomy_data = utils.downloadData(url, json_path)
taxonomy_data = utils.fetchData(url)
print('end fetching')

# with open(json_path, 'r') as f:
#     taxonomy_data = json.load( f)['results']

ranks = utils.getSortedRanks(taxonomy_data)
treeData = utils.buildTree(taxonomy_data, 'id', 'parent_id' )

taxonList = []
taxon = dict()
utils.flattenTree(treeData[0], taxonList, taxon, ranks)

df = utils.createTaxaListCsv(taxonList, ranks)

df.to_csv(taxa_csv_path, index=False)
print('file saved', taxa_csv_path)
