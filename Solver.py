import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from Functions.projectsTable import ProjectsList
import Functions.tableauMaker as tableauMaker
import Functions.SimplexSolver as SimplexSolver
import Functions.persistence as persistence

# Load persisted state (best-effort). Attempt to apply persisted values before setting defaults.
_persisted = persistence.load_state()
if _persisted:
    # Only apply persisted values when the session doesn't already have a meaningful value.
    # Important: do NOT treat an empty list as "no meaningful value" here —
    # the user may intentionally clear the selection. Only apply persisted
    # `selected_projects` when the key is missing or explicitly None.
    if ("selected_projects" not in st.session_state) or st.session_state.get("selected_projects") is None:
        if "selected_projects" in _persisted:
            st.session_state["selected_projects"] = _persisted.get("selected_projects")
    if ("S" not in st.session_state) or st.session_state.get("S") is None:
        if "S" in _persisted:
            st.session_state["S"] = _persisted.get("S")

# Initialize session state keys early so values persist across pages/reruns
if "selected_projects" not in st.session_state:
    st.session_state["selected_projects"] = []
if "S" not in st.session_state:
    st.session_state["S"] = None

POLLUTANTS_MIN = [1000, 35, 25, 20, 60, 45, 80, 12, 6, 10]
EMPTY_POLLUTANTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
POLLUTANT_NAMES = ["CO2", "NO", "SO2", "PM2.5", "CH4", "VOC", "CO", "NH3", "BC", "N2O"]

