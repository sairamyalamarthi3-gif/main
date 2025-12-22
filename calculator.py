import streamlit as st
st.title("Simple Calculator")

num1 = st.number_input("Enter number1",value=0.0)
num2 = st.number_input("Enter number2",value=0.0)

operation = st.selectbox("Choose an Operation",["Add","Subtract","Multiply","Divide"])

if operation == "Add":
    result = num1 + num2
elif operation == "Subtract":
    result = num1 -num2
elif operation == "Multiply":
    result = num1 * num2
else:
    result = "Cannot divide by Zero" if num2 == 0 else num1/num2

st.write(" ###Result:")
st.success(result)