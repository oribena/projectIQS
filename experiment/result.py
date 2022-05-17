import json
from warnings import catch_warnings
import pandas as pd
from csv import reader
import requests


def getURL_ALMIK(claim_id):
    claim_id = int(claim_id)
    #Convert to csv
    read_file = pd.read_csv('experiment/output/ALMIK_ranker_iter5_label20_active_iter3/ALMIK_iter3_label300_active_iter5_label20.txt', skiprows=6,  delim_whitespace=True, header=None, names=range(27) )
    read_file.to_csv (r'experiment/output/ALMIK_ranker_iter5_label20_active_iter3/res.csv', index=None)
    #Filter by claim_id
    Blast = pd.read_csv('experiment/output/ALMIK_ranker_iter5_label20_active_iter3/res.csv')
    df = Blast.loc[Blast["0"] == claim_id]
    df.to_csv (r'experiment/output/ALMIK_ranker_iter5_label20_active_iter3/res2.csv', index=None)
    #Sort the csv
    sorted_df = df.sort_values(by=["2"], ascending=True)
    sorted_df.to_csv (r'experiment/output/ALMIK_ranker_iter5_label20_active_iter3/res3.csv', index=None)
    #Get top 10 post ID 
    df = pd.read_csv('experiment/output/ALMIK_ranker_iter5_label20_active_iter3/res3.csv', nrows=20, header=None) 
    df_list = df[1].tolist()[1:]
    res = load_source(df_list)
    return res[:10]

def getURL_IQS(claim_id):
    claim_id = int(claim_id)
    #Convert to csv
    read_file = pd.read_csv('experiment/IQS_res/trec2012_eval_black_box_wmd_iter_1_labeling_10.txt', skiprows=6,  delim_whitespace=True, header=None, names=range(27) )
    read_file.to_csv (r'experiment/IQS_res/res.csv', index=None)
    #Filter by claim_id
    Blast = pd.read_csv('experiment/IQS_res/res.csv')
    df = Blast.loc[Blast["0"] == claim_id]
    df.to_csv (r'experiment/IQS_res/res2.csv', index=None)
    #Sort the csv
    sorted_df = df.sort_values(by=["2"], ascending=True)
    sorted_df.to_csv (r'experiment/IQS_res/res3.csv', index=None)
    #Get top 10 post ID 
    df = pd.read_csv('experiment/IQS_res/res3.csv', nrows=20, header=None) 
    df_list = df[1].tolist()[1:]
    res = load_source(df_list)
    return res[:10]


def load_source (list):
    URL = []
    HTML = []
    for id in list:
        read_file = pd.read_csv('Datasets/TREC_microblog_2012/posts.csv')
        df = read_file.loc[read_file["post_id"] == id]
        # print(df)
        # print(df["url"].values)
        url = df["url"].values[0]
        if url is not None:
            URL.append(url)
            html = get_tweet_html(url)
            if html is not None: 
                HTML.append(html)
    # print(URL)
    # print(HTML)

    return HTML
    
def get_tweet_html(url):
    # print("get_tweet_html")
    embed_api = 'https://publish.twitter.com/oembed'
    params = {
        'url': url,
        'partner': '',
        'hide_thread': False,
        'maxheight': 200,
        'limit': 1,
        'cards': 'hidden',
    }
    headers = {
        'Accept-Encoding': 'json'
    }
    try:
        json_res = requests.get(embed_api, params=params, headers=headers).json()
        y = json.dumps(json_res)
        check_json = json.loads(y)
        if "html" in check_json:
            res = json_res['html']
        else:
            res = None
        # print(res)
        return res
    except:
        return None


# getURL_ALMIK(51)
# getURL_IQS(51)

def get_claims ():
    all_claims = []
    with open('Datasets/TREC_microblog_2012/claims.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            if row[0] != "claim_id":
                json = {"claim_id":row[0], "title":row[1], "description": row[2]}
                all_claims.append(json)
    # print(all_claims)
    return(all_claims)
    
# get_claims()
