import arrow

import comments
import stats
import util

def get_subreddit(conn, name):
    '''
    Returns an object containing the requested subreddit
    Takes the connection object and name of the subreddit
    '''

    return conn.get_subreddit(name)

def get_posts(conn, subreddit_name, limit=0):
    '''
    Returns a generator for the latest limit submissions
    to a subreddit
    '''

    sub = get_subreddit(conn, subreddit_name)
    return sub.get_new(limit=limit)


def get_posts_summary(conn, subreddit_name, limit=0):
    '''
    Returns a dataframe containing a summary of posts
    '''

    submissions = get_posts(conn, subreddit_name, limit=limit)

    data = {}
    count = 0 
    for submission in submissions:
        count += 1
        util.status_update(count)
        sub_stats = comments.get_submission_comment_summary(submission)
        sub_stats[submission.id]['title'] = submission.title
        data.update(sub_stats)

    df = stats.convert_stats_to_dataframe(data)
    return df
 
 
def get_submission_by_date(conn, sub_name, end, start=None, limit=0):
    '''
    Gets all submissions to a subreddit in the interval [start, end]
    Unfortunatly this loops through get_new until we hit the start of the interval.
    Be warned that this is very time intensive because of reddit's rate limit if 
    your start timestamp is far back in the past.
    Start and end can be in any form arrow.get can parse.
    Recomended %Y-%m-%d %H:%M:%S
    '''

    if start:
        start_ts = arrow.get(start)

    end_ts = arrow.get(end)
    posts = get_posts(conn, sub_name, limit=None)
    submissions_in_interval = []
    count = 0
    processed = 0
    for post in posts:
        processed += 1
        util.status_update(processed)
        ts = arrow.get(post.created)
        if ts > end_ts:
            break
        if start_ts and ts < start_ts:
            continue
        submissions_in_interval.append(post)
        if limit and count >= limit:
            break        

    return submissions_in_interval
