"""
Simple callback functions for state management in the Top 10 Agent system
"""

from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from datetime import datetime
import uuid


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
    """
    # Update last activity
    callback_context.state['last_activity'] = datetime.now().isoformat()
    
    # Check if response has function calls and track them
    if hasattr(llm_response, 'content') and llm_response.content:
        if hasattr(llm_response.content, 'parts') and llm_response.content.parts:
            for part in llm_response.content.parts:
                # Track function calls in the response
                if hasattr(part, 'function_call') and part.function_call:
                    func_name = part.function_call.name
                    
                    # Track searches
                    if func_name == 'google_search':
                        count = callback_context.state.get('searches_count', 0)
                        callback_context.state['searches_count'] = count + 1
                    
                    # Track artifacts
                    elif func_name == 'save_research_artifact':
                        saved = callback_context.state.get('artifacts_saved', 0)
                        callback_context.state['artifacts_saved'] = saved + 1


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
