#!/usr/bin/env python

import argparse
import praw

import connect
import subreddit
import stats

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def parse_args():
    p = argparse.ArgumentParser(description='''
        ''', formatter_class=argparse.RawTextHelpFormatter)
    args = p.parse_args()
    return args

def main():
    args = parse_args()

    conn = connect.create_connection()

    df = subreddit.get_posts_summary(conn, 'soccer', limit=10)
 
    print df
    stats.generate_cdf(df)

    return
    posts = subreddit.get_posts(conn, 'soccer', limit=100)
    for post in posts:
        #print post
        post.replace_more_comments(limit=None)
        for comment in post.comments:
            author = comment.author
            upvotes = comment.ups
            downvotes =comment.downs
            print "{} {} {}".format(upvotes, downvotes, author)
            #print "\t{}".format(comment)
        

if __name__ == '__main__':
    main()

