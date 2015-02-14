import config
import praw

def form_user_agent(config_object=config):
    '''
    Returns the user agent to use when connecting through the Reddit api
    following the guidelines outlined here: https://github.com/reddit/reddit/wiki/API
    '''
    user_agent = "{}.{}: {} For inquiries contact /u/{}"
    user_agent = user_agent.format(config_object.NAME, config_object.VERSION,\
     config_object.DESCRIPTION, config_object.REDDIT_USER)

def create_connection(reddit_interface=praw):
    '''
    Returns the reddit connection object initialized on success
    None of failure
    '''

    user_agent = form_user_agent()
    r = reddit_interface.Reddit(user_agent)
    return r
