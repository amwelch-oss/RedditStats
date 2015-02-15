
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
