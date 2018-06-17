import unittest
import wlang.ast as ast
import wlang.stats_visitor as stats_visitor

class TestStatsVisitor (unittest.TestCase):
    def test_asg (self):
        prg1 = "x := 10; print_state"
        ast1 = ast.parse_string (prg1)
        print ast1
        sv = stats_visitor.StatsVisitor ()
        sv.visit (ast1)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)
        # UNCOMMENT to run the test


#if statement
    def test_if (self):
        prg2 = "if true then a :=1 else b := 0"
        ast2 = ast.parse_string (prg2)
        print ast2
        sv = stats_visitor.StatsVisitor ()
        sv.visit (ast2)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 2)

# if statement
    def test_if2(self):
        prg2 = "if true then a :=1"
        ast2 = ast.parse_string(prg2)
        print ast2
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast2)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)

    # while statement
    def test_while(self):
        prg3 = "while 1 <= 2 inv true do { x := 0} "
        ast3 = ast.parse_string(prg3)
        print ast3
        sv = stats_visitor.StatsVisitor()
        #nums = sv.get_num_stats()
        #numv = sv.get_num_vars()
        sv.visit(ast3)
        self.assertEquals(sv.get_num_stmts(), 2)
        self.assertEquals(sv.get_num_vars(), 1)



#assert
    def test_assert (self):
        prg5 = "assert x < 4"
        ast5 = ast.parse_string(prg5)
        print ast5
        sv = stats_visitor.StatsVisitor()
#        self.assertEquals(sv.get_num_stmts(), 2)
#        self.assertEquals(sv.get_num_vars(), 2)
        sv.visit(ast5)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)

#assume
    def test_assume (self):
        prg6 = "assume x < 4"
        ast6 = ast.parse_string(prg6)
        print ast6
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast6)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)


#havoc
    def test_havoc (self):
        prg7 = "havoc y"
        ast7 = ast.parse_string(prg7)
        print ast7
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast7)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 1)

#stmt
    def test_stmt (self):
        prg8 = "skip"
        ast8 = ast.parse_string(prg8)
        print ast8
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast8)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 0)

#exp
    def test_exp (self):
        prg9 = "y := (3+ x) * y"
        ast9 = ast.parse_string(prg9)
        print ast9
        pv = ast.PrintVisitor()
        pv.visit(ast9)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast9)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 2)


#intvar
    def test_intVar (self):
        prg12 = "havoc x, y, z"
        ast12 = ast.parse_string(prg12)
        print ast12
       # pv = ast.PrintVisitor()
       # pv.visit(ast12)
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast12)
        self.assertEquals(sv.get_num_stmts(), 1)
        self.assertEquals(sv.get_num_vars(), 3)

#intvar
    def test_ele (self):
        prg13 = "x :=1; y := -2; z := 3"
        ast13 = ast.parse_string(prg13)
        print ast13
        sv = stats_visitor.StatsVisitor()
        sv.visit(ast13)
        self.assertEquals(sv.get_num_stmts(), 3)
        self.assertEquals(sv.get_num_vars(), 3)

