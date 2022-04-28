import sys
import os
import csv
import re
import time
import math
import numpy as np
# import torch as th
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.auto import tqdm
from collections import defaultdict
from pathlib import Path
from sklearn.svm import SVC, LinearSVC
from scipy.spatial.distance import cdist

# !pip install tqdm nltk numpy scikit-learn

base_dataset_path = Path('Datasets/')
output_path = Path('output/')
dataset_path = base_dataset_path / 'TREC_microblog_2012'
# dataset_path = base_dataset_path / 'TREC_COVID_2019'

########## Load Data

claims_df = pd.read_csv(dataset_path / 'claims.csv')
posts_df = pd.read_csv(dataset_path / 'posts.csv')
posts_df['content'] = posts_df['content'].str.lower()
claims_df['keywords'] = claims_df['keywords'].str.lower()

claim_tweet_connection_df = pd.read_csv(dataset_path / 'claim_tweet_connection.csv')
merge_df = claim_tweet_connection_df.merge(claims_df, on='claim_id')[['claim_id', 'post_id', 'keywords']]
merge_df = merge_df.merge(posts_df, on='post_id')[['claim_id', 'post_id', 'keywords', 'content']]

########### Incremental MinHash Clustering
print("Incremental MinHash Clustering")

def get_min_hash(s):
    uni_grams = s.split()
    bi_grams = nltk.ngrams(uni_grams, 2)
    tri_grams = nltk.ngrams(uni_grams, 3)
    
    uni_hash_min = min(map(hash, uni_grams))
    bi_hash_min = min(map(hash, bi_grams)) if len(uni_grams) > 1 else hash('')
    tri_hash_min = min(map(hash, tri_grams)) if len(uni_grams) > 2 else hash('')
    
    return f'{uni_hash_min}{bi_hash_min}{tri_hash_min}'

# get_min_hash('British Government cuts')

class IncrementalMinHashClustering:
    
    def incremental_cluster(self, minhash_cluster_df):
        minhash_cluster_df = minhash_cluster_df.copy()
        cluster_df = minhash_cluster_df.groupby('cluster')[['str']].first().reset_index()        
        tf_idf_vals = TfidfVectorizer(stop_words='english', max_features=5000).fit_transform(cluster_df['str'].str.lower().fillna(''))

        cluster_view = np.copy(cluster_df['cluster'].values)
        for i in tqdm(range(len(cluster_df) - 1), desc='compute clusters', total=len(cluster_df)):
            mask = np.full(len(cluster_df), False, dtype=bool)
            mask[i+1:] = (cosine_similarity(tf_idf_vals[i], tf_idf_vals[i+1:], dense_output=True) >= 0.3)
            cluster_view[mask] = cluster_df['cluster'][i]
        
        cluster_map = dict(zip(cluster_df['cluster'], cluster_view))
        
        minhash_cluster_df['cluster'] = minhash_cluster_df['cluster'].map(cluster_map)        
        sorted_clusters = sorted(pd.unique(cluster_view))
        cluster_reset_map = dict(zip(sorted_clusters, range(len(sorted_clusters))))
        minhash_cluster_df['cluster'] = minhash_cluster_df['cluster'].map(cluster_reset_map)
        return minhash_cluster_df
    
    def fit_transform(self, strings, threshold = 0.3):        
        minhash_cluster_df = pd.DataFrame()
        minhash_cluster_df['str'] = strings
        minhash_cluster_df['hash'] = minhash_cluster_df['str'].apply(get_min_hash)
        unique_hashes = pd.unique(minhash_cluster_df['hash'])
        hashs_map = {h: i for i, h in enumerate(unique_hashes)}
        minhash_cluster_df['cluster'] = minhash_cluster_df['hash'].map(hashs_map)
        
        new_cluster_df = self.incremental_cluster(minhash_cluster_df)
        print('old', len(pd.unique(new_cluster_df['cluster'])), 'new', len(pd.unique(minhash_cluster_df['cluster'])))
              
        while len(pd.unique(new_cluster_df['cluster'])) < len(pd.unique(minhash_cluster_df['cluster'])):
            minhash_cluster_df = new_cluster_df
            new_cluster_df = self.incremental_cluster(minhash_cluster_df)
            print('old', len(pd.unique(new_cluster_df['cluster'])), 'new', len(pd.unique(minhash_cluster_df['cluster'])))
        return new_cluster_df['cluster'].values

########## Search Engine
print("Search Engine")

