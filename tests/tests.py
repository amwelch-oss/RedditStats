import unittest
from mock import Mock
import random

import redditstats.connect as connect
import redditstats.subreddit as subreddit
import redditstats.comments as comments

from collections import namedtuple

class ConnectionTests(unittest.TestCase):
    MAX_UA_LEN = 4096
    def test_user_agent(self):
        '''
        Tests that we properly construct the user-agent string. 
        '''
        
        #Given
        test_config_fields = [
            ("VERSION", "1.0"), 
            ("NAME", "FOO"), 
            ("DESCRIPTION", "THIS IS A THING"), 
            ("REDDIT_USER", "BAR")
        ]

        MockedConfigContainer = namedtuple('config', [x[0] for x in test_config_fields])
        mocked_config = MockedConfigContainer(*[x[1] for x in test_config_fields])

        #When
        ua = connect.form_user_agent(config_object = mocked_config)

        #Then
        for field in test_config_fields:
            self.assertTrue(field[1] in ua)

        self.assertTrue(len(ua) < self.MAX_UA_LEN)
        
class CommentTests(unittest.TestCase):
    def test_get_comment_info(self):
        '''
        Tests that given a comment object returns a dict 
        with stats about it
        '''
        
        #Given
        mocked_comment = Mock()
        mocked_comment.author = 'foo'
        mocked_comment.ups = 3
        mocked_comment.downs = 1
        mocked_comment.created = 123.0

        #When
        info = comments.get_comment_info(mocked_comment)

        #then
        self.assertEquals(info['author'], mocked_comment.author)
        self.assertEquals(info['score'], mocked_comment.ups - mocked_comment.downs)
        self.assertEquals(info['ts'], mocked_comment.created)

    def test_get_user_comment_summary(self):
        '''
        Tests the simple case that given a submission object with comments
        get_user_comment_summary correctly returns a dict of user activity
        '''

        #Given
        true_values = {}
        mocked_submission = Mock()
        mocked_submission.replace_more_comments.return_value = None

        mocked_comments = []
        for a in ['foo', 'bar']:
            true_values[a] = {}
            true_values[a]['count'] = 0
            true_values[a]['score'] = 0
            for i in range(random.randint(0,10)):
                ups = random.randint(0,10)
                downs = random.randint(0,10)
                created = random.randint(0,10000)

                true_values[a]['count'] += 1
                true_values[a]['score'] += ups - downs

                comment = Mock()
                comment.author = a
                comment.ups = ups
                comment.downs = downs
                comment.created = created
                mocked_comments.append(comment)

        mocked_submission.comments = mocked_comments

        #When
        summary = comments.get_user_comment_summary(mocked_submission)

        #Then
        self.assertEquals(summary, true_values)
     

class SubredditTests(unittest.TestCase):
    def test_get_subreddit(self):
        '''
        Tests that get_subreddit makes the correct call to praw
        '''
        #Given
        conn = Mock()
        conn.get_subreddit.return_value = True

        #When
        ret = subreddit.get_subreddit(conn, 'foo')

        #Then
        self.assertTrue(ret)

    def test_get_posts(self):
        '''
        Tests that get_posts makes the correct call to praw
        '''
        #Given
        conn = Mock()
        conn.get_subreddit.return_value = Mock()
        conn.get_subreddit.return_value.get_new.return_value = True

        #When
        ret = subreddit.get_posts(conn, 'foo')

        #Then
        self.assertTrue(ret)


if __name__ == '__main__':
    unittest.main()
