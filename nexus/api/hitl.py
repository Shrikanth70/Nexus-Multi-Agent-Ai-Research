from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from nexus.db.session import get_db
from nexus.db.models import DBTaskSession
from nexus.core.state import NexusState

router = APIRouter()

class HITLApprovalRequest(BaseModel):
    approved: bool
    feedback: str = ""

@router.post("/{session_id}/approve")
async def approve_task(session_id: str, request: HITLApprovalRequest, db: AsyncSession = Depends(get_db)):
    """Human-in-the-loop endpoint to approve or reject a paused agent task."""
    result = await db.execute(select(DBTaskSession).where(DBTaskSession.session_id == session_id))
    db_session = result.scalar_one_or_none()
    
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    state = NexusState.model_validate(db_session.state_json)
    if not state.is_paused_for_human:
        raise HTTPException(status_code=400, detail="Session is not waiting for human approval")
        
    if request.approved:
        state.is_paused_for_human = False
    else:
        state.is_paused_for_human = False
        state.add_error(state.current_agent, f"Human rejected: {request.feedback}")
        
    db_session.state_json = state.model_dump(mode="json")
    await db.commit()
    
    return {"status": "success", "session_id": session_id, "approved": request.approved}