def build_post_dictionary(posts_df):
    return dict(zip(posts_df['post_id'], posts_df[['post_id', 'content']].itertuples(index=False)))

def build_word_post_dict_for_trec(posts_df):
    word_post_dictionary = defaultdict(set)
    posts = posts_df[['post_id', 'content']]
    print("create words corpus")
    for i, post in tqdm(posts.iterrows(), desc='process posts', total=len(posts)):
        for word in post['content'].split(' '):
            word_post_dictionary[word].add(post['post_id'])
    return word_post_dictionary    

def get_posts_from_word_post_dict(words, word_post_dictionary, post_dictionary):
    post_sets = [word_post_dictionary[word] for word in words]
    if post_sets:
        result_post_ids = set.intersection(*post_sets)
        return [post_dictionary[post_id] for post_id in result_post_ids]
    else:
        return []

def search_using_keyword_list(keyword_list, word_post_dictionary, post_dictionary):
    posts = []
    post_id_set = set()
    for keywords in keyword_list:
        result_posts = get_posts_from_word_post_dict(keywords, word_post_dictionary, post_dictionary)
        for post in result_posts:
            if post.post_id not in post_id_set:
                post_id_set.add(post.post_id)
                posts.append(post)
    return posts

word_post_dictionary = build_word_post_dict_for_trec(posts_df)
post_dictionary = build_post_dictionary(posts_df)

class SimpleSearchEngine:
    def __init__(self, posts_df):
        self.post_dictionary = self.build_post_dictionary(posts_df)
        self.word_post_dictionary = self.build_word_post_dict_for_trec(posts_df)
            
    def build_post_dictionary(self, posts_df):
        return dict(zip(posts_df['post_id'], posts_df[['post_id', 'content']].itertuples(index=False)))
    
    def build_word_post_dict_for_trec(self, posts_df):
        word_post_dictionary = defaultdict(set)
        posts = posts_df[['post_id', 'content']]
        print("create words corpus")
        for i, post in tqdm(posts.iterrows(), desc='process posts', total=len(posts)):
            for word in post['content'].split(' '):
                word_post_dictionary[word].add(post['post_id'])
        return word_post_dictionary
    
    def get_posts_from_word_post_dict(self, words):
        post_sets = [self.word_post_dictionary[word] for word in words]
        if post_sets:
            result_post_ids = set.intersection(*post_sets)
            return [self.post_dictionary[post_id] for post_id in result_post_ids]
        else:
            return []
        
    def search(self, keyword_list, post_id_with_labels=None):
        posts = []
        post_id_set = set()
        for keywords in keyword_list:
            result_posts = self.get_posts_from_word_post_dict(keywords)
            for post in result_posts:
                if post.post_id not in post_id_set:
                    if post_id_with_labels is None or post.post_id in post_id_with_labels:
                        post_id_set.add(post.post_id)
                        posts.append(post)
        return pd.DataFrame(posts)

######### Load document labels
print("Load document labels")

def get_topic_doc_rel_dict(qrels_file_path):
    judgment_df = pd.read_csv(qrels_file_path, delimiter=' ',
                              names=['topic', 'Q', 'docid', 'rel'])
    topic_doc_rel = {}
    for topic_id, post_osn_id, rel in judgment_df[['topic', 'docid', 'rel']].to_records(index=False):
        key = str(topic_id) + str(post_osn_id)
        topic_doc_rel[key] = rel if rel < 2 else 1
    return topic_doc_rel

topic_doc_rel = get_topic_doc_rel_dict(dataset_path / 'adhoc-qrels_filtered')
topic_doc_rel

def get_post_rel_to_claim(self, claim, p, topic_doc_rel):
    return topic_doc_rel['{}{}'.format(claim.claim_id, p.post_id)]

######### Experiment
print("Experiment")

claim_id = 51
# print("merge_df", merge_df)
claim_data_df = merge_df[merge_df['claim_id'] == claim_id]
# print("claim_data_df",claim_data_df)
init_keywords = np.array(claim_data_df['keywords'][0].split()).reshape(-1, 1)
# print("init_keywords", init_keywords)
posts_id_with_labels = set(merge_df['post_id'])

# se = SimpleSearchEngine(posts_df)

def simple_text_clean(s):
    # Cleans a string: Lowercasing, trimming, removing non-alphanumeric
    return " ".join(re.findall(r'\w+', s, flags=re.UNICODE)).lower()

tf_idf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tf_idf_vectorizer.fit(posts_df['content'].str.lower().fillna(''))

