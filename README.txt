Mockaccino 0.1
by Paolo Victor - paolovictor@gmail.com

A Python mocking library with a syntax similar to the Easymock Java mocking library.

The basic way to use it is:

1. Create a mock object for the class you want to mock
2. Invoke methods on this mock, applying modifiers such as what the call will return and how many times it will happen
3. Put the mock on replay mode
4. Continue the test. Invocations to a mock object's methods will be matched sequentially, unless the call is recorded with an "always" modifier (more on that later)

Code example

    import mockaccino

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

    print mock.sum(1, 1) # Prints 3
    print mock.is_even(2) # Prints False
    print mock.sum(1, 1) # Prints 3
    print mock.is_even(3) # Prints True

    # Mocking functions
    def function():
        return 0
    
    function_mock = mockaccino.create_mock(function)
    
    function_mock.will_return(1)

    mockaccino.replay(function_mock)

    print function_mock() # Prints 1

Usage

Creating and changing mock state

* mockaccino.create_mock(class) - returns a mock object for the specified class or function
* mockaccino.replay(mock, ...) - sets one or more mocks on "replay mode", meaning that all upcoming calls will be matched against the recorded calls

Recording mocks

When a mock is not on replay mode and you call one of its methods, it will return an Expectation the represents an expected method call. For example:

    mock = mockaccino.create_mock(StringIO.StringIO)
    mock.getvalue()
    mock.replay()

Creates a mock for the StringIO.StringIO class, configures it to expect getvalue to be called once and puts it on replay mode. You may also specify parameters for the expectation, that will be matched on replay mode:

    mock = mockaccino.create_mock(Calc)
    mock.sum(2, 2)
    mock.replay()
    mock.sum(1, 2) # Will raise an UnexpectedCall error

Expectation modifiers

Besides defining the expected parameters for a method call, you may configure other behaviors like what values will be returned, how many calls are expected and whether the call will raise an error or not:

    mock = mockaccino.create_mock(Calc)
    mock.sum(2, 2).will_return(5)
    mock.sum(1, 1).will_return(2).times(2)
    mock.sum(0, "cat").will_raise(ValueError).always()
    mock.replay() 
    mock.sum(2, 2) # Will return 5, because I like it better this way
    mock.sum(1, 1)
    mock.sum(1, 1)
    mock.sum(1, 1) # This would raise an error, sum(1, 1) is expected only 2 times after sum(2, 2)
    mock.sum(0, "cat") # This would raise ValueError

Note that after setting an "always" modifier, you cannot record any other behaviors for the method or vice-versa.

The currently implemented expectation modifiers are:

* times(n) - "This method will be called n times"
* always() - "Whenever this method is called, this is the expected behavior"
* will_return(x) - "This method will return x"
* will_raise(e) - "This method will raise an error e"

Roadmap

1. Add support for "magic method" (__eq__, __str__, etc) mocking
2. Implement a "verify" method that checks if there are unmatched calls
