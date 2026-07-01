from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
import asyncio
import json

from nexus.db.session import get_db
from nexus.db.models import DBTaskSession
from nexus.core.state import NexusState

# Note: In Phase 2, we should use the LangGraph workflow.
# For now, we mock the execution loop or use the state machine.
# This ensures it compiles while the user migrates from Phase 1.
try:
    from nexus.core.graph import workflow_graph
except ImportError:
    workflow_graph = None

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)

manager = ConnectionManager()

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    session_id: str
    status: str

async def run_workflow_background(session_id: str, db: AsyncSession):
    result = await db.execute(select(DBTaskSession).where(DBTaskSession.session_id == session_id))
    db_session = result.scalar_one_or_none()
    if not db_session:
        return
        
    state = NexusState.model_validate(db_session.state_json)
    
    if workflow_graph:
        def _run():
            return workflow_graph.invoke(state.model_dump(mode="json"))
            
        try:
            final_state_dict = await asyncio.to_thread(_run)
            db_session.state_json = final_state_dict
            await db.commit()
            await manager.broadcast(session_id, {"type": "completed", "state": final_state_dict})
        except Exception as e:
            await manager.broadcast(session_id, {"type": "error", "message": str(e)})
    else:
        # Placeholder for Phase 1 / manual orchestrator
        await manager.broadcast(session_id, {"type": "info", "message": "workflow_graph not found."})

@router.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    state = NexusState(user_query=request.query)
    
    db_session = DBTaskSession(
        session_id=state.session_id,
        user_query=state.user_query,
        state_json=state.model_dump(mode="json")
    )
    db.add(db_session)
    await db.commit()
    
    background_tasks.add_task(run_workflow_background, state.session_id, db)
    return ResearchResponse(session_id=state.session_id, status="started")

@router.get("/tasks/{session_id}")
async def get_task_status(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBTaskSession).where(DBTaskSession.session_id == session_id))
    db_session = result.scalar_one_or_none()
    if not db_session:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_session.state_json

@router.websocket("/ws/tasks/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            # We don't expect messages from the client right now
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
