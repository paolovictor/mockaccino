# -*- coding: utf-8 -*-
'''
Copyright (c) 2012, Paolo Victor.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
'''

import inspect


def create_mock(to_mock):
    '''
    Returns a mock object for the given class. The returned mock is on record
    mode by default
    '''
    mock = Mock()

    if inspect.isclass(to_mock):
        for n, a in [(n, a) for (n, a) in inspect.getmembers(to_mock)\
                                       if inspect.ismethod(a)]:
            try:
                setattr(mock, n, MockMethod(n, mock))
            except AttributeError:
                # Read-only methods are not mocked
                pass
    elif inspect.isfunction(to_mock):
        setattr(mock, '_called_as_function', MockMethod(to_mock.__name__, mock))
    else:
        raise ValueError("Only classes or functions may be mocked")

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
    def __init__(self, expected=None, got=None, message=None):
        super(Exception, message)
        self.expected = expected
        self.got = got

    def __str__(self):
        return "Expected %s, got %s" % (self.expected, self.got)


class Expectation(object):
    '''
    Represents an expectation about a method invocation
    '''
    ALWAYS = -1

    def __init__(self, method, args=None, kwargs=None):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.returns = False
        self.to_return = None
        self.to_raise = None
        self._times = 0

    def count_down(self):
        self._times -= 1

    def check(self, method, args, kwargs):
        if (self.method != method or self.args != args or
            self.kwargs != kwargs):
            raise UnexpectedCallError((self.method, self.args, self.kwargs),
                    (method, args, kwargs))

    def depleted(self):
        return self._times <= 0

    def outcome(self):
        if self.to_raise:
            raise self.to_raise
        elif self.returns:
            return self.to_return

    def is_always_expected(self):
        return self._times == Expectation.ALWAYS

    def will_return(self, value):
        self.returns = True
        self.to_return = value
        return self

    def will_raise(self, error):
        if not error or not isinstance(error, Exception):
            raise ValueError("Error paramenter should be an Exception or " +
                             "a subclass of it")

        self.to_raise = error
        return self

    def times(self, times):
        if times <= 0:
            raise ValueError("Number of times must be greater than zero")

        self._times = times
        return self

    def always(self):
        self._times = Expectation.ALWAYS

class MockMethod(object):
    '''
    Class used to override a mocked class' methods
    '''
    def __init__(self, name, parent):
        self.name = name
        self.__parent = parent

    def __call__(self, *args, **kwargs):
        return self.__parent._invoked(self, args, kwargs)


class Mock(object):
    def __init__(self):
        self.__current_expectation = None
        self.__expectations = []
        self.__always_expected = {}
        self.replay_mode = False

    def __save_current_expectation(self):
        if not self.__current_expectation:
            return

        method_name = self.__current_expectation.method
        recorded_methods = set((e.method for e in self.__expectations))

        if self.__current_expectation.is_always_expected():
            if method_name in recorded_methods:
                raise ValueError("Method already recorded without a " +
                                 "'always' modifier")

            self.__always_expected[method_name] = self.__current_expectation
        elif method_name in self.__always_expected:
            raise ValueError("Method already recorded with a " +
                             "'always' modifier")
        else:
            self.__expectations.append(self.__current_expectation)

    def enter_replay_mode(self):
        self.replay_mode = True

        if self.__current_expectation:
            self.__save_current_expectation()

    def _invoked(self, mock_method, args, kwargs):
        '''
        Method called by a mock's methods when they are invoked. It checks
        the method's name, its arguments and keyword arguments. The order
        of arguments does matter, the order of keyword arguments doesn't.
        '''
        if self.replay_mode:
            expectation = None

            # If the method has an "always" modifier, the next expectation
            # should not be dequeued
            if mock_method.name in self.__always_expected:
                expectation = self.__always_expected[mock_method.name]
            elif self.__expectations:
                expectation = self.__expectations[0]
            else:
                raise UnexpectedCallError("No more method calls are expected")

            expectation.check(mock_method.name, args, kwargs)

            # If the last method has no "always" modifier, its expected
            # call count should be decreased
            if not expectation.is_always_expected():
                expectation.count_down()

                if expectation.depleted():
                    del self.__expectations[0]

            return expectation.outcome()
        else:
            self.__save_current_expectation()

            self.__current_expectation = Expectation(mock_method.name,
                    args, kwargs)

            return self.__current_expectation

    def __call__(self, *args, **kwargs):
        '''
        Magic methods may only be changed on the class, before creating the
        object. This workaround redirects the __call__ to a bound method that
        may be changed after the object creation.
        '''
        return self._called_as_function(args, kwargs)

    def _called_as_function(self, *args, **kwargs):
        raise AttributeError("This method may only be called if overriden")
