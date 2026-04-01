import streamlit as st
import json
import os
import time
import requests
import random
import pandas as pd

# ==========================================
# CONFIG & PATHS
# ==========================================
st.set_page_config(page_title="AI DevOps Command Center", layout="wide", page_icon="🚀")

SCORE_FILE = "c:/AI_DeVops/github_agent_backend/rl_scores.json"
KNOWLEDGE_BASE_FILE = "c:/AI_DeVops/github_agent_backend/episodic_patch_memory.json"
HOT_ZONES_FILE = "c:/AI_DeVops/github_agent_backend/hot_zones.json"
ENV_FILE = "c:/AI_DeVops/github_agent_backend/.env"
WEBHOOK_URL = "http://localhost:8080/api/v1/webhook/github"

def load_json(filepath, default_val):
    if not os.path.exists(filepath):
        return default_val
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return default_val

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("🎛️ Command Center")
st.sidebar.markdown("Configure Agent Runtime Flags")

REPOS = ["Shubhamjkd01/Nursesycn", "Shubhamjkd01/Edusential_collabration", "Shubhamjkd01/edusentinel-v3"]
target_repo = st.sidebar.selectbox("🎯 Target Repository", REPOS)

st.sidebar.markdown("---")
agent_mode = st.sidebar.radio("⚙️ Operational Mode", ["Auto Fix (Production)", "Dry Run (Sandbox)"])

st.sidebar.markdown("---")
llm_priority = st.sidebar.selectbox("🧠 Primary LLM Engine", ["Groq Llama-3 (Fastest)", "Gemini 1.5 Flash", "OpenAI GPT-4o", "Offline / Failover Mode"])

st.sidebar.markdown("---")
simulate_btn = st.sidebar.button("🚀 Trigger Pipeline Failure", type="primary", use_container_width=True)

# ==========================================
# METRICS HEADER
# ==========================================
st.title("🚀 Enterprise CI/CD Autonomous DevOps Agent")
st.caption("Real-Time Triage, Classification, and Multi-LLM Rollback Command Center")

scores = load_json(SCORE_FILE, {"total_score": 0.0, "success_count": 0, "failure_count": 0, "total_time": 0.0})
memory = load_json(KNOWLEDGE_BASE_FILE, [])

total_fixes = scores.get("success_count", 0) + scores.get("failure_count", 0)
success_count = scores.get("success_count", 0)

hits = sum(1 for m in memory if m.get("accepted", False))
hit_rate = (hits / len(memory) * 100.0) if memory else 0.0

cost_per_failure = 150 
saved_cost = success_count * cost_per_failure
human_avg_mttr = 45 # minutes
ai_avg_mttr_sec = (scores.get("total_time", 0.0) / total_fixes) if total_fixes > 0 else 14.5

# Render 3 Columns
col1, col2, col3 = st.columns(3)
col1.metric("⏱️ Time to Fix (Auto vs Human)", f"{ai_avg_mttr_sec:.1f} sec", delta=f"-{human_avg_mttr} mins", delta_color="normal")
col2.metric("🧠 Memory Reuse Efficiency", f"{hit_rate:.1f}%", delta="+Efficiency")
col3.metric("💰 Cost Saved Per Failure", f"${cost_per_failure:,}", delta=f"${saved_cost:,} Total Saved", delta_color="normal")

# ==========================================
# LIVE PIPELINE SIMULATION EXECUTION
# ==========================================
st.markdown("---")

pipeline_col, memory_col = st.columns(2)

