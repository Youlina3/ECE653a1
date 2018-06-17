import unittest
import wlang.ast as ast
import wlang.undef_visitor as undef_visitor

class TestStatsVisitor (unittest.TestCase):

#statementlist
    def test_asg (self):
        prg1 = "x := 10; y := x + z"
        ast1 = ast.parse_string (prg1)

        uv = undef_visitor.UndefVisitor ()
        uv.check (ast1)
        # UNCOMMENT to run the test
        self.assertEquals (set ([ast.IntVar('z')]), uv.get_undefs ())

    def test_havoc(self):
        prg2 = "havoc x, y, z"
        ast2 = ast.parse_string(prg2)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast2)
#check if there is an empty set
        self.assertEquals(0, len(uv.get_undefs()))

    def test_skip(self):
        prg3 = "skip"
        ast3 = ast.parse_string(prg3)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast3)
#check if there is an empty set
        self.assertEquals(0, len(uv.get_undefs()))

    def test_assert(self):
        prg4 = "assert x < y"
        ast4 = ast.parse_string(prg4)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast4)
#check if there is an empty set
        self.assertEquals(set([ast.IntVar('x'), ast.IntVar('y')]), uv.get_undefs())

    def test_assume(self):
        prg5 = "assume x < 3"
        ast5 = ast.parse_string(prg5)
        print ast5
        uv = undef_visitor.UndefVisitor()
        uv.check(ast5)
#check if there is an empty set
        self.assertEquals(set([ast.IntVar('x')]), uv.get_undefs())

    def test_if(self):
        prg6 = "if true then x := z + 5 else x := 6"
        ast6 = ast.parse_string(prg6)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast6)
#check if there is an empty set
        self.assertEquals(set([ast.IntVar('z')]), uv.get_undefs())

    def test_while(self):
        prg7 = "while true do x := k +3 "
        ast7 = ast.parse_string(prg7)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast7)
#check if there is an empty set
        self.assertEquals(set([ast.IntVar('k')]), uv.get_undefs())



    def test_while_if(self):
        prg1 = "x := 5; " \
           "while x >= 0 do {" \
           "  if false then {" \
           "    if x > 1 then m := 0" \
           "    else m := 1" \
           "  } " \
           "};" \
           "y := m + k"
        ast1 = ast.parse_string(prg1)
        uv = undef_visitor.UndefVisitor()
        uv.check(ast1)
        self.assertEquals({ast.IntVar('m'), ast.IntVar('k')}, uv.get_undefs())
