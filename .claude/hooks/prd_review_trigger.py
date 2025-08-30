#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from utils.constants import ensure_session_log_dir

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def parse_transcript_for_phase_completion(transcript_path):
    """
    Parse JSONL transcript to detect PRD phase completion and extract context.
    Returns dict with phase completion info or None if no completion detected.
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return None
        
    try:
        phase_completion_patterns = [
            "Phase completed:",
            "Implementation phase done:",
            "Ready for review:",
            "Phase complete:",
            "## Phase",
            "### Phase"
        ]
        
        # Read the JSONL file and look for completion patterns
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
            
        # Process recent messages (last 20 lines should capture phase completion)
        recent_messages = []
        for line in lines[-20:]:
            try:
                message = json.loads(line.strip())
                if message.get('type') == 'message' and message.get('role') == 'assistant':
                    recent_messages.append(message.get('content', ''))
            except json.JSONDecodeError:
                continue
                
        # Join recent assistant messages and check for patterns
        recent_content = '\n'.join(recent_messages)
        
        # Check for phase completion patterns
        phase_completed = any(pattern in recent_content for pattern in phase_completion_patterns)
        
        if phase_completed:
            # Extract additional context
            context = {
                "phase_completed": True,
                "transcript_path": transcript_path,
                "completion_detected_at": datetime.now().isoformat(),
                "recent_content_snippet": recent_content[-500:] if recent_content else "",  # Last 500 chars
                "total_messages": len(lines)
            }
            
            # Try to extract PRD file path from content
            if "PRD" in recent_content or "prds/" in recent_content:
                # Look for PRD file references
                content_lower = recent_content.lower()
                if "prds/" in content_lower:
                    context["prd_reference_found"] = True
                    
            return context
            
        return None
        
    except Exception as e:
        # Log error but don't fail
        return {"error": f"Failed to parse transcript: {str(e)}"}


def should_trigger_review(input_data, context):
    """
    Determine if code review should be triggered based on context.
    """
    # Only trigger for specific agents
    agent_name = input_data.get("agent_name", "")
    target_agents = ["code-implementation-agent", "implementation-agent"]
    
    if agent_name not in target_agents:
        return False, f"Agent '{agent_name}' not in target agents"
        
    # Don't trigger if stop_hook_active (prevent infinite loops)
    if input_data.get("stop_hook_active", False):
        return False, "Stop hook already active, preventing loop"
        
    # Check if phase completion was detected
    if not context or not context.get("phase_completed", False):
        return False, "No phase completion detected"
        
    # Check for errors in parsing
    if "error" in context:
        return False, f"Transcript parsing error: {context['error']}"
        
    return True, "Phase completion detected, triggering review"


def trigger_code_review(context, session_id, log_dir):
    """
    Trigger the code review agent with appropriate context.
    This is a placeholder for now - the actual triggering mechanism
    would need to integrate with Claude Code's agent invocation system.
    """
    
    # For now, just log the review trigger request
    # In a full implementation, this would invoke the code-review-agent
    
    review_request = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "trigger_source": "prd_review_trigger_hook",
        "context": context,
        "review_agent": "code-review-agent",
        "status": "review_requested"
    }
    
    # Log the review request
    review_log_path = log_dir / "prd_review_requests.json"
    
    if review_log_path.exists():
        with open(review_log_path, 'r') as f:
            try:
                review_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                review_data = []
    else:
        review_data = []
        
    review_data.append(review_request)
    
    with open(review_log_path, 'w') as f:
        json.dump(review_data, f, indent=2)
        
    return review_request


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help='Enable debug logging')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = {
            "timestamp": datetime.now().isoformat(),
            **json.loads(sys.stdin.read())
        }
        
        # Extract required fields
        session_id = input_data.get("session_id", "")
        transcript_path = input_data.get("transcript_path", "")
        
        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        
        # Parse transcript for phase completion
        context = parse_transcript_for_phase_completion(transcript_path)
        
        # Determine if review should be triggered
        should_trigger, reason = should_trigger_review(input_data, context)
        
        # Create log entry
        log_entry = {
            **input_data,
            "context": context,
            "should_trigger_review": should_trigger,
            "trigger_reason": reason,
            "hook_name": "prd_review_trigger"
        }
        
        if should_trigger:
            # Trigger code review
            review_request = trigger_code_review(context, session_id, log_dir)
            log_entry["review_request"] = review_request
            
        # Log the hook execution
        hook_log_path = log_dir / "prd_review_trigger.json"
        
        if hook_log_path.exists():
            with open(hook_log_path, 'r') as f:
                try:
                    hook_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    hook_data = []
        else:
            hook_data = []
            
        hook_data.append(log_entry)
        
        with open(hook_log_path, 'w') as f:
            json.dump(hook_data, f, indent=2)
            
        if args.debug:
            print(f"PRD Review Trigger: {reason}", file=sys.stderr)
            
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception as e:
        # Handle any other errors gracefully
        if args.debug:
            print(f"PRD Review Trigger Error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()