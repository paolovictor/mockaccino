# -*- coding: utf-8 -*-

import inspect


def create_mock(cls):
    '''
    Returns a mock object for the given class. The returned mock is on record
    mode by default
    '''

    if not inspect.isclass(cls):
        raise ValueError("Tried to mock something that is not a class")

    mock = Mock()

    for n, a in [(n, a) for (n, a) in inspect.getmembers(cls)\
                                   if inspect.ismethod(a)]:
        try:
            setattr(mock, n, MockMethod(n, mock))
        except AttributeError:
            # Read-only methods are not mocked
            pass

    return mock


def replay(*args):
    '''
    Sets the specified mocks on replay mode, meaning that all method calls
    will be checked against what was previously recorded
    '''
    for mock in args:
        mock.enter_replay_mode()


class UnexpectedCallError(Exception):
    '''
    Exception thrown when an unexpected call is invoked on a moc
    '''
    pass


class Expectation(object):
    def __init__(self, method, args=None, kwargs=None, returns=False,
                 to_return=None, to_raise=None, times = 0):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.returns = returns
        self.to_return = to_return
        self.to_raise = to_raise
        self.times = 0

    def count_down(self):
        self.times -= 1

    def check(self, method, args, kwargs):
        if (self.method != method or self.args != args or
            self.kwargs != kwargs):
            raise UnexpectedCallError()

    def depleted(self):
        return self.times <= 0
           
    def outcome(self):
        if self.to_raise:
            raise self.to_raise
        elif self.returns:
            return self.to_return

    def returns(self):
        return self.returns

    def will_return(self, value):
        self.returns = True
        self.to_return = value

    def will_raise(self, error):
        self.to_raise = error


class MockMethod(object):
    '''
    Class used to override a mocked class' methods
    '''
    def __init__(self, name, parent):
        self.name = name
        self.__parent = parent

    def __call__(self, *args, **kwargs):
        return self.__parent._invoked(self, args, kwargs)

    def times(self, num_expected_calls):
        self.__parent._times(num_expected_calls)
        return self

    def will_raise(self, error):
        self.__parent._will_raise(error)
        return self

    def will_return(self, return_value):
        self.__parent._will_return(return_value)
        return self


class Mock(object):
    def __init__(self):
        self.__current_expectation = None
        self.__expectations = []
        self.replay_mode = False

    def enter_replay_mode(self):
        self.replay_mode = True

        if self.__current_expectation:
            self.__expectations.append(self.__current_expectation)
            

    def _invoked(self, mock_method, args, kwargs):
        '''
        Method called by a mock's methods when they are invoked. It checks
        the method's name, its arguments and keyword arguments. The order
        of arguments does matter, the order of keyword arguments doesn't.
        '''
        if self.replay_mode:
            if not self.__expectations:
                raise UnexpectedCallError("No more method calls are expected")

            expectation = self.__expectations[0]
            expectation.check(mock_method.name, args, kwargs)

            expectation.count_down()
            if expectation.depleted():
                del self.__expectations[0]

            if expectation.returns:
                return expectation.outcome()
            else:
                expectation.outcome()
        else:
            if self.__current_expectation:
                self.__expectations.append(self.__current_expectation)
    
            self.__current_expectation = Expectation(mock_method.name,
                    args, kwargs)

            return mock_method

    def _times(self, num_expected_calls):
        self.__current_expectation.times = num_expected_calls

    def _will_return(self, value):
        self.__current_expectation.will_return(value)
       
    def _will_raise(self, error):
        self.__current_expectation.will_raise(error) 
