# test_simple_pytest.py

"""
Using pytest library instead of unittest: simpler, no need to use classes
"""

import pytest #external, need to be installed with 'pip install'

import simple

def test_simple():
    assert simple.add(2,2) == 5

def test_str():
    assert simple.add('hello','world') == 'helloworld'