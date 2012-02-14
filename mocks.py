# -*- coding: utf-8 -*-

import inspect


def createMock(cls):
    '''
    Returns a mock object for the given class. The returned mock is on record
    mode by default
    '''

    if not inspect.isclass(cls):
        raise ValueError("Tried to mock something that is not a class")

    mock = Mock()

    for n, a in [(n, a) for (n, a) in inspect.getmembers(cls) if inspect.ismethod(a)]:
        try:
            setattr(mock, n, MockMethod(n, mock))
        except AttributeError:
            pass # read-only methods are not mocked

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


class MockMethod(object):
    '''
    Class used to override a mocked class' methods
    '''

    def __init__(self, name, parent):
        self.name = name
        self.__parent = parent

        self.__num_calls = 1
        self.__to_raise = None

    def __call__(self, *args, **kwargs):
        if self.__num_calls > 0:
            self.__num_calls -= 1

        return self.__parent._invoked(self, args, kwargs)

    def is_depleted(self):
        return self.__num_calls == 0

    def times(self, num_expected_calls):
        self.__num_calls = num_expected_calls

    def will_raise(self, error):
        self.__to_raise = error

    def should_raise(self):
        return self.__to_raise is not None

    def do_raise(self):
        raise self.__to_raise


class Mock(object):
    def __init__(self):
        self.__calls = []
        self.replay_mode = False

    def enter_replay_mode(self):
        self.replay_mode = True

    def _invoked(self, mock_method, args, kwargs):
        '''
        Method called by a mock's methods when they are invoked. It checks
        the method's name, its arguments and keyword arguments. The order
        of arguments does matter, the order of keyword arguments doesn't.
        '''
        if self.replay_mode:
            if not self.__calls:
                raise UnexpectedCallError("No more method calls are expected")

            expected_name, expected_args, expected_kwargs = self.__calls[0]

            if mock_method.is_depleted():
                del self.__calls[0]

            if (mock_method.name != expected_name or args != expected_args or
                kwargs != expected_kwargs):
                raise UnexpectedCallError("Unexpected method call. Expected \
                        %s(args=%s, kwargs=%s], got %s(args=%s, kwargs=%s)." %
                        (expected_name, expected_args.__str__,
                         expected_kwargs.__str__, mock_method.name,
                         args.__str__, kwargs.__str__))

            if mock_method.should_raise():
                mock_method.do_raise()
        else:
            self.__calls.append((mock_method.name, args, kwargs))

            return mock_method
