import math


def _generate_constraints(nparams, _min = -500, _max = 500):
    out = {}
    for i in range(nparams):
        out[i] = {"MIN":_min,"MAX":_max}
    return out

class _Rc_options:
    def __init__(self, PFR_MC):
        self.PFR_MC = PFR_MC
        self._rc_options_unfactorized_poly = {
            '0x0': {
                'form': self.PFR_MC + '*(@0)',
                'constraints': _generate_constraints(1)
            },
            '1x0': {
                'form': self.PFR_MC + '*(@0+@1*x)',
                'constraints': _generate_constraints(2)
            },
            '0x1': {
                'form': self.PFR_MC + '*(@0+@1*y)',
                'constraints': _generate_constraints(2)
            },
            '1x1': {
                'form': self.PFR_MC + '*(@0+@1*x+@2*y+@3*x*y)',
                'constraints': _generate_constraints(4)
            },
            '2x0': {
                'form': self.PFR_MC + '*(@0+@1*x+@2*x*x)',
                'constraints': _generate_constraints(3)
            },
            '0x2': {
                'form': self.PFR_MC + '*(@0+@1*y+@2*y*y)',
                'constraints': _generate_constraints(3)
            },
            '2x1': {
                'form': self.PFR_MC + '*(@0+@1*x+@2*y+@3*x*y+@4*x**2+@5*y*x**2)',
                'constraints': _generate_constraints(6)
            },
            '1x2': {
                'form': self.PFR_MC + '*(@0+@1*x+@2*y+@3*x*y+@4*y**2+@5*x*y**2)',
                'constraints': _generate_constraints(6)
            },
            '2x2': {
                'form': self.PFR_MC + '* (@0+@1*x+@2*x**2)*(@3+@4*y+@5*y**2)',
                'constraints': _generate_constraints(6)
            }
        }


        self._rc_options_factorized_poly = {
            '0x0': {
                'form': self.PFR_MC + '*(@0)',
                'constraints': _generate_constraints(1)
            },
            '1x0': {
                'form': self.PFR_MC + '*@0 * (1+@1*x)',
                'constraints': _generate_constraints(2)
            },
            '0x1': {
                'form': self.PFR_MC + '*@0*(1+@1*y)',
                'constraints': _generate_constraints(2)
            },
            '2x0': {
                'form': self.PFR_MC + '*@0*(1+@1*x+@2*x*x)',
                'constraints': _generate_constraints(3)
            },
            '0x2': {
                'form': self.PFR_MC + '*@0*(1+@1*y+@2*y*y)',
                'constraints': _generate_constraints(3)
            },
            '0x3': {
                'form': self.PFR_MC + '*@0*(1+@1*y+@2*y*y+@3*y*y*y)',
                'constraints': _generate_constraints(4)
            },
            '1x1': {
                'form': self.PFR_MC + '* @0 *(1+@1*x)*(1+@2*y)',
                'constraints': _generate_constraints(3)
            },
            '2x1': {
                'form': self.PFR_MC + '* @0 * (1+@1*x+@3*x*x)*(1+@2*y)',
                'constraints': _generate_constraints(4)
            },
            '1x2': {
                'form': self.PFR_MC + '* @0 * (1+@1*x)*(1+@2*y + @3*y*y)',
                'constraints': _generate_constraints(4)
            },
            '2x2': {
                'form': self.PFR_MC + '* @0 * (1+@1*x+@3*x*x) * (1+@2*y + @4*y*y)',
                'constraints': _generate_constraints(5)
            },
            '1x3': {
                'form': self.PFR_MC + '* @0 * (1+@1*x) * (1+@2*y + @3*y*y + @4*y*y*y)',
                'constraints': _generate_constraints(5)
            },
            '3x1': {
                'form': self.PFR_MC + '* @0 * (1+@1*x+@3*x*x + @4*x*x*x) * (1+@2*y)',
                'constraints': _generate_constraints(5)
            },
            '3x2': {
                'form': self.PFR_MC + '* @0 * (1+@1*x+@3*x*x + @4*x*x*x) * (1+@2*y + @5 * y*y)',
                'constraints': _generate_constraints(6)
            },
            '2x3': {
                'form': self.PFR_MC + '* @0 * (1+@1*x + @5 *x * x) * (1+@2*y + @3*y*y + @4*y*y*y)',
                'constraints': _generate_constraints(6)
            },
        }
    

    def expr_legendre(self, n, var):
        term_const = f"{1/(2**n):.4f}*"
        term_sum = ""
        for k in range(n+1):
            term_Cnk = f"{(math.comb(n, k))**2}*"
            term_1 = ""
            for i in range(n-k):
                term_1 += f"(2*{var}-2)*"
            term_2 = ""
            for i in range(k):
                term_2 += f"(2*{var})*"
            term_k = term_Cnk + term_1 + term_2
            term_k = "(" + term_k[:-1] + ")+"
            term_sum = term_sum + term_k
        term_sum = "(" + term_sum[:-1] + ")"
        term = term_const + term_sum
        return term


    def rc_legendre_factorized_exp(self, PFR_MC, d_x, d_y):
        term_0 = f"@0+"
        n_par = 1
        x_term = ""
        for i in range(1, d_x + 1):
            expr = self.expr_legendre(i, "x")
            if i == 0:
                x_term += f"{expr}+"
            else:
                x_term += f"@{n_par}*{expr}+"
                n_par += 1
        if x_term == "":
            x_term = "0"
        else:
            x_term = "(" + x_term[:-1] + ")"

        y_term = ""
        for i in range(1, d_y + 1):
            expr = self.expr_legendre( i, "y")
            if i == 0:
                y_term += f"{expr}+"
            else:
                y_term += f"@{n_par}*{expr}+"
                n_par += 1
        if y_term == "":
            y_term = "0"
        else:
            y_term = "(" + y_term[:-1] + ")"
        
        form = f"{PFR_MC}*exp(" + term_0 + x_term + "+" + y_term + ")"
        
        
        constraints = _generate_constraints(n_par, -10.0, 10.0)

        for constraint in constraints.values():
            constraint["NOM"] = 0.0
            constraint["ERROR"] = 0.1

        entry = {"form": form, "constraints": constraints}

        return entry


    @property
    def _rc_options_factorized_legendre_factorized_exp(self):
        options = {}
        for d_x in range(6):
            for d_y in range(6):
                options[f"{d_x}x{d_y}"] = self.rc_legendre_factorized_exp(self.PFR_MC, d_x, d_y)
        return options


    def expr_bernstein(self, n, v, var):
        term_Cnk =  f"{math.comb(n, v)}*"
        term_1 = ""
        for i in range(v):
            term_1 += f"{var}*" 
        term_2 = ""
        for i in range(n-v):
            term_2 += f"(1-{var})*"
        term = term_Cnk + term_1 + term_2
        if term.endswith("*"): 
            term = "(" + term[:-1] + ")"
        else:
            term = "(" + term[:] + ")"
        return term

    def rc_bernstein_factorized(self, PFR_MC, d_x, d_y):
        form = f"{PFR_MC}*@0*"
        n_par = 1
        x_term = ""
        for i in range(d_x + 1):
            expr = self.expr_bernstein(d_x, i, "x")
            if i == 0:
                x_term += f"{expr}+"
            else:
                x_term += f"@{n_par}*{expr}+"
                n_par += 1
        x_term = "(" + x_term[:-1] + ")"
            
        y_term = ""
        for i in range(d_y + 1):
            expr = self.expr_bernstein(d_y, i, "y")
            if i == 0:
                y_term += f"{expr}+"
            else:
                y_term += f"@{n_par}*{expr}+"
                n_par += 1
        y_term = "(" + y_term[:-1] + ")"
        

        constraints = _generate_constraints(n_par, 0.0, 10.0)

        for constraint in constraints.values():
            constraint["NOM"] = 1.0
            constraint["ERROR"] = 0.1

        constraints[0]["MIN"] = 1e-6
        entry = {"form": form + x_term + "*" + y_term, "constraints": constraints}

        return entry

    def rc_bernstein_factorized_log_par(self, PFR_MC, d_x, d_y):
        form = f"{PFR_MC}*exp(@0)*"
        n_par = 1
        x_term = ""
        for i in range(d_x + 1):
            expr = self.expr_bernstein(d_x, i, "x")
            if i == 0:
                x_term += f"{expr}+"
            else:
                x_term += f"exp(@{n_par})*{expr}+"
                n_par += 1
        x_term = "(" + x_term[:-1] + ")"
            
        y_term = ""
        for i in range(d_y + 1):
            expr = self.expr_bernstein(d_y, i, "y")
            if i == 0:
                y_term += f"{expr}+"
            else:
                y_term += f"exp(@{n_par})*{expr}+"
                n_par += 1
        y_term = "(" + y_term[:-1] + ")"
        
        entry = {"form": form + x_term + "*" + y_term, "constraints": _generate_constraints(n_par, -10, 10)}
        return entry

    @property
    def _rc_options_factorized_bernstein(self):
        options = {}
        for d_x in range(6):
            for d_y in range(6):
                options[f"{d_x}x{d_y}"] = self.rc_bernstein_factorized(self.PFR_MC, d_x, d_y)
        return options

    @property
    def _rc_options_factorized_bernstein_log_par(self):
        options = {}
        for d_x in range(6):
            for d_y in range(6):
                options[f"{d_x}x{d_y}"] = self.rc_bernstein_factorized_log_par(self.PFR_MC, d_x, d_y)
        return options



if __name__ == "__main__":
    rcs = _Rc_options("1")
    print(rcs._rc_options_factorized_bernstein) 
    print(rcs._rc_options_factorized_bernstein_log_par) 
            
        



