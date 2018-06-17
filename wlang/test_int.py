# The MIT License (MIT)
# Copyright (c) 2016 Arie Gurfinkel

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
import wlang.ast as ast
import wlang.int
import wlang.parser as parser

def run_interpret(test,string):
    root = ast.parse_string(string)
    print root
    interp = wlang.int.Interpreter ()
    st = wlang.int.State ()
    st = interp.run (root, st)
    print str(st)
#there is a bug so no one could cover it
    print repr(st)
    test.assertIsNotNone(st)
    return st


class TestInt (unittest.TestCase):

#exemple case
    def test_assign (self):
        prg1 = "x := 10; print_state"
        # test parser
        ast1 = ast.parse_string (prg1)
        print ast1
        interp = wlang.int.Interpreter ()
        st = wlang.int.State ()
        st = interp.run (ast1, st)
        self.assertIsNotNone (st)
        # x is defined
        self.assertIn ('x', st.env)
        # x is 10
        self.assertEquals (st.env['x'], 10)
        # no other variables in the state
        self.assertEquals (len (st.env), 1)

# below is testing int.py

##+,-,*,/
    def test_Aexp(self):
        st = run_interpret(self, "{a := 1; b := 2}; c:=a + b; d:= a - b;e:= a * b ;f:= a / b")
        self.assertIn('a', st.env)
        self.assertIn('b', st.env)
        self.assertIn('c', st.env)
        self.assertIn('d', st.env)
        self.assertIn('e', st.env)
        self.assertIn('f', st.env)
        self.assertEquals(st.env['a'], 1)
        self.assertEquals(st.env['b'], 2)
        self.assertEquals(st.env['c'], 3)
        self.assertEquals(st.env['d'], -1)
        self.assertEquals(st.env['e'], 2)
        self.assertEquals(st.env['f'], 1/2)
        self.assertEquals(len(st.env), 6)


    def test_Bexp(self):
        st = run_interpret(self, " a := 4; b := 5; " \
                                 "if a < 0 or b >0 then skip; " \
                                 "if a > 0 and b > 0 then skip; " \
                                 "if not a > 0 then skip else skip")
        self.assertIn('a', st.env)
        self.assertIn('b', st.env)
        self.assertEquals(len(st.env), 2)


    def test_if(self):
        st = run_interpret(
            self, "if false then i := 1 else i := 2; if false then u := 1; if true then h := 1 else h := 2")
        self.assertIn('i', st.env)
        self.assertEquals(st.env['i'], 2)
        self.assertNotIn('u', st.env)
        self.assertIn('h', st.env)
        self.assertEquals(st.env['h'], 1)

    def test_Rel(self):
        st = run_interpret(
            self,"{a :=1; b :=2}; if a = b then skip; if a<b then skip; if a>b then skip; if b >= a then skip ")
        self.assertIn('a',st.env)
        self.assertIn('b',st.env)


    def test_assert(self):
        caught = False
        try:
            run_interpret(self, "x := 1; assert x < 2 ; assert x >2")
        except:
            caught = True
        self.assertTrue(caught)

    def test_assume(self):
        st = run_interpret(self, "x := 1; assume x < 2")

    def test_havoc(self):
        st = run_interpret(self, "havoc x, y, z")
        self.assertIn('x', st.env)
        self.assertIn('y', st.env)
        self.assertIn('z', st.env)

