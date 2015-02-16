import unittest
from mock import Mock
import random
import string
import arrow

import redditstats.connect as connect
import redditstats.subreddit as subreddit
import redditstats.comments as comments
import redditstats.stats as stats

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

    def test_get_submission_comment_summary(self):
        '''
        Tests the simple case that given a submission object with comments
        get_submission_comment_summary correctly returns a dict summarizing 
        the comments in a submission
        '''

        #Given
        sub_id = 'baz'
        true_values = {}
        mocked_submission = Mock()
        mocked_submission.replace_more_comments.return_value = None
        mocked_submission.id = sub_id
        true_values[sub_id] = {}
        true_values[sub_id]['count'] = 0
        true_values[sub_id]['score'] = 0
        true_values[sub_id]['total_len'] = 0 

        mocked_comments = []
        for a in ['foo', 'bar']:
            for i in range(random.randint(0,10)):
                ups = random.randint(0,100)
                downs = random.randint(0,10)
                created = random.randint(0,10000)
                body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1,200)))

                true_values[sub_id]['count'] += 1
                true_values[sub_id]['score'] += ups - downs
                true_values[sub_id]['total_len'] += len(body)

                comment = Mock()
                comment.author = a
                comment.ups = ups
                comment.downs = downs
                comment.created = created
                comment.body = body
                mocked_comments.append(comment)

        mocked_submission.comments = mocked_comments

        #When
        summary = comments.get_submission_comment_summary(mocked_submission)

        #Then
        self.assertEquals(summary, true_values)

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
            true_values[a]['total_len'] = 0 
            for i in range(random.randint(0,10)):
                ups = random.randint(0,100)
                downs = random.randint(0,10)
                created = random.randint(0,10000)
                body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1,200)))

                true_values[a]['count'] += 1
                true_values[a]['score'] += ups - downs
                true_values[a]['total_len'] += len(body)

                comment = Mock()
                comment.author = a
                comment.ups = ups
                comment.downs = downs
                comment.created = created
                comment.body = body
                mocked_comments.append(comment)

        mocked_submission.comments = mocked_comments

        #When
        summary = comments.get_user_comment_summary(mocked_submission)

        #Then
        self.assertEquals(summary, true_values)
     

class SubredditTests(unittest.TestCase):
    def test_get_submission_by_date(self):
        '''
        Given a list of submissions tests that get_submission_by_date
        returns only the submissions in the given interval
        '''
        #Given
        mocked_submissions = []

        interval_start = arrow.get('2015-02-05 00:00')
        interval_end = interval_start.replace(hours=24)

        generated_dates_start = interval_start.replace(hours=-24)
        generated_dates_end = interval_end.replace(hours=24)

        generated_dates = generated_dates_start.range('hour', generated_dates_start, end=generated_dates_end)
        interval_dates = interval_start.range('hour', interval_start, end=interval_end)

        for date in generated_dates:
            submission = Mock()
            submission.created = date.format('X')
            mocked_submissions.append(submission)

        conn = Mock()
        conn.get_subreddit.return_value = Mock()
        conn.get_subreddit.return_value.get_new.return_value = mocked_submissions

        end_str = interval_end.strftime('%Y-%m-%d %H:%M')
        start_str = interval_start.strftime('%Y-%m-%d %H:%M')

        #When
        submissions = subreddit.get_submission_by_date(conn, 'foo', end = end_str, start=start_str)
        
        #Then
        self.assertEquals(len(submissions), len(interval_dates))

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


    def test_get_posts_summary(self):
        '''
        Simple test to ensure that get_posts_summary correctly
        aggregates the stats
        '''
        #Given

        title ='test_post'
        sub_id = 'baz'
        true_values = {}
        mocked_submission = Mock()
        mocked_submission.replace_more_comments.return_value = None
        mocked_submission.id = sub_id
        mocked_submission.title = title
        true_values[sub_id] = {}
        true_values[sub_id]['count'] = 0
        true_values[sub_id]['score'] = 0
        true_values[sub_id]['total_len'] = 0 
        true_values[sub_id]['title'] = title

        mocked_comments = []
        for a in ['foo', 'bar']:
            for i in range(random.randint(0,10)):
                ups = random.randint(0,100)
                downs = random.randint(0,10)
                created = random.randint(0,10000)
                body = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(1,200)))

                true_values[sub_id]['count'] += 1
                true_values[sub_id]['score'] += ups - downs
                true_values[sub_id]['total_len'] += len(body)

                comment = Mock()
                comment.author = a
                comment.ups = ups
                comment.downs = downs
                comment.created = created
                comment.body = body
                mocked_comments.append(comment)

        mocked_submission.comments = mocked_comments
        conn = Mock()
        mocked_subreddit = Mock()
        mocked_subreddit.get_new.return_value = [mocked_submission]
        conn.get_subreddit.return_value = mocked_subreddit

        true_df = stats.convert_stats_to_dataframe(true_values)

        #When
        df = subreddit.get_posts_summary(conn, 'foo')
        #Then
        self.assertTrue((true_df.values == df.values).all())


if __name__ == '__main__':
    unittest.main()
