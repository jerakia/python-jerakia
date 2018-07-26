
import sys
import os
import pytest
from jerakia import Jerakia,JerakiaError

def func(x):
    return x + 1

def test_helper():
    assert func(3) == 5