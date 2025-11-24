import streamlit as st
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
            st.write(solved["Verbose"])
        else:
            # fallback: show whatever was stored
            st.write(solved)
