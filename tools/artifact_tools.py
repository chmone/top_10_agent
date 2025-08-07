"""
Custom artifact tools for saving and loading research findings
Uses local file storage for development and testing
"""

from typing import Any, Dict, List, Optional
from google.adk.tools.tool_context import ToolContext
from google.genai import types
import json
import hashlib
from datetime import datetime
import os
from pathlib import Path


async def save_research_artifact(
    category: str,
    artifact_type: str,  # 'search_results', 'analysis', 'recommendations'
    data: Dict[str, Any],
    tool_context: Optional[ToolContext] = None  # Optional for local storage
) -> Dict[str, Any]:
    """
    Save research findings as artifacts to local storage.
    
    Args:
        category: The product category being researched
        artifact_type: Type of artifact ('search_results', 'analysis', 'recommendations')
        data: The data to save as an artifact
        tool_context: ADK tool context (optional, for future cloud integration)
    
    Returns:
        Status and artifact ID
    """
    # Create local artifacts directory if it doesn't exist
    artifacts_dir = Path("agent/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename for the artifact
    timestamp = datetime.now().isoformat()
    artifact_id = hashlib.md5(f"{category}_{artifact_type}_{timestamp}".encode()).hexdigest()[:8]
    filename = f"{category}_{artifact_type}_{artifact_id}.json"
    filepath = artifacts_dir / filename
    
    # Add metadata to the artifact
    artifact_data = {
        'category': category,
        'type': artifact_type,
        'timestamp': timestamp,
        'data': data
    }
    
    # Save to local file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(artifact_data, f, indent=2)
    
    # Also save to ADK session if tool_context is available
    if tool_context:
        try:
            json_data = json.dumps(artifact_data, indent=2)
            artifact_part = types.Part(text=json_data)
            await tool_context.save_artifact(filename, artifact_part)
        except Exception as e:
            # If ADK save fails, local save is still successful
            pass
    
    return {
        'status': 'saved',
        'artifact_id': artifact_id,
        'filename': filename,
        'category': category,
        'type': artifact_type
    }


async def load_research_artifacts(
    tool_context: Optional[ToolContext] = None,
    category: Optional[str] = None,
    artifact_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Load saved research artifacts from local storage.
    
    Args:
        tool_context: ADK tool context (optional, not used for local loading)
        category: Filter by product category (optional)
        artifact_type: Filter by type (optional)
    
    Returns:
        List of matching artifacts
    """
    artifacts_dir = Path("agent/artifacts")
    results = []
    
    # Create directory if it doesn't exist
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    # Read all JSON files in the artifacts directory
    for filepath in artifacts_dir.glob("*.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                artifact_data = json.load(f)
                
                # Apply filters
                if category and artifact_data.get('category') != category:
                    continue
                if artifact_type and artifact_data.get('type') != artifact_type:
                    continue
                    
                results.append(artifact_data)
        except (json.JSONDecodeError, IOError) as e:
            # Skip files that can't be read or parsed
            continue
    
    # Sort by timestamp (newest first)
    results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return results


async def get_artifact_summary(
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Get a summary of all saved artifacts in local storage.
    
    Args:
        tool_context: ADK tool context (optional, not used for local loading)
    
    Returns:
        Summary of artifacts by category and type
    """
    # Load all artifacts
    artifacts = await load_research_artifacts(tool_context=tool_context)
    
    summary = {
        'total_artifacts': len(artifacts),
        'artifacts_directory': str(Path("agent/artifacts").absolute()),
        'by_category': {},
        'by_type': {},
        'recent_artifacts': []
    }
    
    for artifact in artifacts:
        category = artifact.get('category', 'unknown')
        artifact_type = artifact.get('type', 'unknown')
        
        # Count by category
        if category not in summary['by_category']:
            summary['by_category'][category] = 0
        summary['by_category'][category] += 1
        
        # Count by type
        if artifact_type not in summary['by_type']:
            summary['by_type'][artifact_type] = 0
        summary['by_type'][artifact_type] += 1
    
    # Add 5 most recent artifacts
    summary['recent_artifacts'] = [
        {
            'category': a.get('category'),
            'type': a.get('type'),
            'timestamp': a.get('timestamp')
        }
        for a in artifacts[:5]
    ]
    
    return summary
