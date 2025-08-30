```markdown
# Product Requirements Document (PRD): Claude Code Ecosystem

## 1. Introduction

Claude Code is an **AI assistant designed to enhance developer productivity** by streamlining coding workflows and providing intelligent assistance. It offers a versatile platform for building with Claude through features like subagents, output styles, hooks, and the Model Context Protocol (MCP). The system aims to provide **deterministic control over AI behavior** and facilitate deep integration with external tools and models.

## 2. Vision and Goals

The vision for the Claude Code ecosystem is to empower developers with a highly **customizable, extensible, and intelligent AI coding environment**. It seeks to offer advanced capabilities for managing complex development tasks, enabling sophisticated multi-AI collaboration, and automating routine actions.

**Key goals include:**

*   **Customization & Extensibility**: Allow users to precisely tailor Claude Code's behavior through user-defined shell commands (hooks) and seamlessly integrate with external services and other LLMs via the Model Context Protocol (MCP).
*   **Enhanced Productivity**: Accelerate common development tasks, automate repetitive actions, and provide intelligent, context-aware assistance throughout the entire software development lifecycle.
*   **Intelligent Workflow Management**: Enable efficient delegation of specialized tasks to AI subagents and provide robust mechanisms for managing long-running processes in the background.
*   **Multi-AI Collaboration**: Facilitate dynamic interactions and collaboration between Claude Code and other leading AI models, fostering a powerful "teamwork" approach to problem-solving.
*   **Security & Control**: Implement robust mechanisms for governing AI actions, ensuring adherence to codebase conventions, and enforcing critical security best practices within development workflows.

## 3. Key Features

### 3.1. Claude Code Core AI Assistant

*   Serves as the **primary AI assistant for interactive coding sessions**.
*   Supports various advanced models, including **Claude 4.1 Opus and Sonnet**.
*   Manages **stateful conversation history** and offers configurable memory management options.

### 3.2. Model Context Protocol (MCP)

*   A **standardized protocol that allows Claude Code to bridge with external AI models and services**.
*   Enables **communication with other LLMs**, such as Google's Gemini CLI, and access to **over 400+ AI models via OpenRouter integration**.
*   MCP servers can **expose specialized tools and prompts as slash commands** directly within the Claude Code interface.
*   **Example**: The Gemini CLI MCP Server offers **33 specialized tools** across 6 categories for comprehensive multi-AI integration, including analysis, code review, and AI collaboration tools.

### 3.3. Hooks

*   **User-defined shell commands that execute at various points in Claude Code’s lifecycle**.
*   Provide **deterministic control over Claude Code’s behavior**, ensuring specific actions always occur rather than relying on the LLM's choice.
*   **Configuration**: Hooks are defined in settings files such as `~/.claude/settings.json` (user), `.claude/settings.json` (project), or `.claude/settings.local.json`.
*   **Hook Events**: Support a range of events including:
    *   `PreToolUse`: Runs before tool calls and can block them.
    *   `PostToolUse`: Runs after tool calls complete.
    *   `UserPromptSubmit`: Runs when the user submits a prompt, before Claude processes it.
    *   `Notification`: Runs when Claude Code sends notifications.
    *   `Stop` / `SubagentStop`: Runs when the main agent or a subagent finishes responding.
    *   `PreCompact`: Runs before a compact operation.
    *   `SessionStart` / `SessionEnd`: Runs when a session starts or ends.
*   **Matchers**: Can use patterns (e.g., `Write`, `Edit|Write`, `*`, `mcp__<server>__.*`) to target specific tool names or types, including MCP tools.
*   **Input/Output**: Hooks receive JSON data via stdin containing session and event-specific information. They communicate status through **exit codes** (0 for success, 2 for blocking error) or **structured JSON output** for advanced control (e.g., `continue`, `stopReason`, `permissionDecision`).
*   **Key Use Cases**: **Notifications**, **automatic formatting** (e.g., `prettier`, `gofmt`), **logging** of executed commands, providing **automated feedback**, and implementing **custom permissions** to block modifications to sensitive files.

### 3.4. Subagents

*   **Specialized AI assistants** that can be invoked to handle specific types of tasks.
*   Each subagent operates with its **own context window**, preventing pollution of the main conversation and enabling **specialized expertise** with fine-tuned instructions.
*   **Configurable Tool Access**: Subagents can be granted access to specific internal tools or inherit all tools from the main thread, including MCP tools.
*   **Storage**: Defined as Markdown files with YAML frontmatter in project (`.claude/agents/`) or user (`~/.claude/agents/`) directories.
*   **Invocation**: Can be automatically delegated tasks based on their `description` field or explicitly invoked by mentioning them in a prompt.
*   **Examples**: Pre-configured subagents include a **code reviewer**, **debugger**, and **data scientist**, each with tailored instructions and tool access.

### 3.5. Slash Commands

*   **Interactive commands** that allow users to control Claude Code's behavior during a session.
*   **Built-in commands**: Include `/add-dir`, `/agents`, `/clear`, `/compact`, `/mcp`, `/model`, `/review`, `/status`, and more for common operations.
*   **Custom slash commands**: User-defined prompts stored as Markdown files in `.claude/commands/` (project-specific) or `~/.claude/commands/` (personal).
    *   Support features like **namespacing**, passing **arguments** (`$ARGUMENTS`, `$1`, `$2`), executing **bash commands** (`!`), and referencing **file contents** (`@`).
*   **MCP slash commands**: **Dynamically discovered** from connected MCP servers and follow the pattern `/mcp__<server-name>__<prompt-name>`.

### 3.6. Background Commands

*   Allows users to **execute long-running shell commands in the background without blocking their workflow**.
*   **Execution Methods**:
    *   **Keyboard Shortcut**: Press `Ctrl+B` when Claude suggests a command.
    *   **Programmatic**: Use the `run_in_background: true` parameter within the Bash tool.
    *   **Prompt Instructions**: Request background execution directly in natural language prompts.
*   **Tools**: Utilizes `BashTool` for command execution, `BashOutputTool` to retrieve incremental output, and `KillBashTool` to terminate tasks.
*   **Interactive Management**: The `/bashes` command provides an interactive menu to view, check status, monitor output, and kill all running or completed background shells.
*   **Session Persistence**: Background tasks **automatically persist across Claude Code sessions**, meaning they continue running even after exiting Claude Code.
*   **Key Use Cases**: Starting development servers, monitoring real-time application logs, managing build processes, and debugging while continuing other development tasks.

## 4. Use Cases / User Stories

*   **As a developer, I want to automatically format my TypeScript files after editing**, so that I maintain consistent code style without manual intervention.
*   **As a team lead, I need to track and count all executed commands for compliance audits**, so that I have a clear and comprehensive audit trail of AI actions.
*   **As a security engineer, I want to block modifications to production files or sensitive directories**, so that I can enforce security policies and prevent accidental or unauthorized changes.
*   **As a developer, I want to receive desktop notifications when Claude Code is awaiting my input**, so that I don't miss important prompts or permissions requests.
*   **As a power user, I want to integrate Google's Gemini CLI with Claude Code**, so that I can leverage Gemini's specialized tools and capabilities directly within my Claude Code workflow.
*   **As a developer, I want Claude Code to perform a deep analysis of my codebase and then delegate the same codebase to Google Gemini for a second opinion**, so that I can get synthesized insights from multiple AI models.
*   **As a senior engineer, I want an AI subagent to proactively review newly written or modified code for quality, security, and maintainability**, so that I can ensure high code standards are consistently met.
*   **As a developer, I want to start a development server (e.g., `npm run dev`) and monitor its logs in the background**, so that I can continue working on other tasks without blocking my terminal.
*   **As a lead developer, I want to prevent "Context Rot" during long coding sessions**, by having an external AI (like Codex CLI/GPT-5 High) critique Claude's generated code and identify duplicate functions or distractors.

## 5. Technical Details

### 5.1. Architecture

*   The Gemini CLI MCP Server features a **modular, enterprise-grade architecture** with 83 Python files across specialized modules.
*   `mcp_server.py` functions as the **main coordinator** for tool registration and service orchestration.
*   Built on the `FastMCP` framework, adhering to the **JSON-RPC 2.0 protocol** for efficient MCP communication.
*   Leverages an **async architecture** capable of supporting **1,000-10,000+ concurrent requests** for high performance in the MCP server.
*   Employs **Redis-backed storage** for scalable and stateful conversation history management, with graceful memory fallback.

### 5.2. Configuration

*   Settings for Claude Code and its components are stored in standard JSON files: `~/.claude/settings.json` (user-level), `.claude/settings.json` (project-level), `.claude/settings.local.json` (local project), or enterprise managed policy settings.
*   MCP server configuration involves adding the server via the `claude mcp add` command, specifying absolute paths to the Python executable and `mcp_server.py`.
*   The Gemini CLI MCP server supports **extensive configuration via environment variables**, controlling aspects like command timeouts, logging levels, retry mechanisms, tool-specific character limits, automatic model fallback, rate limiting, OpenRouter API keys, conversation management settings, Cloudflare AI Gateway integration, and enterprise monitoring (OpenTelemetry, Prometheus).

### 5.3. Security

*   **Hooks**: Hooks execute **arbitrary shell commands** on the user's system using **current environment credentials**. This necessitates a **thorough review of all hook implementations** before registration.
*   **Security Best Practices for Hooks**:
    *   **Validate and sanitize all inputs** to prevent injection vulnerabilities.
    *   **Always quote shell variables** (e.g., `"$VAR"`) to avoid command injection.
    *   **Block path traversal** by checking for `..` in file paths.
    *   **Use absolute paths** for scripts (leveraging `$CLAUDE_PROJECT_DIR`).
    *   **Skip sensitive files** (e.g., `.env`, `package-lock.json`, `.git/` directories) from hook operations.
*   **Configuration Safety**: Claude Code captures a snapshot of hooks at startup, ignores external modifications during a session, and requires review in the `/hooks` menu to apply changes, preventing malicious runtime alterations.
*   **Gemini CLI MCP Server**: Incorporates **22 critical security fixes**, a **multi-layer defense** against 25+ attack categories, and **real-time security pattern detection** (e.g., for command injection, path traversal, XSS, prompt injection, information disclosure).
*   Includes **JSON-RPC security middleware** for protocol-level validation, request size limits, and nesting depth protection.

### 5.4. Integrations

*   **OpenRouter API**: Provides access to **400+ AI models** from over 20 providers (including OpenAI, Anthropic, Meta, Google, etc.) through the Gemini CLI MCP server.
*   **Cloudflare AI Gateway**: Optional integration for routing OpenRouter requests, potentially enhancing performance and security.
*   **OpenTelemetry + Prometheus**: Supports enterprise-grade monitoring and observability for the Gemini CLI MCP server, including distributed tracing and metrics collection.
*   **GitHub Actions**: Mentioned as a key "Build with Claude Code" feature.

## 6. Future Enhancements / Considerations

*   **Advanced Context Management**: Further develop strategies to mitigate "Context Rot" challenges, potentially through more sophisticated summarization, intelligent content filtering, or dynamic context chunking.
*   **Automated Background Command Detection**: Implement smarter, **context-aware auto-detection for long-running commands**, enabling Claude to automatically trigger background execution without explicit user instruction.
*   **Visual Management Tools**: Develop a **graphical user interface (UI) for managing background tasks and subagents**, offering a more intuitive and visual way to monitor and control AI-driven workflows.
*   **Enhanced Task Orchestration**: Introduce advanced features such as **task dependency graphs**, **automatic restart policies**, and deeper **integration with container orchestration platforms** for background processes.
*   **Cross-Session Task Migration**: Explore and implement features for seamless migration of background tasks between different Claude Code sessions or even different development environments.
*   **Refined AI Collaboration**: Continue to build out more sophisticated collaboration modes and tighter integration points between Claude Code and external AI models via the MCP, possibly including structured debate or validation workflows.
```