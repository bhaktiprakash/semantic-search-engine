# Security Policy

## Overview

This project processes Excel files, sends spreadsheet-derived content to an LLM, generates embeddings, and stores indexed data in ChromaDB.

Users should treat spreadsheet files and indexed data as potentially sensitive.

## Security Considerations

### Sensitive Data

Spreadsheet contents may be sent to the configured Gemini API. Do not process confidential or regulated data unless the use of the external LLM service has been approved.

API keys and secrets must never be committed to the repository.

### Untrusted Excel Files

Treat uploaded or automatically detected `.xlsx` files as untrusted input.

Deployments should enforce:

- File size and processing limits
- Reasonable row, column, and worksheet limits
- Up-to-date `pandas` and `openpyxl` dependencies
- Restricted permissions on directories monitored by the file watcher

Macros or executable content must not be executed.

### Prompt Injection

Spreadsheet cells may contain malicious instructions intended to influence the LLM.

Spreadsheet content must be treated as **untrusted data**, not as instructions. LLM output should also be treated as untrusted and validated before being used by the application.

### ChromaDB

The ChromaDB index may contain spreadsheet-derived content in addition to embeddings.

Protect the index from unauthorized access and do not commit generated index files or sensitive data to source control.

For multi-user deployments, access controls must be enforced before retrieving documents for the LLM.

### Resource Limits

Large or malicious spreadsheets may cause excessive CPU, memory, storage, or LLM API usage.

Production deployments should implement appropriate:

- File-size limits
- Processing timeouts
- LLM request/token limits
- Rate limits and quotas

## Reporting a Vulnerability

Please report security vulnerabilities privately to the project maintainers rather than opening a public issue.

Include:

- A description of the vulnerability
- Steps to reproduce
- Affected component
- Potential impact
- Proof of concept, if available

Do not include real credentials, confidential spreadsheets, or other sensitive information in reports.
