import streamlit as st
import Functions.persistence as persistence

st.title("Verbose Output")


# Load persisted state (best-effort)
_persisted = persistence.load_state()

# Prefer the in-memory session solution, fall back to persisted file
solved = st.session_state.get("S")
if solved is None and _persisted:
    solved = _persisted.get("S")

# Debug: show session state + persisted for traceability
with st.expander("Debug: session_state"):
    debug_state = {k: (v if not isinstance(v, (list, dict)) else v) for k, v in st.session_state.items()}
    debug_state["_persisted"] = _persisted
    st.json(debug_state)

# Controls to manage persisted state
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Clear persisted state"):
        persistence.clear_state()
        # also clear relevant session keys
        for k in ("selected_projects", "select_all", "S"):
            if k in st.session_state:
                del st.session_state[k]
        st.experimental_rerun()
with col2:
    if st.button("Save current state"):
        persistence.save_state({
            "selected_projects": st.session_state.get("selected_projects", []),
            "select_all": st.session_state.get("select_all", False),
            "S": st.session_state.get("S", None)
        })
        st.success("State saved")

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
