'''
Matchers that allow more flexible value comparation on mock invocations
'''

def any(type_to_match):
    '''
    Returns a matcher that will match two values when they are of the same type
    '''
    class AnyMatcher(object):
        def __init__(self, cls):
            self.cls = cls

        def __eq__(self, other):
            return isinstance(other, self.cls)

    return AnyMatcher(type_to_match)
