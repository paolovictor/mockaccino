# -*- coding: utf-8 -*-

import unittest
import mockaccino

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
