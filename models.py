from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DevOpsAction(BaseModel):
    """
    Action format that the LLM must generate to interact with the environment.
    """
    action_type: str = Field(description="Action to perform. e.g., 'analyze' or 'patch'")
    file_path: Optional[str] = Field(None, description="The file path to modify or analyze")
    patch_content: Optional[str] = Field(None, description="The precise code to insert or replace")

class DevOpsObservation(BaseModel):
    """
    State format returned by the environment on reset() and step().
    """
    system_state: str = Field(description="Overall status of the Virtual Repository.")
    ci_logs: str = Field(description="The Github Action traceback logs to analyze")
    target_files: List[str] = Field(default_factory=list, description="Files contextual to the error")
