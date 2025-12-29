# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required (demo application).

## Endpoints

### Health Checks

#### GET /health

Basic health check.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-29T23:00:00.000Z",
  "version": "0.1.0"
}
```

#### GET /health/ready

Readiness check for orchestration.

#### GET /health/live

Liveness check for container health.

---

### Workflows

#### POST /api/v1/workflows/execute

Execute a workflow.

**Request Body**:
```json
{
  "workflow_type": "code_review",
  "workspace_path": "/path/to/repo",
  "config": {}
}
```

**Workflow Types**:
- `code_review` - Full code analysis + build
- `pr_check` - Quick PR validation
- `dependency_audit` - Check dependencies

**Response** (200 OK):
```json
{
  "workflow_id": "abc-123",
  "status": "success",
  "data": {
    "workflow_type": "code_review",
    "agent_results": {
      "code_analyzer": {...},
      "builder": {...}
    },
    "summary": "Code Review Summary:\n..."
  }
}
```

**Error Response** (500):
```json
{
  "detail": "Workflow failed: error message"
}
```

#### GET /api/v1/workflows/{workflow_id}/status

Get workflow status.

**Response** (200 OK):
```json
{
  "workflow_id": "abc-123",
  "name": "code_review",
  "status": "completed",
  "created_at": "2025-12-29T23:00:00Z",
  "updated_at": "2025-12-29T23:05:00Z",
  "current_step": null,
  "completed_steps": ["analysis", "build"],
  "failed_steps": []
}
```

#### GET /api/v1/workflows/list

List all workflows.

**Response** (200 OK):
```json
{
  "workflows": [
    {
      "workflow_id": "abc-123",
      "name": "code_review",
      "status": "completed",
      "created_at": "2025-12-29T23:00:00Z",
      "updated_at": "2025-12-29T23:05:00Z"
    }
  ]
}
```

---

### Analysis

#### POST /api/v1/analysis/code

Analyze code in a workspace.

**Request Body**:
```json
{
  "workspace_path": "/path/to/repo"
}
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "todos": [
      {
        "type": "TODO",
        "file": "src/main.py",
        "line": "10",
        "content": "TODO: Implement feature"
      }
    ],
    "security_issues": [
      {
        "type": "security",
        "description": "Hardcoded password",
        "file": "src/config.py",
        "line": "5",
        "content": "password = 'secret123'"
      }
    ],
    "code_stats": {
      "total_files": 15,
      "python_files": 12,
      "total_lines": 1500,
      "test_files": 5
    },
    "summary": "Code Analysis Summary:\n..."
  },
  "warnings": [
    "Found 3 potential security issues"
  ],
  "execution_time_ms": 1250
}
```

#### POST /api/v1/analysis/build

Run build and tests.

**Request Body**:
```json
{
  "workspace_path": "/path/to/repo"
}
```

**Response** (200 OK):
```json
{
  "status": "success",
  "data": {
    "linting": {
      "passed": true,
      "tools": {
        "ruff": {
          "success": true,
          "output": "All checks passed!"
        },
        "black": {
          "success": true,
          "output": "All files formatted correctly"
        }
      }
    },
    "testing": {
      "passed": true,
      "pytest": {
        "success": true,
        "output": "10 passed in 2.5s"
      }
    },
    "type_checking": {
      "passed": true,
      "mypy": {
        "success": true,
        "output": "Success: no issues found"
      }
    },
    "summary": "Build Summary:\n✓ Linting: PASSED\n..."
  },
  "warnings": [],
  "execution_time_ms": 5000
}
```

---

## Example Usage

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST http://localhost:8000/api/v1/analysis/code \
  -H "Content-Type: application/json" \
  -d '{"workspace_path": "/path/to/repo"}'

# Execute workflow
curl -X POST http://localhost:8000/api/v1/workflows/execute \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "code_review",
    "workspace_path": "/path/to/repo"
  }'

# Get workflow status
curl http://localhost:8000/api/v1/workflows/{workflow_id}/status
```

### Python

```python
import httpx

# Analyze code
response = httpx.post(
    "http://localhost:8000/api/v1/analysis/code",
    json={"workspace_path": "/path/to/repo"}
)
result = response.json()
print(result["data"]["summary"])

# Execute workflow
response = httpx.post(
    "http://localhost:8000/api/v1/workflows/execute",
    json={
        "workflow_type": "code_review",
        "workspace_path": "/path/to/repo"
    }
)
workflow = response.json()
print(f"Workflow ID: {workflow['workflow_id']}")
```

### JavaScript

```javascript
// Analyze code
const response = await fetch('http://localhost:8000/api/v1/analysis/code', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ workspace_path: '/path/to/repo' })
});

const result = await response.json();
console.log(result.data.summary);
```

---

## Interactive Docs

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
