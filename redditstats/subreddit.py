import comments
import stats

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
    for submission in submissions:
        sub_stats = comments.get_submission_comment_summary(submission)
        sub_stats['title'] = submission.title
        data.update(sub_stats)

    df = stats.convert_stats_to_dataframe(data)
    return df
    
