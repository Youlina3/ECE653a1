import unittest
from a1q3 import M

class CoverageTests (unittest.TestCase):
    def test_1 (self):
        """RT={[ "", 0],[ "a", 0],[ "ab", 0],[ "abc", 0]}"""
        o = M ()
        o.m("",0)
        o.m("a",0)
        o.m("ab",0)
        o.m("abc",0)
      
    def test_2 (self):
        """RT={[ "", 0],[ "a", 1],[ "ab", 1],[ "abc", 1]}"""
        o = M ()
        o.m("",0)
        o.m("a",1)
        o.m("ab",1)
        o.m("abc",1)
      
    def test_3 (self):
        """RT={[ "", 0],[ "a", 0],[ "ab", 0],[ "abc", 0],[ "", 1],[ "a", 1],[ "ab", 1]}"""
        o = M ()
        o.m("",0)
        o.m("a",0)
        o.m("ab",0)
        o.m("abc",0)
        o.m("",1)
        o.m("a",1)
        o.m("ab",1)
     
    def test_4 (self):
        """RT={[ "", 0],[ "a", 0],[ "ab", 0],[ "abc", 0],[ "", 1],[ "a", 1],[ "ab", 1], [ "abc", 1]}"""
        o = M ()
        o.m("",0)
        o.m("a",0)
        o.m("ab",0)
        o.m("abc",0)
        o.m("",1)
        o.m("a",1)
        o.m("ab",1)
        o.m("abc",1)
  
    