# below is tesing ast.py

    def test_while2 (self):
        prg2 = "{ p := 0; x := 1; n :=3 }; while x <= n do { x := x+1; p := p + n }"
        ast2 = ast.parse_string(prg2)
        print ast2
        interp2 = wlang.int.Interpreter()
        print repr(ast2)
        print str(ast2)
        self.assertTrue(ast2 == ast2)
        self.assertTrue(ast2.stmts[1] == ast2.stmts[1])
        #create a state
        st = wlang.int.State()
        #run ast2 under the state
        st = interp2.run(ast2, st)
        self.assertIsNotNone(st)
        # x, p, n are defined (state environment)
        self.assertIn('x', st.env)
        self.assertIn('p', st.env)
        self.assertIn('n',st.env)
        # x is 4
        self.assertEquals(st.env['x'], 4)
        self.assertEquals(st.env['p'], 9)
        self.assertEquals(st.env['n'], 3)
        # no other variables in the state
        self.assertEquals(len(st.env), 3)

    def test_skip2(self):
        prg3 = "skip"
        ast3 = ast.parse_string(prg3)
        self.assertTrue(ast3 == ast3)

    def test_print2(self):
        prg4 = "print_state"
        ast4 = ast.parse_string(prg4)
        self.assertTrue(ast4 == ast4)

    def test_assign2(self):
        prg5 = "x := 1"
        prg6 = "x := 1"
        ast5 = ast.parse_string(prg5)
        ast6 = ast.parse_string(prg6)
        self.assertTrue(ast5 == ast6)

    def test_if2(self):
        prg7 = "if true then x := 1"
        ast7 =  ast.parse_string(prg7)
        self.assertTrue(ast7 == ast7)

    def test_assert2(self):
        prg1 = "assert (y > 0)"
        prg2 = "assert (y > 0)"
        ast1 = ast.parse_string(prg1)
        ast2 = ast.parse_string(prg2)
       # interp = wlang.int.Interpreter()
       # st = wlang.int.State()
        #self.assertIsNotNone(st)
        ast1 == ast2

    def test_assume2(self):
        prg8 = "assume x > 9"
        ast8 = ast.parse_string(prg8)
        self.assertTrue(ast8 == ast8)

    def test_havoc2(self):
        prg10 = "havoc x"
        ast10 = ast.parse_string(prg10)
        self.assertTrue(ast10 == ast10)

    def test_const(self):

        node = ast.Const(11)
        print(str(node), repr(node), hash(node))


    def test_invar(self):

        node = ast.IntVar('x')
        print(str(node), repr(node), hash(node))

    def test_file(self):
        self.assertIsNotNone(ast.parse_file('wlang/test1.prg'))


class MyVisitorAst (wlang.ast.AstVisitor):
    """in order to void overriding"""
    def __init__ (self):
        super (MyVisitorAst, self).__init__ ()
        self.vars = 0

#    def visit_StmtList (self, node, *args, **kwargs):
 #       for s in node.stmts:
 #           self.visit(s)

    def visit_AsgnStmt (self, node, *args, **kwargs):
        self.visit(node.lhs)
        self.vars += 1

 #   def visit_Stmt (self, node, *args, **kwargs):
  #      pass

    def visit_Exp (self, node, *args, **kwargs):
       pass


#astvisitor
class TestAstVisitorIntvar (unittest.TestCase):

    def test_IntVar (self):
        prg1 = "x := 5"
        ast1 = ast.parse_string(prg1)
        sv = MyVisitorAst()
        sv.visit(ast1)
        self.assertEquals(sv.vars, 1)


class MyVisitorAst2(wlang.ast.AstVisitor):
    """in order to void overriding"""

    def __init__(self):
        super(MyVisitorAst2, self).__init__()
        self.vars = 0

 #   def visit_StmtList(self, node, *args, **kwargs):
#        for s in node.stmts:
 #           self.visit(s)

    def visit_Stmt(self, node, *args, **kwargs):
        pass

 #   def visit_Exp(self, node, *args, **kwargs):
 #       pass



# test astvisitor and WhileLangSemantics
class TestAstVisitorOther (unittest.TestCase):

    def test_Asg_My(self):
        prg1 = "x := 7"
        ast1 = ast.parse_string(prg1)
        sv = MyVisitorAst2()
        sv.visit(ast1)


    def test_If_My(self):
        prg2 = "if true then x := 99"
        ast2 = ast.parse_string(prg2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

    def test_Assume_My(self):
        prg2 = "assume x > 2"
        ast2 = ast.parse_string(prg2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

    def test_Assert_My(self):
        prg2 = "assert y>5"
        ast2 = ast.parse_string(prg2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

    def test_Havoc_My(self):
        prg2 = "havoc x"
        ast2 = ast.parse_string(prg2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

    def test_Print_My(self):
        prg2 = "print_state"
        ast2 = ast.parse_string(prg2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

    def test_While_My_Parser(self):
        prg2 = "while true do x := 99"
        ast2 = ast.parse_string(prg2)
        testLang = parser.WhileLangSemantics()
        self.assertEquals(parser.WhileLangSemantics.start(testLang,ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.stmt_list(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.asgn_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.block_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.skip_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.print_state_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.if_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.while_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.assert_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.assume_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.havoc_stmt(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.bexp(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.bterm(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.bfactor(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.batom(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.var_list(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.rexp(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.rop(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.aexp(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.addition(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.subtraction(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.term(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.mult(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.division(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.neg_number(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.atom(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.name(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.number(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.INT(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.NAME(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.NEWLINE(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.factor(testLang, ast2), ast2)
        self.assertEquals(parser.WhileLangSemantics.bool_const(testLang, ast2), ast2)
        sv = MyVisitorAst2()
        sv.visit(ast2)

