"""
Phase 4: Streamlit Frontend.

This UI visualizes the execution of the LangGraph StateMachine.
"""

import time
import json
import streamlit as st

# Setup observability early
from nexus.observability.logger import setup_logging
setup_logging(log_format="console")

from nexus.core.state import NexusState, AgentName, TaskStatus
from nexus.core.graph import app as workflow_graph


# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Nexus | Multi-Agent Researcher",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium UI feel (Bright Theme Only)
st.markdown("""
<style>
    .reportview-container {
        background: #f8f9fa;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
    }
    .json-viewer {
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 12px;
        height: 600px;
        overflow-y: scroll;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "nexus_state" not in st.session_state:
    st.session_state.nexus_state = None
if "workflow_status" not in st.session_state:
    st.session_state.workflow_status = "idle"


# ==========================================
# 3. SIDEBAR (The Control Room)
# ==========================================
with st.sidebar:
    st.title("🧠 Nexus Control")
    st.markdown("Phase 4: Production Multi-Agent Research Pipeline.")
    
    st.divider()
    
    st.markdown("### 🤖 Agents in Graph")
    st.markdown("- 🧠 **Planner** (Task decomposition)")
    st.markdown("- 🔎 **Researcher** (Evidence gathering)")
    st.markdown("- ⚖️ **Fact Checker** (Validation loop)")
    st.markdown("- 📊 **Analyst** (Synthesis)")
    st.markdown("- ✍️ **Writer** (Drafting)")
    st.markdown("- 📋 **Reviewer** (Quality control)")
    
    st.divider()
    st.caption("Nexus Framework v0.4.0 | Phase 4")


# ==========================================
# 4. MAIN INTERFACE
# ==========================================

st.title("NeuralNet Multi-Agent Researcher")
st.markdown("""
Watch the **Shared State** mutate in real-time as LangGraph routes control between **Real LLM Agents**. 
*(Note: Execution may take a few minutes as LLMs reason through the state).*
""")

with st.container(border=True):
    query = st.text_area(
        "Research Directive", 
        value="Explain the core differences between LangGraph and Autogen for Multi-Agent Systems.",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        start_btn = st.button("🚀 Initialize Pipeline")
    with col2:
        if st.button("🧹 Reset State"):
            st.session_state.nexus_state = None
            st.session_state.workflow_status = "idle"
            st.rerun()

# ==========================================
# 5. EXECUTION & VISUALIZATION
# ==========================================

if start_btn and query:
    st.session_state.nexus_state = NexusState(user_query=query)
    st.session_state.workflow_status = "running"
    
if st.session_state.workflow_status == "running":
    
    viz_col, state_col = st.columns([1, 1])
    
    with viz_col:
        st.subheader("Graph Execution")
        status_box = st.empty()
        
        st.markdown("### Execution Status")
        stepper_box = st.empty()
        
        st.markdown("### Execution Timeline")
        timeline_container = st.container()
        
    with state_col:
        st.subheader("Shared State (Live)")
        state_metrics_box = st.empty()
        state_view = st.empty()
        
    # Prepare the initial state
    current_state = st.session_state.nexus_state
    
    status_box.info("🟢 Starting LangGraph Execution...")
    
    try:
        # workflow_graph.stream yields a dict of updates from the graph.
        for output in workflow_graph.stream(current_state.model_dump()):
            for node_name, state_dict in output.items():
                # Enforce Pydantic validation because state_dict is a dict, not a NexusState object.
                valid_state = NexusState.model_validate(state_dict)
                
                with viz_col:
                    # Update timeline
                    timestamp = valid_state.errors[-1].timestamp.strftime('%H:%M:%S') if valid_state.errors and node_name == valid_state.errors[-1].agent_name.value else "completed"
                    timeline_container.success(f"✅ [{node_name}] Executed successfully.")
                    
                    # Update Stepper
                    all_agents = ["Planner", "Researcher", "FactChecker", "Analyst", "Writer", "Reviewer"]
                    current_idx = all_agents.index(valid_state.current_agent.value) if valid_state.current_agent.value in all_agents else len(all_agents)
                    stepper_md = ""
                    for i, ag in enumerate(all_agents):
                        if i < current_idx:
                            stepper_md += f"{ag} ✅ | "
                        elif i == current_idx:
                            stepper_md += f"**{ag} ⏳** | "
                        else:
                            stepper_md += f"{ag} ⏸️ | "
                    stepper_box.markdown(stepper_md.strip(" | "))
                    
                with state_col:
                    state_metrics_box.markdown(f"**Current Agent:** {valid_state.current_agent.value} | **Retries:** {valid_state.retry_count} | **Errors:** {len(valid_state.errors)}")
                    state_json = valid_state.model_dump_json(indent=2)
                    state_view.markdown(f'<div class="json-viewer"><pre>{state_json}</pre></div>', unsafe_allow_html=True)
                
                # Persist the latest valid state
                current_state = valid_state
                st.session_state.nexus_state = current_state
                
    except Exception as e:
        import traceback
        st.session_state.workflow_status = "error"
        with viz_col:
            st.error("❌ Graph Execution Failed")
            st.markdown("### Structured Error Report")
            st.warning(f"**Reason:** {str(e)}\n\n**Origin:** `workflow_graph.stream`")
            with st.expander("Stack Trace"):
                st.code(traceback.format_exc(), language="python")
        
    if st.session_state.workflow_status != "error":
        st.session_state.workflow_status = "completed"
        with viz_col:
            status_box.success("✅ Workflow Complete")


if st.session_state.workflow_status == "completed":
    st.divider()
    st.success("🎉 LangGraph Workflow Completed Successfully!")
    
    state = st.session_state.nexus_state
    
    tab_report, tab_evidence, tab_tasks = st.tabs(["📄 Final Report", "🗂️ Evidence", "📋 Task Execution"])
    
    with tab_report:
        if state.draft.content:
            st.markdown(state.draft.content)
        else:
            st.warning("Draft was not completed.")
            
    with tab_evidence:
        for ev in state.evidence:
            val_status = "✅ Validated" if ev.validated else "❌ Rejected"
            st.info(f"**{val_status}**: {ev.content}\n\n*Source: {ev.source}*\n\n*Reason: {ev.validation_reason}*")
            
    with tab_tasks:
        for task in state.plan.tasks:
            status_emoji = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
            st.write(f"{status_emoji} **{task.description}**")
            if task.result:
                st.caption(f"Result: {task.result}")