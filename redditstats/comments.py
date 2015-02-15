def get_comment_info(comment):
    '''
    Takes a comment object and returns a dict containing standardized information
    about the comment
    '''
    ret = {}
    ret['author'] = str(comment.author)
    ret['score'] = int(comment.ups) - int(comment.downs)
    ret['ts'] = int(comment.created)

    return ret

def get_user_comment_summary(submission):
    '''
    Takes a submission and returns a dict where 
    the key equals the username and the value is summary of that 
    users comment activity
    '''

    users = {}

    submission.replace_more_comments(limit=None)
    for comment in submission.comments:
        author =str(comment.author)
        if author not in users:
            users[author] = {}
            users[author]['count'] = 0
            users[author]['score'] = 0
        users[author]['count'] += 1
        users[author]['score'] += int(comment.ups) - int(comment.downs)
    return users