def active_search(claim_id, merge_df, init_keywords, se, tf_idf_vectorizer, topic_doc_rel, label_count=10, init_labels={}, iterations = 5):
    posts_id_with_labels = set(merge_df['post_id'])
    # retrive results with labels
    results = se.search(init_keywords, posts_id_with_labels)
    # label the results
    results['label'] = pd.Series(map(topic_doc_rel.get ,str(claim_id) + results['post_id'].astype(str)))
    results = results.dropna()

    # cluster the results
    clusters = IncrementalMinHashClustering().fit_transform(results['content'].values)
    results['cluster'] = clusters
    results['claim_id'] = claim_id
    
#     print(results)
    count_vectorizer = CountVectorizer(vocabulary=init_keywords.ravel())
    keyword_frec = count_vectorizer.transform(results['content']).sum(axis=1)
    results['keyword_frec'] = keyword_frec
    results.to_csv("res.csv")

    sorted_clustres = results.groupby('cluster')['keyword_frec'].sum().sort_values(ascending=False).reset_index()
    cluster_for_labeling = sorted_clustres['cluster'].tolist()[:label_count//2]
    cluster_for_labeling += sorted_clustres['cluster'].tolist()[-label_count//2:]
    seen_clusters = set()
    
    label_map = {}
    for c in sorted_clustres['cluster'].tolist()[:2//2]:
        label_map[c] = 1
    for c in sorted_clustres['cluster'].tolist()[-2//2:]:
        label_map[c] = 0 
#     print(label_map)
    true_clusters = {}
    
    
    temp_true_clusters = {}
    user_labels = {}
    user_labels.update(init_labels)
    
    cluster_idxs = {}
    results_without_labels = results[~results['post_id'].isin(user_labels)]
    for cluster, cluster_df in results_without_labels.groupby('cluster'):
        cluster_idxs[cluster] = 0
        
    print(results.shape)
    for i in range(iterations):
        print(f'iter {i}')
        seen_clusters = seen_clusters | set(cluster_for_labeling)
        
        results['anotator_label'] = results['cluster'].map(label_map)
        anotated_results = results[results['anotator_label'].notna()].copy().dropna()        
#         print(anotated_results)
#         print(label_map)
        true_clusters.update(dict(anotated_results[anotated_results['anotator_label'] == 1][['cluster', 'anotator_label']].itertuples(index=False, name=None)))
        
        # Add manual labels
#         if len(list(user_labels.keys())) > 0:
        anotated_results['anotator_label'] = anotated_results['anotator_label'].astype(int)
        current_labels = dict(anotated_results[['post_id', 'anotator_label']].itertuples(index=False, name=None))
        current_labels.update(user_labels)
        
        y_train  = [current_labels[x] for x in anotated_results['post_id']]
        print('classes', set(y_train))
    
        X_train = tf_idf_vectorizer.transform(anotated_results['content'])
#         y_train = anotated_results['anotator_label'].astype(int)

        X_test = tf_idf_vectorizer.transform(results['content'])
        y_test = results['label'].astype(int)
        
        if len(set(y_train)) == 1:
            y_pred = y_train[0]
            distances = 1
        else:
            svm = SVC(verbose=True)
            svm.fit(X_train, y_train)

            y_pred = svm.predict(X_test)
            print('Score', svm.score(X_test, y_test))
            distances = cdist(X_test.toarray(), svm.support_vectors_.toarray(), metric='euclidean').mean(axis=1)
                
#         print(sorted(distances))
        results['pred'] = y_pred
        results['distances'] = distances
        results['score'] = results['pred'] * results['distances']
        results['method'] = 'ALMIK'
        
        temp_true_clusters = dict(results[results['pred'] == 1][['cluster', 'pred']].itertuples(index=False, name=None))
#         print(results[['cluster', 'pred']])
#         print(len(temp_true_clusters.keys()))
    
        cluster_for_labeling = results.groupby('cluster')['distances'].mean().sort_values(ascending=True).reset_index()['cluster']
        cluster_for_labeling = cluster_for_labeling[cluster_for_labeling.isin(cluster_idxs)].tolist()[:label_count]
#         results[['claim_id', 'post_id', 'score', 'method']]
        
        train_df = results[results['cluster'].isin(cluster_for_labeling)]
        
#         print('cluster for labelsing', len(cluster_for_labeling))

        for cluster in cluster_for_labeling:
            cluster_df = results_without_labels[results_without_labels['cluster'] == cluster]
            
            tweet_row = cluster_df.iloc[cluster_idxs[cluster]]
            tweet_label = int(tweet_row['label'])
            tweet_id = tweet_row['post_id']
            
            user_labels[tweet_id] = tweet_label
            label_map[cluster] = tweet_label
            
            cluster_idxs[cluster] += 1
#             print('cluster idx',cluster_idxs[cluster],'cluster size', len(cluster_df))
            if cluster_idxs[cluster] == len(cluster_df):
                del cluster_idxs[cluster]
#                 print('del cluster', cluster, 'cluster count', len(cluster_idxs))
      
    
        
        label_map.update(true_clusters)
        label_map.update(temp_true_clusters)
#         print('#############################')
#         print(cluster_for_labeling)
#         print(len(temp_true_clusters))
# #         print(true_clusters)
#         print('#############################')
        
    return results, user_labels
    
# results, user_labels = active_search(claim_id, merge_df, init_keywords, se, tf_idf_vectorizer, topic_doc_rel, label_count=10)
# print(user_labels)

def word_rank(words, P, N):
    count_vectorizer = CountVectorizer(vocabulary=words, binary=True) 
    w_P_count = count_vectorizer.fit_transform(P).toarray()
    w_N_count = count_vectorizer.fit_transform(N).toarray()
    
    p_w_P = np.nan_to_num(w_P_count.mean(axis=0))
    p_w_N = np.nan_to_num(w_N_count.mean(axis=0))
#     print('p_w_P', p_w_P)
#     print('p_w_N', p_w_N)
#     print('np.log(p_w_P / p_w_N)', np.log(p_w_P / p_w_N))
    
    relEnt_w = np.nan_to_num(p_w_P * np.log(p_w_P / p_w_N))
    
    coverage_w = np.nan_to_num(w_P_count.sum(axis=0) / w_N_count.sum(axis=0))
    
#     print('relEnt_w', relEnt_w)
#     print('w_P_count.sum(axis=0)', w_P_count.sum(axis=0))
#     print('w_N_count.sum(axis=0)', w_N_count.sum(axis=0))
#     print('coverage_w', coverage_w)
    
    return np.nan_to_num(relEnt_w * np.exp(-1 / coverage_w))
    

word_rank(['cut', 'goverment'], merge_df['content'][:10000], merge_df['content'][10000:])

def combine_keywords(current, new):
    return np.unique(np.append(current.ravel(), new)).reshape(-1, 1)

posts_id_with_labels = set(merge_df['post_id'])
se = SimpleSearchEngine(posts_df)
tf_idf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tf_idf_vectorizer.fit(posts_df['content'].str.lower().fillna(''))
topic_doc_rel = get_topic_doc_rel_dict(dataset_path / 'adhoc-qrels_filtered')

######## The test
print("The test")

label_count=20 
ranker_iterations = 5
active_iterations = 3

output_dir = output_path / f'ALMIK_ranker_iter{ranker_iterations}_label{label_count}_active_iter{active_iterations}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for claim_id in tqdm(pd.unique(merge_df['claim_id']), desc='process claims'):
    
    init_labels={}
    claim_data_df = merge_df[merge_df['claim_id'] == claim_id]
#     print(claim_data_df['keywords'].values[0])
    init_keywords = np.array(claim_data_df['keywords'].values[0].split()).reshape(-1, 1)
#     print(init_keywords)
    
    for i in tqdm(range(1, active_iterations + 1), desc='active retrieval iter', total = active_iterations + 1):
        results, user_labels = active_search(claim_id, merge_df, init_keywords, se, tf_idf_vectorizer, 
                                             topic_doc_rel,label_count=label_count, 
                                             init_labels=init_labels, iterations=ranker_iterations)
        P = results[results['pred'] == 1]['content']
        N = results[results['pred'] == 0]['content']
#         print(results)
        cv = CountVectorizer()
        if len(P) > 0:
            cv.fit(P) 
        else:
            cv.fit(N) 
        vocab = np.array(list(cv.vocabulary_.keys()))
#         print(vocab)
        ranks = word_rank(vocab, P, N)

        new_keywords = vocab[np.argsort(ranks)[-10:]]

        init_keywords = combine_keywords(init_keywords, new_keywords)
        init_labels.update(user_labels)
        print('init_labels size', len(init_labels))
        results[['claim_id', 'post_id', 'score', 'method']].to_csv(f'{output_dir}/ALMIK_iter{i}_label{i*label_count*5}_active_iter5_label{label_count}.txt', sep=' ', index=False, header=None, mode='a')