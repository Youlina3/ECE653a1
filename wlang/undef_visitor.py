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
from __future__ import print_function

import wlang.ast
            
class UndefVisitor (wlang.ast.AstVisitor):
    """Computes all variables that are used before being defined"""
    def __init__ (self):
        super (UndefVisitor, self).__init__ ()
        #number of undefined nodes
        self._undefined_vars = set()


    def check (self, node):
        """Check for undefined variables starting from a given AST node"""
        # do the necessary setup/arguments and call self.visit (node, args)

        self.visit(node, defined = set())


    def get_undefs (self):
        """Return the set of all variables that are used before being defined
           in the program.  Available only after a call to check()
        """
        return self._undefined_vars
        
    def visit_StmtList (self, node, *args, **kwargs):
        for s in node.stmts:
            self.visit(s, *args, **kwargs)

    def visit_IntVar (self, node, *args, **kwargs):
        if node.name not in kwargs["defined"]:
            self._undefined_vars.add(node)


            
    def visit_Const (self, node, *args, **kwargs):
        pass
    
    def visit_Stmt (self, node, *args, **kwargs):
        pass
    
    def visit_AsgnStmt (self, node, *args, **kwargs):
        self.visit(node.rhs,*args,**kwargs)
        kwargs['defined'].add(node.lhs.name)

    def visit_Exp (self, node, *args, **kwargs):
        for a in node.args:
            self.visit(a, *args, **kwargs)
    
    def visit_HavocStmt (self, node, *args, **kwargs):
        for v in node.vars:
            kwargs["defined"].add(v.name)
    
    def visit_AssertStmt (self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
    
    def visit_AssumeStmt (self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
#all visit have args kwargs. args kwargs is a dictionary is key-value pair
    def visit_IfStmt (self, node, *args, **kwargs):
        ds = set(kwargs["defined"]); #copy by constrct
        self.visit(node.cond, defined=ds)
        self.visit(node.then_stmt, defined = ds)
        if node.has_else():
            ds2 = set(kwargs["defined"])
            self.visit(node.else_stmt, defined = ds2)
            intersec = ds & ds2
            kwargs['defined'] = kwargs['defined'] | intersec

    def visit_WhileStmt (self, node, *args, **kwargs):
        ds = set(kwargs["defined"])
        self.visit(node.cond, defined = ds)
        self.visit(node.body, defined = ds)



