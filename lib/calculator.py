import pandas as pd
import sympy as sp
import numpy as np

from ._functions import _tokenize, _validate_parenthesis, _evaluate_tokens

pd.set_option('display.float_format', lambda x: f'{x:.10f}')

class Calculator:

    def __init__(self):
        self._history = {}

    def calculate(self, expression: str) -> float:

        if expression in self._history:
            return self._history[expression]
        
        result = self._evaluate(expression)
        sympy_result = self._evaluate_sympy(expression)

        self._history[expression] = {}

        self._history[expression]["result"] = result
        self._history[expression]["sympy_result"] = sympy_result
        
        return result, sympy_result

    def display_history(self):
        if len(self._history) == 0:
            print("History is empty.")
            return
        
        df = pd.DataFrame(self._history).T
        print(df)

    def _evaluate(self, expression: str):
        try:
            _tokens = _tokenize(expression)
            _validate_parenthesis(_tokens)
            _result = _evaluate_tokens(_tokens)

            return _result
        
        except ValueError:
            return np.nan

    def _evaluate_sympy(self, expression: str):
        try:
            expression = expression.lstrip('0') or '0'
            expression = expression.replace('^', '**')
            result = sp.sympify(expression).evalf(16)

            try:
                result = float(result)

                if result.is_integer():
                    return int(result)
                else:
                    return result
            
            except ValueError:
                return np.nan
        
        except (sp.SympifyError, TypeError):
            return np.nan