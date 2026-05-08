---
agent: ask
---

Perform a security audit of this codebase to detect any potential voulnerabilities in this project.

Output your findings as a markdown formatted table with the following columns (ID should start with 1 and auto-increment, File Path should be a link to the file): "ID", "Severity", "Issue", "File Path", "Line Number(s)", "Recommendation".

Next ask the user which issues they want to fix by either replying "all", or a comma separeted list of IDs. After their reply, run a separate sub agent (#runSubagent) to fix each issue that the user has specified. Each sub agent should report with a simple `subAgentSuccess: true | false`. 