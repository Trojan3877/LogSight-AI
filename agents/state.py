# agents/state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentState(BaseModel):
    """
    The immutable single source of truth passed across the LogSight-AI lifecycle.
    Prevents side effects and provides explicit telemetry for debugging.
    """
    raw_logs: str
    parsed_json: Optional[List[Dict[str, Any]]] = None
    security_threats: List[str] = Field(default_factory=list)
    root_cause_analysis: Optional[str] = None
    recommended_actions: Optional[str] = None
    
    # Observability & Guardrails Telemetry
    execution_steps: List[str] = Field(default_factory=list)
    loop_count: int = 0
    circuit_tripped: bool = False
    failure_reason: Optional[str] = None

    def log_step(self, step_description: str) -> "AgentState":
        """Returns a new copy of state with the updated execution trace."""
        updated_steps = list(self.execution_steps) + [step_description]
        return self.model_copy(update={"execution_steps": updated_steps})
