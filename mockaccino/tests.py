# -*- coding: utf-8 -*-
'''
Copyright (c) 2010, Rhomobile, Inc.

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

import unittest
import mockaccino
from mockaccino.matchers import any

from nose.tools import raises


class MockTests(unittest.TestCase):
    class MockedClass(object):
        def __init__(self): pass

        def method_that_returns_an_int(self): pass

        def method_with_no_return_value(self): pass

        def method_with_parameter(self, parameter): pass

        def method_with_two_parameters(self, a, b): pass

    @raises(mockaccino.UnexpectedCallError)
    def test_unexpected_call_raises_error_on_replay_mode(self):
        '''
        An UnexpectedCallError should be raised if the mock is on replay
        mode and an unexpected method is invoked
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mockaccino.replay(mock)

        # this is unexpected and should raise an error
        mock.method_that_returns_an_int()

    def test_unexpected_call_never_happens_on_record_mode(self):
        '''
        Calls on record mode never raise errors
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # This is okay, the method is on record mode
        mock.method_that_returns_an_int()

    def test_expected_call_raises_no_error(self):
        '''
        A call to an expected method should not raise an error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_that_returns_an_int()

        mockaccino.replay(mock)

        mock.method_that_returns_an_int()

    @raises(mockaccino.UnexpectedCallError)
    def test_mismatched_method_name_raises_unexpected_call_error(self):
        '''
        A call to a method different to what was recorded should raise
        an unexpected call error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_that_returns_an_int()

        mockaccino.replay(mock)

        # Invoking a different method should raise an error
        mock.method_with_no_return_value()

    @raises(mockaccino.UnexpectedCallError)
    def test_mismatched_parameter_raises_unexpected_call_error(self):
        '''
        A call to a method with diferent arguments than what was recorded
        should raise an unexpected call error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(1)

        mockaccino.replay(mock)

        # Invoking the same method with a different paramenter should raise
        mock.method_with_parameter(2)

    def test_correct_parameter_raises_no_error(self):
        '''
        A call to a method with the same arguments as was recorded should raise
        no errors
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(1)

        mockaccino.replay(mock)
        mock.method_with_parameter(1)

    @raises(mockaccino.UnexpectedCallError)
    def test_mismatched_kwargs_raises_unexpected_call_error(self):
        '''
        A call to a method with diferent kwargs than what was recorded
        should raise an unexpected call error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(parameter=1)

        mockaccino.replay(mock)

        # Invoking the same method with a different paramenter should raise
        mock.method_with_parameter(parameter=2)

    def test_correct_kwargs_raises_no_error(self):
        '''
        A call to a method with the same kwargs was recorded should raise
        no errors
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(parameter=1)
        mockaccino.replay(mock)
        mock.method_with_parameter(parameter=1)

    def test_mixed_args_and_kwargs(self):
        '''
        Expectations should work for calls that mix args and kwargs
        '''
        mock = mockaccino.create_mock(self.MockedClass)
        mock.method_with_two_parameters(1, key="cat")
        mockaccino.replay(mock)
        mock.method_with_two_parameters(1, key="cat")

    @raises(mockaccino.UnexpectedCallError)
    def test_mixed_args_and_kwargs_wrong_parameters(self):
        '''
        Mismatched args and kwargs should raise errors
        '''
        mock = mockaccino.create_mock(self.MockedClass)
        mock.method_with_two_parameters(1, key="cat")
        mockaccino.replay(mock)
        mock.method_with_two_parameters(1, key="dog")

    @raises(mockaccino.UnexpectedCallError)
    def test_wrong_argument_order_raises_unexpected_call_error(self):
        '''
        An unexpected call error should be raised if a method mock is invoked
        with a wrong argument order
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_two_parameters(0, 1)

        mockaccino.replay(mock)

        # Invoking the same method with a different order should raise
        mock.method_with_two_parameters(1, 0)

    @raises(mockaccino.UnexpectedCallError)
    def test_repeating_previously_expected_call_raises_error(self):
        '''
        An equal, with same parameters, unexpected call after an
        expected call raises an error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(0)
        mock.method_with_parameter(1)

        mockaccino.replay(mock)

        # Second invocation the same call, but it's unexpected
        mock.method_with_parameter(0)
        mock.method_with_parameter(0)

    @raises(mockaccino.UnexpectedCallError)
    def test_same_call_wrong_params_after_expected_call_raises_error(self):
        '''
        Am equal, but with differente parameters, unexpected call after an
        expected call raises an error
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(0)
        mock.method_with_parameter(1)

        mockaccino.replay(mock)

        # Second invocation the same call, but it's unexpected
        mock.method_with_parameter(0)
        mock.method_with_parameter(2)

    def test_times_mock_method_modifier(self):
        '''
        The times() mock method modifier should allow multiple calls
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(0).times(2)

        mockaccino.replay(mock)

        # Second invocation is legal, as mock is recorded with times modifier
        mock.method_with_parameter(0)
        mock.method_with_parameter(0)

    @raises(mockaccino.UnexpectedCallError)
    def test_calling_more_times_than_specified_raises_error(self):
        '''
        If the method is called more times than specified, an error
        should be raised
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(0).times(2)

        mockaccino.replay(mock)

        # Second invocation is legal, as mock is recorded with times modifier
        mock.method_with_parameter(0)
        mock.method_with_parameter(0)
        mock.method_with_parameter(0)

    def test_call_after_times_modifier(self):
        '''
        After a method is called enough times, the next expectiation should be set
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(0).times(2)
        mock.method_with_two_parameters(0, 1)

        mockaccino.replay(mock)

        # Second invocation is legal, as mock is recorded with times modifier
        mock.method_with_parameter(0)
        mock.method_with_parameter(0)
        mock.method_with_two_parameters(0, 1)

    @raises(ValueError)
    def test_will_raise(self):
        '''
        Mock methods configured to raise errors should do so when invoked
        '''
        mock = mockaccino.create_mock(self.MockedClass)
        mock.method_that_returns_an_int().will_raise(ValueError)
        mockaccino.replay(mock)
        mock.method_that_returns_an_int()

    def test_will_return_single_call(self):
        '''
        A mock method modified with will_return should return the correct
        value
        '''
        mock = mockaccino.create_mock(self.MockedClass)
        mock.method_that_returns_an_int().will_return(1)
        mockaccino.replay(mock)
        assert mock.method_that_returns_an_int() == 1

    def test_will_return_two_calls(self):
        '''
        A mock method modified with will_return should return the correct
        value on two different calls for the same method
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_that_returns_an_int().will_return(1)
        mock.method_that_returns_an_int().will_return(2)

        mockaccino.replay(mock)

        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 2

    def test_will_return_and_times_modifier(self):
        '''
        will_return should work with times modifier
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_that_returns_an_int().will_return(1).times(2)

        mockaccino.replay(mock)

        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 1

    def test_mockaccino_warps_math(self):
        '''
        mockaccino should be able to distort math to do my bidding
        '''
        class Calc(object):
            def sum(self, a, b):
                return a + b

            def is_even(self, n):
                return n % 2 == 0

        calc = Calc()

        assert calc.sum(2, 2) == 4
        assert calc.sum(1, 1) == 2
        assert calc.is_even(2)

        mock = mockaccino.create_mock(Calc)

        mock.sum(2, 2).will_return(5)
        mock.sum(1, 1).will_return(-1)
        mock.is_even(2).will_return(False)

        mockaccino.replay(mock)

        # BAM! 2 + 2 is now 5!
        assert mock.sum(2, 2) == 5

        # PRESTO! 1 + 1 is now -1!
        assert mock.sum(1, 1) == -1

        # BAZINGA! 2 is now odd!
        assert mock.is_even(2) is False

    def test_mixed_repeated_and_single_calls(self):
        '''
        Testing multiple mixed operations
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_that_returns_an_int().will_return(1)
        mock.method_that_returns_an_int().will_return(2).times(2)
        mock.method_with_parameter(2).times(2)
        mock.method_with_two_parameters(3, 4).will_return("String").times(2)
        mock.method_with_no_return_value()

        mockaccino.replay(mock)

        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 2
        assert mock.method_that_returns_an_int() == 2
        mock.method_with_parameter(2)
        mock.method_with_parameter(2)
        assert mock.method_with_two_parameters(3, 4) == "String"
        assert mock.method_with_two_parameters(3, 4) == "String"
        mock.method_with_no_return_value()

    def test_mock_stringio_getvalue(self):
        '''
        Mockaccino should be able to mock StringIO from the standard library
        '''
        import StringIO

        mock = mockaccino.create_mock(StringIO.StringIO)
        mock.getvalue().will_return("mocked")
        mockaccino.replay(mock)
        assert mock.getvalue() == "mocked"

    @raises(ValueError)
    def test_mock_stringio_to_make_close_raise(self):
        '''
        Mockaccino should be able to mock raised errors on StringIO
        '''
        import StringIO

        mock = mockaccino.create_mock(StringIO.StringIO)
        mock.close().will_raise(ValueError)
        mockaccino.replay(mock)
        mock.close()

    def test_always_modifier(self):
        '''
        Always modifier should allow any number of method calls
        on no particular order
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        # method_with_parameter should be called before
        # method_with_no_return_value, and method_that_returns_an_int
        # may be called any times in between
        mock.method_that_returns_an_int().will_return(1).always()
        mock.method_with_parameter(2)
        mock.method_with_no_return_value()

        mockaccino.replay(mock)

        assert mock.method_that_returns_an_int() == 1
        mock.method_with_parameter(2)
        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 1
        mock.method_with_no_return_value()
        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 1
        assert mock.method_that_returns_an_int() == 1

    @raises(ValueError)
    def test_error_raised_when_trying_to_override_always(self):
        '''
        Overriding an always modifier should not be allowed
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_that_returns_an_int().will_return(1).always()
        mock.method_that_returns_an_int()

        # Last expectation is only saved on replay
        mockaccino.replay(mock)

    @raises(ValueError)
    def test_error_raised_when_overriding_recorded_with_always(self):
        '''
        Overriding previously recorded methods with always is not
        allowed either
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_that_returns_an_int()
        mock.method_that_returns_an_int().will_return(1).always()

        # Last expectation is only saved on replay
        mockaccino.replay(mock)

    @raises(ValueError)
    def test_only_exceptions_may_be_raised(self):
        '''
        Overriding previously recorded methods with always is not
        allowed either
        '''
        mock = mockaccino.create_mock(self.MockedClass)
        mock.method_that_returns_an_int().will_raise("")

    def test_code_example(self):
        '''
        Code example from README is correct
        '''
        class Calc(object):
            def sum(self, a, b):
                return a + b

            def is_even(self, n):
                return n % 2 == 0

        mock = mockaccino.create_mock(Calc)

        mock.sum(1, 1).will_return(3).always()
        mock.is_even(2).will_return(False)
        mock.is_even(3).will_return(True)

        mockaccino.replay(mock)

        assert mock.sum(1, 1) == 3
        assert not mock.is_even(2)
        assert mock.sum(1, 1) == 3
        assert mock.is_even(3)

        # Mocking functions
        def function():
            return 0

        function_mock = mockaccino.create_mock(function)

        function_mock().will_return(1)

        mockaccino.replay(function_mock)

        assert function_mock() == 1

    def test_mock_function(self):
        '''
        Function mock that returns a value is correct
        '''
        def function_to_mock():
            return 0

        mock = mockaccino.create_mock(function_to_mock)
        mock().will_return(1)
        mockaccino.replay(mock)
        assert mock() == 1

    @raises(mockaccino.UnexpectedCallError)
    def test_mock_unexpected_call_to_function(self):
        '''
        Unexpect call to function mock should also raise error
        '''
        def function_to_mock():
            return 0

        mock = mockaccino.create_mock(function_to_mock)
        mock(1)
        mockaccino.replay(mock)
        mock(2)

    @raises(ValueError)
    def test_will_raise_on_function_mock(self):
        '''
        will_raise modifier should work on function mocks
        '''
        def function_to_mock():
            return 0

        mock = mockaccino.create_mock(function_to_mock)
        mock().will_raise(ValueError)
        mockaccino.replay(mock)
        mock()

    def test_times_on_function_mock(self):
        '''
        times modifier should work on function mocks
        '''
        def function_to_mock():
            return 0

        mock = mockaccino.create_mock(function_to_mock)
        mock().will_return(1).times(2)
        mockaccino.replay(mock)
        assert mock() == 1
        assert mock() == 1

    def test_matcher_any_class(self):
        '''
        Tests "any" type matcher for classes
        '''
        def function_to_mock(self, cls):
            pass

        mock = mockaccino.create_mock(function_to_mock)
        mock(any(self.MockedClass)).times(2)

        mockaccino.replay(mock)

        mock(self.MockedClass())
        mock(self.MockedClass())

    @raises(mockaccino.UnexpectedCallError)
    def test_matcher_any_fails_on_different_class(self):
        '''
        The "any" type matcher should not match values with different classes
        '''
        def function_to_mock(self, cls):
            pass

        mock = mockaccino.create_mock(function_to_mock)
        mock(any(self.MockedClass))

        mockaccino.replay(mock)

        mock("not a mocked class!")

    def test_matcher_any_int(self):
        '''
        The "any" type matcher should also work for primitive types
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_with_parameter(any(int)).always()

        mockaccino.replay(mock)

        mock.method_with_parameter(0)
        mock.method_with_parameter(1)

    def test_mix_any_matcher_with_exact_value(self):
        '''
        Any matcher and exact value parameter expectations can be mixed
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_with_two_parameters(1, any(basestring)).always()

        mockaccino.replay(mock)

        mock.method_with_two_parameters(1, "a")
        mock.method_with_two_parameters(1, "cat")
        mock.method_with_two_parameters(1, "dog")

    @raises(mockaccino.UnexpectedCallError)
    def test_mix_any_matcher_with_exact_value_fails_on_different_value(self):
        '''
        Mixed any matcher and exact value parameter expectation must fail
        if exact value is different
        '''
        mock = mockaccino.create_mock(self.MockedClass)

        mock.method_with_two_parameters(1, any(basestring)).always()

        mockaccino.replay(mock)

        mock.method_with_two_parameters(2, "a")