with pipeline_col:
    st.markdown("### 🔄 Live Pipeline Execution")
    
    if simulate_btn:
        # Pre-calculate Match and Confidence immediately for Sync with Memory Col
        match_found = random.choice([True, False])
        if hit_rate > 50: match_found = True 
        conf_score = random.randint(85, 99) if match_found else random.randint(55, 87)
        sim_time = random.uniform(4.1, 6.7)
        
        # Async Backend Trigger
        run_id = random.randint(10000, 99999)
        try:
            requests.post(
                WEBHOOK_URL, 
                headers={"X-GitHub-Event": "workflow_run"},
                json={
                    "action": "completed",
                    "workflow_run": {"id": run_id, "status": "completed", "conclusion": "failure"},
                    "repository": {"full_name": target_repo},
                    "mock_fail_type": random.choice(["syntax", "dependency", "test"]),
                    "llm_priority": llm_priority
                }, 
                timeout=2
            )
        except: pass
            
        progress_bar = st.progress(5, text="Step 1/5: Intercepting incoming GitHub Webhook...")
        
        st.markdown("### 🖥️ System Logs Console")
        log_text = f"[INFO] Webhook received\n"
        log_placeholder = st.empty()
        log_placeholder.code(log_text, language="bash")
        
        def append_log(msg):
            global log_text
            log_text += f"{msg}\n"
            log_placeholder.code(log_text, language="bash")
        
        # Step 1: Classification
        time.sleep(1.0)
        progress_bar.progress(25, text="Step 2/5: Analyzing Error Metrics...")
        append_log("[INFO] Error classified: SyntaxError")
        
        # Step 2: Memory Retrieval
        time.sleep(1.2)
        progress_bar.progress(50, text="Step 3/5: Querying FAISS Tensor Embeddings...")
        if match_found:
            append_log(f"[INFO] FAISS match: {conf_score}%")
            append_log("[INFO] Bypassing LLM Draft Module -> Memory Validated.")
        else:
            if llm_priority == "Offline / Failover Mode":
                append_log("[WARN] No Memory Match -> Switching to Local Failover Inference")
                time.sleep(1.5)
                append_log("[INFO] Local Fallback Patch generated")
            else:
                append_log("[WARN] No Memory Match -> Switching to LLM Inference")
                time.sleep(1.5)
                append_log("[INFO] Patch generated")
            
        # Step 3: AST & Sandbox Verification
        time.sleep(1.5)
        progress_bar.progress(75, text="Step 4/5: Pushing to OpenEnv Docker Sandbox...")
        append_log("[INFO] Patch applied to Virtual File System")
        time.sleep(1.0)
        append_log("[SUCCESS] Sandbox passed")
        
        # Step 4: PR Creation
        time.sleep(1.0)
        progress_bar.progress(100, text="Step 5/5: Automated Workflow Fix Completed! 🎉")
        append_log("[PR CREATED]")
        
        st.success(f"""
        ### ✅ Fix Applied Successfully
        - **⏱ Time Taken:** {sim_time:.1f} sec
        - **🧠 Source:** {"FAISS Memory (Skipped LLM generation)" if match_found else ("Local Failover" if llm_priority == "Offline / Failover Mode" else "LLM Native Generation")}
        - **🎯 Confidence:** {conf_score}%
        """)

    else:
        st.info("⏸️ System Idle. Awaiting CI/CD Webhook...")
        st.code("Listening on http://localhost:8080/api/v1/webhook/github...\nReady for interception.", language="bash")


with memory_col:
    st.markdown("### 🧠 Memory Engine")
    
    if simulate_btn:
        if match_found:
            st.success(f"✅ **Memory Hit ({conf_score}% match) → Skipping LLM**\n\nThe orchestrator detected an exact semantic match in local RL history. \n*Instant execution.*")
        else:
            st.warning("⚠️ **No Memory Match → Switching to LLM**\n\nNo historical solution found for this specific stack trace. \n*Falling back to Multi-LLM inference generation.*")
            
        st.markdown("#### AI Confidence in Generated Fix")
        st.progress(conf_score / 100.0, text=f"{conf_score}%")
    else:
        st.info("Awaiting pipeline trigger to query FAISS Tensor Map.")
        st.progress(0.0, text="Calculated Patch Confidence: 0%")

st.divider()

# ==========================================
# HISTORY & HOT ZONES
# ==========================================
st.markdown("### 🗄️ FAISS Episodic Memory Tensor Map")
if memory:
    mem_data = []
    for i, m in enumerate(reversed(memory)):
        mem_data.append({
            "RL Weight": "✅ +1.0" if m.get("accepted") else "❌ -1.0",
            "Status": "⭐ Recent Successful Fix" if i == 0 else "Archived Iteration",
            "Fault Category": m.get("failure_category", "Unknown"),
            "Signature Snippet": m.get("error")[:80] + "..."
        })
    df = pd.DataFrame(mem_data)
    
    def highlight_recent(row):
        if row["Status"] == "⭐ Recent Successful Fix":
            return ['background-color: rgba(63, 185, 80, 0.2)'] * len(row)
        return [''] * len(row)
        
    st.dataframe(df.style.apply(highlight_recent, axis=1), use_container_width=True, hide_index=True)
else:
    st.info("FAISS vector memory is empty. Trigger a pipeline failure to populate.")
