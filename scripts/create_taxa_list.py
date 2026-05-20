import utils

url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&project_id=260796'
taxa_csv_path = '../processed_data/San_Antonio_cnc_2026.csv'

url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&project_id=273661'
taxa_csv_path = '../processed_data/Taranaki_cnc_2026.csv'

url ='https://api.inaturalist.org/v1/observations/taxonomy?verifiable=true&spam=false&taxon_id=47120'
taxa_csv_path = '../processed_data/arthropod.csv'


print('start fetching')
taxonomy_data = utils.fetchData(url)
print('end fetching')

ranks = utils.getSortedRanks(taxonomy_data)
treeData = utils.buildTree(taxonomy_data, 'id', 'parent_id' )

taxonList = []
taxon = dict()
utils.flattenTree(treeData[0], taxonList, taxon)

df = utils.createTaxaListCsv(taxonList, ranks)

df.to_csv(taxa_csv_path, index=False)
print('file saved')
