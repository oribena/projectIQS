import os
import time
import uuid
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import flask
import threading
from flask import Flask, url_for, render_template, request, jsonify, send_from_directory
# import os, psutil
from iterative_query_selection import TwitterCrawler, RelevanceEvaluator, IterativeQuerySelection, get_tweet_html, \
    save_tweets_to_server

app = Flask(__name__)

tweets_generators = {}
search_wmd_updates_dict = defaultdict(list)
threads_dict = {}

twitter_crawler = TwitterCrawler(output_path='output/')
relevance_evaluator = RelevanceEvaluator()

executor = ThreadPoolExecutor(max_workers=4)


# def monitor_memory():
#     while True:
#         process = psutil.Process(os.getpid())
#         print("current memory: {}MB".format(process.memory_info().rss // 1000000))  # in bytes
#         time.sleep(10)
#
#
# monitor_thread = threading.Thread(target=monitor_memory)
# monitor_thread.start()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def read_chunks(fname, n):
    """Yield successive n-sized chunks from lst."""
    tweets = []
    with open(fname, encoding="utf8") as f:
        for line in f:
            tweets.append(json.loads(line))
            if len(tweets) >= n:
                yield tweets
                tweets = []
        yield tweets


@app.route('/')
def home_page():
    return render_template('home_page.html', search_id='', prototype_text='')


@app.route('/load_results', methods=['POST'])
def load_results():
    print("********** load result")
    # print(request)
    # print("request.data",request.data)
    # search_id = json.loads(request.data)['search_id']
    search_id = request.json["search_id"]
    print("search_id", search_id)
    tweet_gen = tweets_generators.get(search_id)
    try:
        tweet_chunk = next(tweet_gen)
        # print(tweet_chunk,"   ***********tweet_chunk")
        tweet_htmls = [get_tweet_html(t) for t in tweet_chunk]
        # print(tweet_htmls, "      **********tweet_htmls")
        return jsonify(tweet_htmls)
    except StopIteration as e:
        tweets_generators.pop(search_id)
        os.remove(f'output/tweets_{search_id}.json')
        return jsonify([])


def safe_remove_key_from_dict(key, dictionary):
    if key in dictionary:
        dictionary.pop(key)


@app.route('/close_search', methods=['POST'])
def close_search():
    print(request.data)
    search_ids = json.loads(request.data)['search_ids']
    for search_id in search_ids:
        safe_remove_key_from_dict(search_id, tweets_generators)
        safe_remove_key_from_dict(search_id, search_wmd_updates_dict)
        safe_remove_key_from_dict(search_id, threads_dict)
        if os.path.exists(f'output/tweets_{search_id}.json'):
            os.remove(f'output/tweets_{search_id}.json')
    return jsonify('stop_search')


def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s


@app.route('/stream')
def stream():
    search_id = request.args.get('search_id')

    def eventStream():
        print('run event stream')
        i = 0
        while True:
            time.sleep(0.2)
            if search_id in search_wmd_updates_dict:
                wmds = search_wmd_updates_dict.get(search_id)
                # print("wmds", wmds)
                counter = 0
                for wmd in wmds[i:]:
                    counter += 1
                    yield 'data: {}\n\n'.format(wmd)
                i += counter
            # else:
            #     break
            if search_id in threads_dict:
                t = threads_dict[search_id]
                # if not t.is_alive():
                if t.done():
                    yield 'data: {}\n\n'.format(-1)
                    threads_dict.pop(search_id)
                    break
    # print("response from eventStream", flask.Response(eventStream(), mimetype="text/event-stream"))
    return flask.Response(eventStream(), mimetype="text/event-stream")


@app.route('/get_id', methods=['POST'])
def get_search_id():
    prototype = json.loads(request.data)['prototype']
    search_id = get_uuid_for_prototype(prototype)
    return jsonify(search_id)


def get_uuid_for_prototype(prototype):
    # return str(uuid.uuid3(uuid.NAMESPACE_DNS, prototype))
    return str(uuid.uuid1())


@app.route('/js/Chart.js')
def send_js():
    return send_from_directory('js', 'Chart.js')

