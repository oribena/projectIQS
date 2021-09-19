from iterative_query_selection import *
import pandas as pd
import json


class TwitterDataset:
    def __init__(self, input_path='Datasets/TREC_microblog_2012') -> None:
        super().__init__()
        self.input_path = Path(input_path)
        if not os.path.exists(self.input_path):
            raise FileExistsError()

        posts_df = pd.read_csv(self.input_path / 'posts.csv')
        jsons_str = posts_df.to_json(orient='records', lines=True)
        tweets = list(map(json.loads, jsons_str.split('\n')))
        for t in tweets:
            t['tweet'] = t['content']

        self.post_dictionary = self.build_post_dictionary(tweets)
        self.word_post_dictionary = self.build_word_post_dict_for_trec(tweets)
        pass

    def build_post_dictionary(self, tweets):
        return {t['post_id']: t for t in tweets}

    def build_word_post_dict_for_trec(self, tweets):
        word_post_dictionary = defaultdict(set)
        print("create words corpus")
        for post in tqdm(tweets, desc='process posts', total=len(tweets)):
            for word in clean_tweet(post['content']).lower().split(' '):
                word_post_dictionary[word].add(post['post_id'])
        return word_post_dictionary

    def get_posts_from_word_post_dict(self, words):
        post_sets = [self.word_post_dictionary[word] for word in words]
        if post_sets:
            result_post_ids = set.intersection(*post_sets)
            return [self.post_dictionary[post_id] for post_id in result_post_ids]
        else:
            return []

    def retrieve_tweets(self, query_str, max_num_tweets=20, hide_output=True, post_id_with_labels=None):
        posts = []
        post_id_set = set()
        keyword_list = [query_str.lower().split()]
        for keywords in keyword_list:
            result_posts = self.get_posts_from_word_post_dict(keywords)
            for post in result_posts:
                if len(posts) > max_num_tweets:
                    break
                if post['post_id'] not in post_id_set:
                    if post_id_with_labels is None or post['post_id'] in post_id_with_labels:
                        post_id_set.add(post['post_id'])
                        posts.append(post)
        return posts[:max_num_tweets]


if __name__ == "__main__":
    twitter_crawler = TwitterDataset()

    # twitter_crawler = TwitterCrawler(output_path='output/')
    relevance_evaluator = RelevanceEvaluator()
    #
    iqs = IterativeQuerySelection(relevance_evaluator, twitter_crawler, min_tweet_count=3, min_keywords_size=1)
    prototype = "British Government cuts"
    res = iqs.hill_climbing(prototype, search_count=3, iterations=15, keywords_start_size=3)
    print(res)
    #
    tweets = []
    max_tweets_per_query = 100
    for output_query in res:
        tweets.extend(twitter_crawler.retrieve_tweets(output_query, max_num_tweets=max_tweets_per_query))

    tweets_wmds = relevance_evaluator.eval_claim_tweets(prototype, tweets, use_mean=False)

    sorted_tweets = [x for _, x in sorted(zip(tweets_wmds, tweets), key=lambda pair: pair[0])]

    for i in range(min(5, len(sorted_tweets))):
        # get_tweet_html(sorted_tweets[i])
        print(sorted_tweets[i]['tweet'])
