from typing import Any


import streamlit as st
import pandas as pd
import Functions.persistence as persistence

st.title("Verbose Output")


# Load persisted state (best-effort)
_persisted = persistence.load_state()

# Prefer the in-memory session solution, fall back to persisted file
solved = st.session_state.get("S")
if solved is None and _persisted:
    solved = _persisted.get("S")

# Display verbose output (prefer persisted or session `S["Verbose"]`)
if not solved:
    st.info("No computation yet. Please select projects in the Selection page.")
else:
    if solved == "Unbounded Error":
        st.error("Project is infeasible - no optimal solution exists")
    else:
        st.write("### Verbose Output")



        # If the persisted/session `S` is a dict, try to show its 'Verbose' field
        if isinstance(solved, dict) and "Verbose" in solved:
            # pollutant names
            pollutants = ["CO2", "NO", "SO2", "PM2.5", "CH4", "VOC", "CO", "NH3", "BC", "N2O"]

            # Determine size dynamically from tableau shape
            total_cols = len(solved["Verbose"][1][1][0])-1          # width of tableau
            num_projects = (total_cols - 11) // 2 # remove pollutants (10) + Z (1)
            # generate c1..cN and s1..sN
            c_cols = [f"c{i+1}" for i in range(num_projects)]
            s_cols = [f"s{i+1}" for i in range(num_projects)]

            # final column labels
            final_columns = pollutants + c_cols + s_cols
            print(len(final_columns))

        for iteration, tableau, basic_solution in solved["Verbose"]:
            if (iteration == 0 ):
                with st.container(border=True):
                    st.markdown("### Initial Tableau")
                    st.dataframe(pd.DataFrame(tableau, columns = final_columns + ["Z"] + ["Constants"]))

                    st.markdown("### Basic Solution")
                    st.dataframe(pd.DataFrame(basic_solution[0][:-1], index = final_columns))
                    st.write(f"Z: {basic_solution[1]}")
                    continue
        
            with st.container(border=True):
                st.subheader(f"Iteration {iteration}")

                st.markdown("### Tableau")
                st.dataframe(pd.DataFrame(tableau, columns = final_columns +  ["Z"] + ["Constants"]))

                st.markdown("### Basic Solution")
                st.dataframe(pd.DataFrame(basic_solution[0][:-1], index = final_columns))
                st.write(f"Z: {basic_solution[1]}")
