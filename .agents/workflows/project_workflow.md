---
description: Running the Autonomous DevOps CI Fixing System Presentation flow for the Hackathon
---

# Autonomous AI DevOps Project Workflow

Follow these steps exactly to run the full presentation of your GitHub repair agents.

1. **Start the Tracing Dashboard**
   Open a terminal in the `github_agent_backend` directory and run the Streamlit tracer:
   ```powershell
   python -m streamlit run dashboard.py
   ```
   *This will pop open a browser window displaying the live execution telemetry.*

2. **Trigger the Pipeline**
   Open a second terminal in the same directory and execute the backend engine:
   ```powershell
   python run_everything.py
   ```

3. **Observe the Agentic Actions**
   Watch the terminal output as the orchestrator logs events from the `Analyzer`, `Fixer`, `Validator` Sandbox, and `PR Agent`.
   
4. **View the Dashboard & Pull Request**
   - Refresh the Streamlit dashboard to view the generated unified Git diff and the mathematical Episodic Memory traces. 
   - Open your GitHub repository to see the perfectly formatted Draft PR, complete with the `AI-Generated` priority labels and human-in-the-loop protection!
