import seaborn as sns
from bs4 import BeautifulSoup
import re
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


def read_arxiv_file(path, columns=['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref', 'doi',
                                   'report-no', 'categories', 'license', 'abstract', 'versions',
                                   'update_date', 'authors_parsed'], count=None):
    data = []
    with open(path, 'r') as f:
        for idx, line in enumerate(f):
            if idx == count:
                break
            d = json.loads(line)
            d = {col: d[col] for col in columns}
            data.append(d)

    data = pd.DataFrame(data)
    return data


if __name__ == "__main__":
    data = read_arxiv_file('arxiv-metadata-oai-2019.json', ['id', 'authors', 'categories', 'authors_parsed'],
                           100000)

    data2 = data[data['categories'].apply(lambda x: 'cs.CV' in x)]

    all_authors = sum(data2['authors_parsed'], [])
    authors_names = [' '.join(x) for x in all_authors]
    authors_names = pd.DataFrame(authors_names)

    plt.figure(figsize=(10, 6))
    authors_names[0].value_counts().head(10).plot(kind='barh')

    plt.figure(figsize=(10, 6))
    authors_lastnames = [x[0] for x in all_authors]
    authors_lastnames = pd.DataFrame(authors_lastnames)
    authors_lastnames[0].value_counts().head(10).plot(kind='barh')

    plt.show()