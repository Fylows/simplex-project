import streamlit as st

st.title("Verbose Output")


if "selected_projects" not in st.session_state:
    selected_projects = []
else:
    selected_projects = st.session_state["selected_projects"].copy()

# Check if solution exists
if "S" not in st.session_state:
    st.info("No computation yet. Please select projects in the Selection page.")
    
else:
    solved = st.session_state["S"]

    if solved == "Unbounded Error":
        st.error("Project is infeasible - no optimal solution exists")
    else:
        st.write("### Verbose Output")
        st.write(solved["Verbose"])
