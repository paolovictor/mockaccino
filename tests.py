# -*- coding: utf-8 -*-

import unittest
import mockacino

from nose.tools import raises

class MockTests(unittest.TestCase):
    class MockedClass(object):
        def __init__(self): pass

        def method_that_returns_an_int(self): pass

        def method_with_no_return_value(self): pass

        def method_with_parameter(self, parameter): pass

        def method_with_two_parameters(self, a, b): pass

    @raises(mockacino.UnexpectedCallError)
    def test_unexpected_call_raises_error_on_replay_mode(self):
        '''
        An UnexpectedCallError should be raised if the mock is on replay
        mode and an unexpected method is invoked
        '''
        mock = mockacino.createMock(self.MockedClass)

        mockacino.replay(mock)

        # this is unexpected and should raise an error
        mock.method_that_returns_an_int()

    def test_unexpected_call_never_happens_on_record_mode(self):
        '''
        Calls on record mode never raise errors
        '''
        mock = mockacino.createMock(self.MockedClass)

        # This is okay, the method is on record mode
        mock.method_that_returns_an_int()

    def test_expected_call_raises_no_error(self):
        '''
        A call to an expected method should not raise an error
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_that_returns_an_int()

        mockacino.replay(mock)

        mock.method_that_returns_an_int()

    @raises(mockacino.UnexpectedCallError)
    def test_mismatched_method_name_raises_unexpected_call_error(self):
        '''
        A call to a method different to what was recorded should raise
        an unexpected call error
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_that_returns_an_int()

        mockacino.replay(mock)

        # Invoking a different method should raise an error
        mock.method_with_no_return_value()

    @raises(mockacino.UnexpectedCallError)
    def test_mismatched_parameter_raises_unexpected_call_error(self):
        '''
        A call to a method with diferent arguments than what was recorded
        should raise an unexpected call error
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(1)

        mockacino.replay(mock)

        # Invoking the same method with a different paramenter should raise
        mock.method_with_parameter(2)

    def test_correct_parameter_raises_no_error(self):
        '''
        A call to a method with the same arguments as was recorded should raise
        no errors
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(1)

        mockacino.replay(mock)

        mock.method_with_parameter(1)

    @raises(mockacino.UnexpectedCallError)
    def test_mismatched_kwargs_raises_unexpected_call_error(self):
        '''
        A call to a method with diferent kwargs than what was recorded
        should raise an unexpected call error
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(parameter=1)

        mockacino.replay(mock)

        # Invoking the same method with a different paramenter should raise
        mock.method_with_parameter(parameter=2)

    def test_correct_kwargs_raises_no_error(self):
        '''
        A call to a method with the same kwargs was recorded should raise
        no errors
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_parameter(parameter=1)

        mockacino.replay(mock)

        mock.method_with_parameter(parameter=1)

    @raises(mockacino.UnexpectedCallError)
    def test_wrong_argument_order_raises_unexpected_call_error(self):
        '''
        An unexpected call error should be raised if a method mock is invoked
        with a wrong argument order
        '''
        mock = mockacino.createMock(self.MockedClass)

        # Recorded a method with no return value
        mock.method_with_two_parameters(0, 1)

        mockacino.replay(mock)

        # Invoking the same method with a different order should raise
        mock.method_with_two_parameters(1, 0)