# Set page configuration
st.set_page_config(
    page_title="Environmental Projects Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Main title
st.title("🌱 Environmental Projects Dashboard")
st.markdown("---")


# Create two columns for layout
col1, col2 = st.columns([1, 1])

# Left column - Project Checklist
with col1:
    st.header("📋 Project Selection")
    st.markdown("Select the projects you want to analyze:")
    
    # Initialize session state once
    if "selected_projects" not in st.session_state:
        st.session_state.selected_projects = []

    project_names = ProjectsList["ProjectNames"].tolist()

    # Select All button (explicit action) and persistence when selection changes.
    def _on_projects_change():
        # This callback runs after `selected_projects` has been updated in session_state.
        sel = st.session_state.get("selected_projects", [])
        
        try:
            persistence.save_state({
                "selected_projects": sel,
                "S": st.session_state.get("S", None)
            })
        except Exception:
            pass

    # Button to select all projects explicitly
    if st.button("Select All"):
        st.session_state["selected_projects"] = project_names.copy()
        try:
            persistence.save_state({
                "selected_projects": st.session_state.get("selected_projects", []),
                "S": st.session_state.get("S", None)
            })
        except Exception:
            pass

    # Selection box with an on_change callback so we persist whenever the user changes it
    selected_projects = st.multiselect(
        "Choose Projects:",
        options=project_names,
        default=st.session_state.get("selected_projects", []),
        key="selected_projects",
        on_change=_on_projects_change,
    )

    # persist selection immediately (best-effort)
    try:
        persistence.save_state({
            "selected_projects": st.session_state.get("selected_projects", []),
            "S": st.session_state.get("S", None)
        })
    except Exception:
        pass
    
    # Display selected projects info
    if selected_projects:
        st.subheader("📊 Selected Projects Information")
        
        # Filter dataframe for selected projects
        selected_df = ProjectsList[ProjectsList["ProjectNames"].isin(selected_projects)]
        
        # Display as a nice table
        st.dataframe(
            selected_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Show summary statistics
        st.subheader("📈 Summary Statistics")
        summary_cols = st.columns(2)

        # INSERT HERE SIMPLEX ALGORITHM
        selected_projects_names = selected_df['ProjectNames'].tolist()

        selected_projects_matrix = tableauMaker.populateProjects(selected_projects_names)
        systems = tableauMaker.systemsLinearConstructor(selected_projects_matrix, POLLUTANTS_MIN)
        systems = tableauMaker.makeTableau(systems, False)
        solved = SimplexSolver.simplex(systems, False)

        # persist solved result in session state so other pages/components can read it
        st.session_state["S"] = solved

        # persist solved result to disk (best-effort)
        try:
            persistence.save_state({
                "selected_projects": st.session_state.get("selected_projects", []),
                "S": st.session_state.get("S", None)
            })
        except Exception:
            pass

        if solved == "Unbounded Error":
            st.error("Project is infeasible - no optimal solution exists")
        else:
            with summary_cols[0]:
                st.metric("Total Cost", f"${solved['Z']:,.0f}")
            with summary_cols[1]:
                st.metric("Projects Selected", len(selected_projects))
            
            simplex_results = SimplexSolver.expensesSummary(selected_projects_names, solved["Basic Solution"])
            st.dataframe(
                simplex_results,
                use_container_width=True,
                hide_index=True
            )

# USE COL1's DATA
# Right column - Emissions Bar Graph
with col2:
    st.subheader("📈 Selected Projects Emissions Impact")
    
    # Calculate remaining emissions after project reductions
    pollutant_columns = POLLUTANT_NAMES
    initial_values = POLLUTANTS_MIN
    empty_arr = EMPTY_POLLUTANTS

    # Read solved result from session state to survive reruns/pages
    solved_state = st.session_state.get("S", None)

    if selected_projects and solved_state and solved_state != "Unbounded Error":
        project_reductions = solved_state["Basic Solution"][0][:10]
        remaining_emissions = [max(0, initial - reduction) for initial, reduction in zip(initial_values, project_reductions)]
    else:
        project_reductions = empty_arr
        remaining_emissions = initial_values
    
    project_emissions_data = {
        "Pollutant": pollutant_columns,
        "Remaining Emissions (tons)": remaining_emissions
    }
    
    # Create DataFrame for remaining emissions
    project_emissions_df = pd.DataFrame(project_emissions_data)
    
    # Create bar chart for remaining emissions
    fig2 = px.bar(
        project_emissions_df,
        x="Pollutant",
        y="Remaining Emissions (tons)",
        title=f"Remaining Emissions After {len(selected_projects)} Selected Project(s)",
        color="Remaining Emissions (tons)",
        color_continuous_scale="reds",
        text="Remaining Emissions (tons)"
    )
    
    # Customize the second chart
    fig2.update_traces(
        texttemplate='%{text:.2f}',
        textposition='outside'
    )
    
    fig2.update_layout(
        xaxis_title="Pollutant Type",
        yaxis_title="Reduction (tons)",
        showlegend=False,
        height=500,
        title_x=0.5
    )
    
    # Display the second chart
    st.plotly_chart(fig2, use_container_width=True)
    
    # Show comparison between initial and remaining emissions
    st.subheader("🔄 Comparison: Initial vs Remaining Emissions")
    
    # Create comparison DataFrame
    comparison_data = {
        "Pollutant": pollutant_columns,
        "Initial Emissions": initial_values,
        "Remaining Emissions": remaining_emissions
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Create comparison chart
    fig3 = px.bar(
        comparison_df,
        x="Pollutant",
        y=["Initial Emissions", "Remaining Emissions"],
        title="Initial Emissions vs Remaining Emissions After Project Implementation",
        barmode='group',
        color_discrete_sequence=['#ff6b6b', '#4ecdc4']
    )
    
    fig3.update_layout(
        xaxis_title="Pollutant Type",
        yaxis_title="Emissions (tons)",
        height=500,
        title_x=0.5
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Add summary of project impact
    if solved != "Unbounded Error":
        total_co2_reduction = selected_df['CO2'].sum()
        total_cost = selected_df['Cost'].sum()
        
        st.success(f"🎯 **Selected Projects Summary:** {total_co2_reduction:.1f} tons CO2 reduction for ${total_cost:,.0f} total cost")
        

# Bottom section - Additional Information
st.markdown("---")
st.header("ℹ️ About This Dashboard")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 Project Categories")
    st.markdown("""
    - **Renewable Energy**: Solar, Wind, Gas-to-renewables
    - **Transportation**: EV infrastructure, Bus replacements, Traffic optimization
    - **Industrial**: Scrubbers, Energy efficiency, Process changes
    - **Residential**: Insulation, Clean cookstoves, LPG conversion
    - **Environmental**: Reforestation, Wetlands, Methane capture
    """)

with col4:
    st.subheader("📊 Key Metrics")
    st.markdown("""
    - **Cost**: Implementation cost in thousands of dollars
    - **CO2**: Carbon dioxide reduction in tons
    - **Air Quality**: NO, SO2, PM2.5 reductions
    - **Greenhouse Gases**: CH4, N2O, BC reductions
    - **Other Pollutants**: VOC, CO, NH3 reductions
    """)

# Footer
st.markdown("---")
st.markdown("Built using Streamlit | Environmental Impact Analysis Tool")
