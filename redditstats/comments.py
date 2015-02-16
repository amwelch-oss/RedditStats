import random

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

def get_submission_comment_summary(submission):
    '''
    Takes a submission and returns a dict where the key equals
    the submission id and the value is a summary of the comments
    in the provided submission
    '''

    users = get_user_comment_summary(submission)

    #Combine the users into a single summary
    data = {}
    key = submission.id
    data[key] = {}

    if not users:
        return {}

    for k in users[random.choice(users.keys())].keys():
        data[key][k] = 0

    for user,entry in users.iteritems():
        for k,v in entry.iteritems():
            data[key][k] += v

    return data

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
            users[author]['total_len'] = 0
        users[author]['count'] += 1
        users[author]['score'] += int(comment.ups) - int(comment.downs)
        users[author]['total_len'] += len(comment.body)

    return users

