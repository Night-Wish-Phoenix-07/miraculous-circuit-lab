import numpy as np

class Circuit:
    def __init__(self):
        self.components = []          # (kind, name, node_a, node_b, value)
        self.nodes = {"0": 0}         # "0" is always ground

    def _node(self, name):
        name = str(name)
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def resistor(self, name, a, b, ohms):
        self.components.append(("R", name, self._node(a), self._node(b), ohms))

    def voltage_source(self, name, plus, minus, volts):
        self.components.append(("V", name, self._node(plus), self._node(minus), volts))

    def current_source(self, name, a, b, amps):
        self.components.append(("I", name, self._node(a), self._node(b), amps))

    def solve_dc(self):
        n = len(self.nodes) - 1
        vsources = [c for c in self.components if c[0] == "V"]
        m = len(vsources)

        A = np.zeros((n + m, n + m))
        z = np.zeros(n + m)

        for kind, name, a, b, val in self.components:
            if kind == "R":
                g = 1.0 / val
                if a: A[a-1, a-1] += g
                if b: A[b-1, b-1] += g
                if a and b:
                    A[a-1, b-1] -= g
                    A[b-1, a-1] -= g
            elif kind == "I":
                if a: z[a-1] -= val
                if b: z[b-1] += val

        for k, (kind, name, a, b, val) in enumerate(vsources):
            row = n + k
            if a:
                A[a-1, row] += 1
                A[row, a-1] += 1
            if b:
                A[b-1, row] -= 1
                A[row, b-1] -= 1
            z[row] = val

        x = np.linalg.solve(A, z)

        result = {"0": 0.0}
        for name, idx in self.nodes.items():
            if idx:
                result[name] = x[idx-1]
        for k, c in enumerate(vsources):
            result["I_" + c[1]] = x[n + k]
        return result
