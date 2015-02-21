import random

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

import connect
import comments
import subreddit
import util

def generate_cdf(df, column='score'):
    '''
    Given a dataframe this function will plot and show 
    a cdf for the column passed in
    '''
    
    title = 'CDF for {}'.format(column)
    df['score'].hist(cumulative=True, normed=1, bins=100).set_title(title)
    plt.show()
    return
     

def get_user_comment_activity(sub_name='soccer', limit=100, start=None, end=None):
    '''
    Returns a dataframe containing entries for user's recent comment activity
    The comments are pulled from the newest (limit) threads
    '''
    conn = connect.create_connection()
    if end:
        submissions = subreddit.get_submission_by_date(conn, sub_name, end, 
          start=start, limit=limit)
    else:
        submissions = subreddit.get_posts(conn, sub_name, limit=limit)
    stats = {}
    processed = 0
    for submission in submissions:
        processed += 1
        util.stats_update(processed)
        sub_stats = comments.get_user_comment_summary(submission)
        for u in sub_stats:
            if u not in stats:
                stats[u] = sub_stats[u]
            else:
                for k in sub_stats[u]:
                     stats[u][k] += sub_stats[u][k]
    df = convert_stats_to_dataframe(stats)
    return df

def convert_stats_to_dataframe(stats, sort='score', limit=None):
    '''
    Takes a dictionary of statistics and converts it to a dataframe.
    All dictonary entries are assumed to be objects with the same keys.
    The dictionary keys are inserted into the object in the field 'name'
    '''

    for k,v in stats.iteritems():
        v['name'] = k
    data = stats.values()
    columns = stats[random.choice(stats.keys())].keys()
    df = pd.DataFrame(data, columns=columns)
    if sort:
        df = df.sort(sort, ascending=False)
    if limit:
        df = df[:limit]
    return df
