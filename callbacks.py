"""
Simple callback functions for state management in the Top 10 Agent system
"""

from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from datetime import datetime
import uuid

# Create memory and session services
memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

async def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Simple initialization of session state.
    """
    # Initialize state only if needed
    if 'session_id' not in callback_context.state:
        callback_context.state['session_id'] = str(uuid.uuid4())[:8]
        callback_context.state['searches_count'] = 0
        callback_context.state['artifacts_saved'] = 0
        callback_context.state['start_time'] = datetime.now().isoformat()
    
    # Update last activity
    callback_context.state['last_activity'] = datetime.now().isoformat()
    
    # Simple search limit check
    if callback_context.state.get('searches_count', 0) >= 5:
        return types.ModelContent(
            parts=[types.Part(
                text="Search limit reached (5 searches per session). Please start a new session."
            )]
        )
    
    return None


async def after_agent_callback(callback_context: CallbackContext):
    """
    Simple update of last activity time.
    """
    callback_context.state['last_activity'] = datetime.now().isoformat()


async def before_model_callback(
    callback_context: CallbackContext, 
    llm_request: LlmRequest
):
    """
    Simple tracking of google_search and save_research_artifact calls.
    """
    # No return value needed - just update state
    pass


async def after_model_callback(
    callback_context: CallbackContext,
    llm_response: LlmResponse
):
    """
    Simple update after model response.
    Save session to memory when analyzer completes.
    """
    # Update last activity
    callback_context.state['last_activity'] = datetime.now().isoformat()
    

    print("ONE\n\n\n\n")
    # Check if this is the analyzer agent completing its analysis
    if hasattr(llm_response, 'content') and llm_response.content:
        # Check if analyzer agent is responding
        agent_name = getattr(callback_context, 'agent_name', '')
        print(agent_name+ "\n")
        print("TWO\n\n\n\n}")
        
        # If it's the analyzer agent, save session to memory
        if 'analyzer' in agent_name.lower() or 'list_analyzer' in agent_name.lower():
            callback_context.state['analyzer_completed'] = True
            callback_context.state['analysis_time'] = datetime.now().isoformat()
            print("THREE\n\n\n\n")
            # Get session from the invocation context and save to memory
            if hasattr(callback_context, '_invocation_context'):
                invocation_ctx = callback_context._invocation_context
                
                # Get session details
                app_name = getattr(invocation_ctx, 'app_name', 'top_10_agent')
                user_id = getattr(invocation_ctx, 'user_id', 'default_user')
                session_id = getattr(invocation_ctx, 'session_id', None)
                
                print("FOUR\n\n\n\n")

                if session_id:
                    print("FIVE\n\n\n\n")
                    try:
                        # Get the complete session from session service
                        complete_session = await session_service.get_session(
                            app_name=app_name,
                            user_id=user_id,
                            session_id=session_id
                        )
                        
                        if complete_session:
                            print("MEMORYYYYY\n\n\n\n")
                            # Add session to memory using InMemoryMemoryService
                            await memory_service.add_session_to_memory(complete_session)
                            callback_context.state['session_saved_to_memory'] = True
                            print(f"Session {session_id} saved to memory after analysis")
                    except Exception as e:
                        print(f"Failed to save session to memory: {e}")
    



def get_session_summary(callback_context: CallbackContext) -> dict:
    """
    Simple session summary.
    """
    state = callback_context.state

    return {
        'session_id': state.get('session_id', 'unknown'),
        'searches_count': state.get('searches_count', 0),
        'artifacts_saved': state.get('artifacts_saved', 0),
        'start_time': state.get('start_time', 'unknown'),
        'last_activity': state.get('last_activity', 'unknown')
    }


