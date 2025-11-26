from DLangVisitor import DLangVisitor
from DLangParser import DLangParser

import MyMath
import MyPlot
import Matrix
import MyFile
import MyRegression
import MyMLP
import MyClusterNN


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class EvalVisitor(DLangVisitor):
    def __init__(self):
        self.env = {}
        self.funcs = {}

    # ---------- Utilidades ----------

    def _is_true(self, v):
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            return v != ""
        if v is None:
            return False
        return bool(v)

    # ---------- Programa ----------

    def visitProgram(self, ctx: DLangParser.ProgramContext):
        for st in ctx.statement():
            self.visit(st)
        return None

    # ---------- Sentencias básicas ----------

    def visitAssignStmt(self, ctx: DLangParser.AssignStmtContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.env[name] = value
        return value

    def visitPrintStmt(self, ctx: DLangParser.PrintStmtContext):
        value = self.visit(ctx.expr())
        print(value)
        return None

    def visitReturnStmt(self, ctx: DLangParser.ReturnStmtContext):
        value = self.visit(ctx.expr()) if ctx.expr() is not None else None
        raise ReturnException(value)

    # ---------- Control de flujo ----------

    def visitIfStmt(self, ctx: DLangParser.IfStmtContext):
        cond = self.visit(ctx.expr())
        if self._is_true(cond):
            self.visit(ctx.block(0))
        elif ctx.block(1) is not None:
            self.visit(ctx.block(1))
        return None

    def visitWhileStmt(self, ctx: DLangParser.WhileStmtContext):
        while self._is_true(self.visit(ctx.expr())):
            self.visit(ctx.block())
        return None

    def visitBlockStmt(self, ctx: DLangParser.BlockStmtContext):
        for st in ctx.statement():
            self.visit(st)
        return None

    # ---------- Funciones ----------

    def visitFuncDefStmt(self, ctx: DLangParser.FuncDefStmtContext):
        name = ctx.ID().getText()
        params = [p.getText() for p in ctx.paramList().ID()] if ctx.paramList() else []
        block = ctx.block()
        self.funcs[name] = (params, block)
        return None

    def visitFuncCallExpr(self, ctx: DLangParser.FuncCallExprContext):
        name = ctx.ID().getText()
        args = [self.visit(e) for e in ctx.argList().expr()] if ctx.argList() else []

        # 1) Módulos internos
        for module in (MyMath, Matrix, MyPlot, MyFile, MyRegression, MyMLP, MyClusterNN):
            if hasattr(module, name):
                func = getattr(module, name)
                return func(*args)

        # 2) Funciones del DSL
        if name in self.funcs:
            params, block = self.funcs[name]
            old_env = self.env.copy()
            try:
                for p, a in zip(params, args):
                    self.env[p] = a
                try:
                    self.visit(block)
                except ReturnException as r:
                    return r.value
                return None
            finally:
                self.env = old_env

        raise Exception(f"Funcion no definida: {name}")

    def visitFuncCallPrimary(self, ctx: DLangParser.FuncCallPrimaryContext):
        return self.visit(ctx.funcCall())

    # ---------- Literales y variables ----------

    def visitNumberLiteralExpr(self, ctx: DLangParser.NumberLiteralExprContext):
        text = ctx.NUMBER().getText()
        return float(text) if '.' in text else int(text)

    def visitStringLiteralExpr(self, ctx: DLangParser.StringLiteralExprContext):
        text = ctx.STRING().getText()
        return text[1:-1]

    def visitTrueLiteralExpr(self, ctx: DLangParser.TrueLiteralExprContext):
        return True

    def visitFalseLiteralExpr(self, ctx: DLangParser.FalseLiteralExprContext):
        return False

    def visitIdentifierExpr(self, ctx: DLangParser.IdentifierExprContext):
        name = ctx.ID().getText()
        if name not in self.env:
            raise Exception(f"Variable no definida: {name}")
        return self.env[name]

    def visitParenExpr(self, ctx: DLangParser.ParenExprContext):
        return self.visit(ctx.expr())

    # ---------- Listas / matrices ----------

    def visitListLiteralNode(self, ctx: DLangParser.ListLiteralNodeContext):
        return [self.visit(e) for e in ctx.expr()]

    def visitListLiteralExpr(self, ctx: DLangParser.ListLiteralExprContext):
        return self.visit(ctx.listLiteral())

    # ---------- Lógicos ----------

    def visitOrOp(self, ctx: DLangParser.OrOpContext):
        left = self.visit(ctx.expr())
        if self._is_true(left):
            return True
        right = self.visit(ctx.andExpr())
        return self._is_true(right)

    def visitAndOp(self, ctx: DLangParser.AndOpContext):
        left = self.visit(ctx.andExpr())
        if not self._is_true(left):
            return False
        right = self.visit(ctx.relExpr())
        return self._is_true(right)

    def visitRelOpExpr(self, ctx: DLangParser.RelOpExprContext):
        left = self.visit(ctx.addExpr(0))
        if ctx.relOp() is None:
            return left
        right = self.visit(ctx.addExpr(1))
        op = ctx.relOp().getText()
        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return left < right
        if op == '<=':
            return left <= right
        if op == '>':
            return left > right
        if op == '>=':
            return left >= right

    # ---------- Aritmética ----------

    def visitAddSubExpr(self, ctx: DLangParser.AddSubExprContext):
        left = self.visit(ctx.addExpr())
        right = self.visit(ctx.mulExpr())
        op = ctx.getChild(1).getText()

        if isinstance(left, list) and isinstance(right, list):
            return Matrix.mat_add(left, right) if op == '+' else Matrix.mat_sub(left, right)

        return left + right if op == '+' else left - right

    def visitMulDivExpr(self, ctx: DLangParser.MulDivExprContext):
        left = self.visit(ctx.mulExpr())
        right = self.visit(ctx.powExpr())
        op = ctx.getChild(1).getText()

        if isinstance(left, list) and isinstance(right, list) and op == '*':
            return Matrix.mat_mul(left, right)

        if op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            return left % right

    def visitPowerOp(self, ctx: DLangParser.PowerOpContext):
        result = self.visit(ctx.unaryExpr(0))
        for i in range(1, len(ctx.unaryExpr())):
            expo = self.visit(ctx.unaryExpr(i))
            result = MyMath.potencia(result, expo)
        return result

    # ---------- Unarios ----------

    def visitUnaryMinusExpr(self, ctx: DLangParser.UnaryMinusExprContext):
        return -self.visit(ctx.unaryExpr())

    def visitUnaryPlusExpr(self, ctx: DLangParser.UnaryPlusExprContext):
        return +self.visit(ctx.unaryExpr())

    def visitUnaryNotExpr(self, ctx: DLangParser.UnaryNotExprContext):
        return not self._is_true(self.visit(ctx.unaryExpr()))

    def visitPrimaryExpr(self, ctx: DLangParser.PrimaryExprContext):
        return self.visit(ctx.primary())
