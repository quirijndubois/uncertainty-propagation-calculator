import streamlit as st
from sympy import *
import numpy as np

import math

def extract_digits_and_power(number:float):
    scientific_notation = f"{number:e}"

    exponent_index = scientific_notation.index("e")

    return scientific_notation[:exponent_index],scientific_notation[exponent_index+1:]

st.title("Uncertainty Propagation Calculator")

expression_input = st.text_input("Enter the expression (e.g., x * y):")
expression_input = expression_input.replace("^","**")
if expression_input != "":

    expression = parse_expr(expression_input)

    main_symbols = list(expression.free_symbols)
    delta_symbols = [symbols("{\Delta}"+str(latex(symbol))) for symbol in main_symbols]

    st.latex(f"f({set(main_symbols)}) = "+latex(expression))

    delta_expression = sqrt(sum([(diff(expression,main_symbols[i])*delta_symbol)**2 for i,delta_symbol in enumerate(delta_symbols)]))

    st.latex(f"\Delta f ({set(main_symbols)}) = "+latex(delta_expression))

    values = []
    uncertainties = []
    for i,symbol in enumerate(main_symbols):
        col1,col2,col3 = st.columns(3)
        col1.latex(symbol)
        try:
            values.append([symbol,eval(col2.text_input("Value:",key=str(i)))])
        except:
            values.append([symbol,0])
        try:
            uncertainties.append([delta_symbols[i],eval(col3.text_input("Uncertainty:",key=str(i+100)))])
        except:
            uncertainties.append([delta_symbols[i],0])

    values = np.array(values).T
    uncertainties = np.array(uncertainties).T

    f = lambdify(list(values[0]),expression)

    all_symbols= list(values[0])+list(uncertainties[0])
    delta_f = lambdify(all_symbols,delta_expression)

    out1 = f(*values[1])
    out2 = delta_f(*values[1],*uncertainties[1])

    st.latex( f"{out1} \pm {out2}")

    out1_data = extract_digits_and_power(out1)
    out2_data = extract_digits_and_power(out2)

    out1 = str(out1_data[0]) + f"\cdot 10^{int(out1_data[1])}"
    out2 = str(out2_data[0]) + f"\cdot 10^{int(out2_data[1])}"

    st.latex( f"{out1} \pm {out2}")

