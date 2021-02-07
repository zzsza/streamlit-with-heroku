import streamlit as st
import collections
import functools
import inspect
import textwrap

def cache_on_button_press(label, **cache_kwargs):
    """Function decorator to memoize function executions.
    Parameters
    ----------
    label : str
        The label for the button to display prior to running the cached funnction.
    cache_kwargs : Dict[Any, Any]
        Additional parameters (such as show_spinner) to pass into the underlying @st.cache decorator.
    Example
    -------
    This show how you could write a username/password tester:
    >>> @cache_on_button_press('Authenticate')
    ... def authenticate(username, password):
    ...     return username == "buddha" and password == "s4msara"
    ...
    ... username = st.text_input('username')
    ... password = st.text_input('password')
    ...
    ... if authenticate(username, password):
    ...     st.success('Logged in.')
    ... else:
    ...     st.error('Incorrect username or password')
    """
    internal_cache_kwargs = dict(cache_kwargs)
    internal_cache_kwargs['allow_output_mutation'] = True
    internal_cache_kwargs['show_spinner'] = False
    
    def function_decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            @st.cache(**internal_cache_kwargs)
            def get_cache_entry(func, args, kwargs):
                class ButtonCacheEntry:
                    def __init__(self):
                        self.evaluated = False
                        self.return_value = None
                    def evaluate(self):
                        self.evaluated = True
                        self.return_value = func(*args, **kwargs)
                return ButtonCacheEntry()
            cache_entry = get_cache_entry(func, args, kwargs)
            if not cache_entry.evaluated:
                if st.button(label):
                    cache_entry.evaluate()
                else:
                    raise st.script_runner.StopException
            return cache_entry.return_value
        return wrapped_func
    return function_decorator

def display_func_source(func):
    code = inspect.getsource(confirm_button_example)
    code = '\n'.join(code.splitlines()[1:]) # remove first line
    st.code(textwrap.dedent(code))

if __name__ == '__main__':
    st.write("""
        This example shows a hack to create a "confirm button" in Streamlit, e.g.
        to authenticate a username / password pair.
        The correct answer is `buddha` / `s4msara`.
    """)
    display_func_source(confirm_button_example)
    confirm_button_example()
    
    
    
  