## Behavioural Guidelines
- *** NEVER ASSUME OR GUESS ***
- When in doubt, ask for clarification or ask for help. More often than not, you can do websearch to find relevant examples of check ai_docs/ for examples that the user have added.
- **Always confirm file paths & module names** exist before using them.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.
- **KEEP README.md UPDATED**
- Whenever you make changes to the codebase, update the README.md file to reflect the changes. Especially if you add configuration changes or new features.
- Include a .env.example, README with instructions for setup and installation
- Include the project structure in the README
- Use python_dotenv and load_env() for environment variables


- If doing a web search or fetching a document on the web, prefer to use the gemini cli mcp web search tool before falling back to Claude's webfetch tool.