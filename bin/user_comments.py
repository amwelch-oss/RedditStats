#!/usr/bin/env python

import argparse
import praw
import logging
import arrow
import ipdb

import pandas as pd
import numpy as np

import redditstats.stats
import redditstats.connect

def parse_args():
    parser = argparse.ArgumentParser(description='''
        ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('subreddit', action="store", type=str,
      help= "subreddit to look at")
    parser.add_argument('-s', '--start', type=str,
      help= "start of the submission interval, accepts any format arrow can parse")
    parser.add_argument('-e', '--end', type=str,
      help= "end of the submission interval, defaults to 1 day")
    parser.add_argument('-l', '--limit', type=int, default=100,
      help= "limit on the number of submissions searched")
    parser.add_argument('--df', action="store_true",
      help= "drops into an ipython shell with the result dataframe")
 
    args = parser.parse_args()
    return args

def get_posts_df(subreddit, start, end, limit=0):
    conn =  redditstats.connect.create_connection()
    return redditstats.stats.get_user_comment_activity(sub_name=subreddit,
      end=end, start=start, limit=limit)
def main():
    args = parse_args()
 
    if not args.start:
        start_ts = arrow.utcnow()
    else:
        start_ts = arrow.get(args.start)
        if not start_ts:
            logging.error("could not parse {}".format(args.start))
            return
            
    if not args.start:
        end_ts = arrow.utcnow().replace(days=-1)
    else:
        end_ts = arrow.get(args.end)
        if not start_ts:
            logging.error("could not parse {}".format(args.end))
            return
    
    df = get_posts_df(args.subreddit, args.start, args.end, limit=args.limit)
    if args.df:
        ipdb.set_trace()
        logging.info("The result dataframe is available as df")

    print df
    df.plot()    


if __name__ == '__main__':
    main()

