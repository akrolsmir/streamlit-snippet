import streamlit as st
import numpy as np

fib = [0, 1]
iterations = st.slider("Iterations", 0, 20, 8)
for i in range(iterations - 2):
    fib.append(fib[-1] + fib[-2])

st.write(f"Here are the first {len(fib)} Fibonacci numbers!")
st.area_chart(fib)

ratios = np.array(fib[2:]) / np.array(fib[1:-1])
st.write("Their ratios approach the Golden Ratio:")
st.line_chart(ratios)