import unittest
import redditstats.connect as connect

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
        
if __name__ == '__main__':
    unittest.main()
