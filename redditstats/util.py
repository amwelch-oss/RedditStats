import sys

def status_update(count, thresh=10):
    '''
    Prints a "." every time count % thresh == 0
    Intended to give feedback to the user that the
    code is still running. Fetches can take a while
    because of Reddit's rate limiting
    '''
    if count % thresh == 0:
        sys.stdout.write('.')
