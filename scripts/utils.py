import pandas as pd
import json
import requests


def fetchData(url):
    response = requests.get(url)
    return response.json()['results']


def downloadData(url, path):
    response = requests.get(url)
    json_data = response.json()
    with open(path, 'w') as f:
        json.dump(json_data, f)
    return json_data['results']


def buildTree(flatData, idField, parentIdField):
  nodeCache = dict()
  roots = []

  # populate nodeCache with all nodes
  for node in flatData:
    node['children'] = []
    nodeCache[node[idField]] = node

  # created nested tree
  for node in nodeCache.values():
    if parentIdField in node:
      parentId = node[parentIdField]
      if(parentId in nodeCache):
        parent = nodeCache[parentId]
        parent['children'].append(node)
      else:
        roots.append(node)
    else:
      roots.append(node)

  return roots


def flattenTree(node, taxonList, taxon, ranks):
    if(len(node['children']) > 0):
        for child in node['children']:
            prev_taxon = {**taxon}
            # remove ranks in prev_taxon that are lower than child rank
            if ('rank' in prev_taxon and ranks.index(prev_taxon['rank']) > ranks.index(child['rank'])):
                extra_ranks = ranks[ranks.index(prev_taxon['rank']):-1]
                for rank in extra_ranks:
                    if(rank in prev_taxon):
                        del prev_taxon[rank]

            taxon = {
                **prev_taxon,
                child['rank']: child['name'],
                "descendant_obs_count": child['descendant_obs_count'],
                "direct_obs_count": child['direct_obs_count'],
                "id": child["id"],
                "parent_id": child["parent_id"],
                'rank': child['rank'],
            }

            taxonList.append(taxon)

            flattenTree(child, taxonList, taxon, ranks)
    else:
        taxonList.append(taxon)


def log_df(df):
    print(df.shape)
    return df.head()


def getSortedRanks(flatNodes):
  ranksCache = dict()
  for node in flatNodes:
      ranksCache[node['rank']] = node['rank_level']

  sortedRanks = dict(sorted(ranksCache.items(), key=lambda item: item[1], reverse=True))
  if 'stateofmatter' in sortedRanks:
      del sortedRanks['stateofmatter']
  return list(sortedRanks.keys())


def createTaxaListCsv(taxonList, ranks):
    df = pd.DataFrame(taxonList)
    df = df.drop_duplicates()
    return  df[['id', 'parent_id', 'rank'] + ranks + ['descendant_obs_count', 'direct_obs_count']]


