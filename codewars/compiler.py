import re

class Compiler(object):

    def __init__(self):
        self.parenth = False
        self.instructions = []
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        t = [int(tok) if tok.isdigit() else tok for tok in token_iter]
        return t[t.index('[')+1:t.index(']')], t[t.index(']')+1:]

    def pass1(self, program):
        vars, equation = self.tokenize(program)
        tmp_equation = ''.join([str(e) for e in equation])
        if equation[0] == '(' and equation[-1] == ')' and equation.count('(') == 1:
            equation = equation[1:-1]
        if tmp_equation in vars:
            return { 'op': 'arg', 'n': vars.index(tmp_equation) }
        elif tmp_equation.isdigit():
            return { 'op': 'imm', 'n': int(tmp_equation) }

        priority = {'*': 1, '/': 1, '+': 2, '-': 2}
        ops = {}
        for idx, op in enumerate(equation):
            if str(op) in '()':
                self.parenth = not self.parenth
            if str(op) in '+-*/' and not self.parenth:
                ops[idx] = op
        ops = dict(sorted(ops.items(), key=lambda x: (priority[x[1]], x[0]), reverse=True))
        op_idx, op_sym = list(ops.items())[0]

        l_equation, r_equation = equation[:op_idx], equation[op_idx+1:]
        eqn_to_prob = lambda equation: f'[ {" ".join(vars)} ] {"".join([str(e) for e in equation])}'
        return { 'op': op_sym, 'a': self.pass1(eqn_to_prob(l_equation)), 'b': self.pass1(eqn_to_prob(r_equation)) }
        
    def sub_pass2(self, ast):
        if ast['op'] in '+-*/':
            if ast['a']['op'] == 'imm' and ast['b']['op'] == 'imm':
                return { 'op': 'imm', 'n': eval(f'{ast["a"]["n"]}{ast["op"]}{ast["b"]["n"]}') }
            else:
                ast['a'] = self.pass2(ast['a'])
                ast['b'] = self.pass2(ast['b'])
        return ast

    def pass2(self, ast):
        reduced = self.sub_pass2(ast)
        while reduced != self.sub_pass2(reduced):
            reduced = self.sub_pass2(reduced)
        return reduced

    def pass3(self, ast):
        m_assembly = {'imm': 'IM', 'arg': 'AR', '+': 'AD', '-': 'SU', '*': 'MU', '/': 'DI'}
        if ast['op'] in '+-*/':
            a = ast['a']['op']
            b = ast['b']['op']
            if all([v in ['imm', 'arg'] for v in [a, b]]):
                self.instructions.append(f'{m_assembly[b]} {int(ast["b"]["n"])}')
                self.instructions.append('SW')
                self.instructions.append(f'{m_assembly[a]} {int(ast["a"]["n"])}')
                self.instructions.append(m_assembly[ast['op']])
            else:
                self.pass3(ast['a'])
                self.instructions.append('PU')
                self.pass3(ast['b'])
                self.instructions.append('SW')
                self.instructions.append('PO')
                self.instructions.append(m_assembly[ast['op']])
        else:
            self.instructions.append(f'{m_assembly[ast["op"]]} {int(ast["n"])}')
        return self.instructions

    def simulate(self, asm, argv):
        r0, r1 = None, None
        stack = []
        for ins in asm:
            if ins[:2] == 'IM' or ins[:2] == 'AR':
                ins, n = ins[:2], int(ins[2:])
            if ins == 'IM':   r0 = n
            elif ins == 'AR': r0 = argv[n]
            elif ins == 'SW': r0, r1 = r1, r0
            elif ins == 'PU': stack.append(r0)
            elif ins == 'PO': r0 = stack.pop()
            elif ins == 'AD': r0 += r1
            elif ins == 'SU': r0 -= r1
            elif ins == 'MU': r0 *= r1
            elif ins == 'DI': r0 /= r1
        return r0


if __name__ == '__main__':
    program1 = '[ a b ] a*a + b*b'
    program2 = '[ x y ] ( x + y ) / 2'
    program3 = '[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'
    program4 = '[ x ] x + 2*5'
    program5 = '[ x y z ] x - y - z + 10 / 5 / 2 - 7 / 1 / 7'
    c = Compiler()
    program = program5
    print(c.pass1(program))
    print(c.pass2(c.pass1(program)))
    print(c.pass3(c.pass2(c.pass1(program))))
    print(c.simulate(c.pass3(c.pass2(c.pass1(program))), [5, 4, 1]))
