import sys
import os
import pytest
import mock
import unittest
import requests
from requests.exceptions import HTTPError
from ..jerakia import Jerakia,JerakiaError

def func(x):
    return x + 1

def test_helper():
    assert func(3) == 5