@app.route('/search', methods=['POST'])
def search():
    global relevance_evaluator
    global twitter_crawler

    # print(request.form)
    # print(request.data)
    prototype_text = request.json["form"]['text']
    min_tweet_count = int(request.json["form"]['min_tweet_count'])
    iterations = int(request.json["form"]['iterations'])
    keywords_start_size = int(request.json["form"]['keywords_start_size'])
    output_keywords_count = int(request.json["form"]['output_keywords_count'])
    search_count = int(request.json["form"]['search_count'])
    max_tweets_per_query = int(request.json["form"]['max_tweets_per_query'])

    if prototype_text != '':
        search_id =  request.json["form"]['search_id']
        print("searchID", search_id)
        args = (
            search_id, iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
            prototype_text, search_count, twitter_crawler, relevance_evaluator
        )
        future = executor.submit(run_iqs_search, *args)
        threads_dict[search_id] = future

        # t = threading.Thread(target=run_iqs_search, args=(
        #     search_id, iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
        #     prototype_text, search_count, twitter_crawler, relevance_evaluator))
        # t.start()
        # threads_dict[search_id] = t

        # run_iqs_search(iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
        #                prototype_text, relevance_evaluator, search_count, twitter_crawler)
        return 'Done'
    else:
        return 'failed'


# @app.route('/search', methods=['POST'])
# def search():
#     global relevance_evaluator
#     global twitter_crawler

#     print(request.form)
#     # print(request.data)
#     prototype_text = request.form.get('prototype', '')
#     min_tweet_count = int(request.form.get('min_tweet_count', 3))
#     iterations = int(request.form.get('iterations', 15))
#     keywords_start_size = int(request.form.get('keywords_start_size', 3))
#     output_keywords_count = int(request.form.get('output_keywords_count', 3))
#     search_count = int(request.form.get('search_count', 1))
#     max_tweets_per_query = int(request.form.get('max_tweets_per_query', 50))

#     if prototype_text != '':
#         search_id = request.form.get('search_id')
#         args = (
#             search_id, iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
#             prototype_text, search_count, twitter_crawler, relevance_evaluator
#         )
#         future = executor.submit(run_iqs_search, *args)
#         threads_dict[search_id] = future

#         # t = threading.Thread(target=run_iqs_search, args=(
#         #     search_id, iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
#         #     prototype_text, search_count, twitter_crawler, relevance_evaluator))
#         # t.start()
#         # threads_dict[search_id] = t

#         # run_iqs_search(iterations, keywords_start_size, max_tweets_per_query, min_tweet_count, output_keywords_count,
#         #                prototype_text, relevance_evaluator, search_count, twitter_crawler)
#         return 'Done'
#     else:
#         return 'failed'

# json["form"]['min_tweet_count']


def run_iqs_search(search_id, iterations, keywords_start_size, max_tweets_per_query, min_tweet_count,
                   output_keywords_count, prototype_text, search_count, twitter_crawler, relevance_evaluator):
    print("run IQS")
    search_wmd_updates = search_wmd_updates_dict[search_id]
    iqs = IterativeQuerySelection(relevance_evaluator, twitter_crawler, min_tweet_count=min_tweet_count)
    res = iqs.hill_climbing(prototype_text, search_count=search_count, iterations=iterations,
                            keywords_start_size=keywords_start_size,
                            output_keywords_count=output_keywords_count, search_wmd_updates=search_wmd_updates)
    # print(res)
    # print('*************************************')
    tweets = []
    for output_query in res:
        tweets.extend(
            twitter_crawler.retrieve_tweets(output_query, max_num_tweets=max_tweets_per_query, hide_output=True))
    print('Eval relevance')
    tweets_wmds = relevance_evaluator.eval_claim_tweets(prototype_text, tweets, use_mean=False)
    print('embed tweet into HTML tags')
    sorted_tweets = [x for _, x in sorted(zip(tweets_wmds, tweets), key=lambda pair: pair[0])]

    tweet_fname = f'output/tweets_{search_id}.json'
    save_tweets_to_server(tweet_fname, sorted_tweets)
    del iqs
    del sorted_tweets
    del tweets
    del tweets_wmds
    # tweets_generators[str(search_id)] = chunks(sorted_tweets, 4)
    tweets_generators[str(search_id)] = read_chunks(tweet_fname, 4)
    print(tweets_generators[str(search_id)], "tweets generator in searchIQS")
    search_wmd_updates_dict.pop(search_id)


if __name__ == '__main__':
    app.run()
