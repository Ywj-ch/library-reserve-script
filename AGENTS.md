# AGENTS.md - Coding Agent Guidelines

This document provides guidelines for AI coding agents working in this codebase.

## Project Overview

This is a library seat reservation automation system with:
- **Backend**: FastAPI (Python 3.8+)
- **Frontend**: Vue 3 + TypeScript + Tailwind CSS
- **Architecture**: Monorepo with separate backend/ and frontend/ directories

## Build/Lint/Test Commands

### Backend (Python/FastAPI)

```bash
# Install dependencies
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the batch file
run.bat

# Test configuration (manual testing)
cd ..
python scripts\test_reserve.py

# Run main reservation script
python reserve_seat.py
```

**Note**: No formal Python linter (pylint/black) or test framework (pytest) is currently configured. Manual testing is done via `scripts/test_reserve.py` and API documentation at http://localhost:8000/docs.

### Frontend (Vue 3 + TypeScript)

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Format code
npm run format

# Or use the batch file
run.bat
```

**Running a Single Test**: No automated test suite exists. To test manually:
1. Start backend: `cd backend && run.bat`
2. Start frontend: `cd frontend && run.bat`
3. Access http://localhost:5173
4. Use API docs at http://localhost:8000/docs for backend testing

## Code Style Guidelines

### Python Backend Style

#### Imports
```python
# Order: Standard library → Third-party → Local imports
import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.config_service import ConfigService
from ..models.auth import AuthConfig
```

#### Naming Conventions
- **Classes**: PascalCase (e.g., `ConfigService`, `AuthConfig`)
- **Functions/Methods**: snake_case (e.g., `get_auth_config`, `update_section`)
- **Variables**: snake_case (e.g., `config_path`, `days_remaining`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_ATTEMPTS`)
- **Private methods**: Prefix with underscore (e.g., `_lock`)

#### Type Annotations
- Use type hints for function parameters and return types
- Import types from `typing` module (Dict, Any, Optional, List)
- Pydantic models for data validation and serialization

```python
def get_auth_config(self) -> AuthConfigResponse:
    auth_data = self.yaml_handler.get_section('auth')
    return AuthConfigResponse(...)

async def update_config(config_update: ConfigUpdate) -> Dict[str, Any]:
    ...
```

#### Error Handling
- Use try-except blocks for error handling
- Raise HTTPException in FastAPI routes
- Log errors with logging module
- Return structured error responses

```python
try:
    config = config_service.get_full_config()
    return {"success": True, "data": config}
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

#### Pydantic Models
- Define separate models for request/response/update operations
- Use Field() for validation and documentation
- Include description and examples

```python
class AuthConfig(BaseModel):
    cookie: str = Field(..., description="用户认证 Cookie")
    code: str = Field(..., description="预约验证码")
    last_update: str = Field(default_factory=lambda: datetime.now().isoformat())

class AuthConfigUpdate(BaseModel):
    cookie: str = Field(..., description="用户认证 Cookie")
    code: str = Field(..., description="预约验证码")

class AuthConfigResponse(BaseModel):
    cookie: str
    code: str
    days_remaining: int = Field(..., description="剩余天数")
```

#### FastAPI Routers
- Use APIRouter with prefix and tags
- Async functions for all route handlers
- Return Dict[str, Any] with success/data/message structure

```python
router = APIRouter(prefix="/api/config", tags=["配置管理"])

@router.get("")
async def get_config() -> Dict[str, Any]:
    try:
        config = config_service.get_full_config()
        return {"success": True, "data": config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### TypeScript/Vue Frontend Style

#### Prettier Configuration
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

**Important**: Run `npm run format` before committing frontend changes.

#### Imports
```typescript
// Vue and libraries first
import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'

// Components (use @ alias)
import Card from '@/components/common/Card.vue'
import Button from '@/components/common/Button.vue'

// Types
import type { Config } from '@/types/config'
import type { ApiResponse } from '@/types/api'

// API and stores
import { configApi } from '@/api/config'
import { useConfigStore } from '@/stores/config'
```

#### Naming Conventions
- **Components**: PascalCase (e.g., `ConfigPanel.vue`, `SeatManager.vue`)
- **Variables/Functions**: camelCase (e.g., `localSeats`, `handleSave`)
- **Interfaces/Types**: PascalCase (e.g., `AuthConfig`, `ApiResponse`)
- **Props**: camelCase in TypeScript, kebab-case in templates
- **Composables**: Prefix with `use` (e.g., `useConfigStore`)

#### Vue 3 Composition API
- Always use `<script setup lang="ts">`
- Define props with interface and defineProps
- Define emits with typed defineEmits
- Use ref/reactive for state, computed for derived state

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  cookie: string
  code: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  save: [cookie: string, code: string]
  test: []
}>()

const localCookie = ref(props.cookie)
const saving = ref(false)

async function handleSave() {
  saving.value = true
  try {
    emit('save', localCookie.value, localCode.value)
  } finally {
    saving.value = false
  }
}
</script>
```

#### Type Definitions
- Define interfaces in `src/types/` directory
- Use explicit type annotations for props, emits, API responses
- Avoid `any` - use `unknown` or specific types

```typescript
// types/config.ts
export interface Seat {
  id: string
  name: string
  enabled: boolean
}

export interface AuthConfig {
  cookie: string
  code: string
  last_update: string
  days_remaining: number
}

// types/api.ts
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}
```

#### API Functions
- Organize by domain in `src/api/` directory
- Return typed ApiResponse promises
- Use async/await

```typescript
// api/config.ts
export const configApi = {
  async getFullConfig(): Promise<ApiResponse<Config>> {
    return api.get('/config')
  },

  async updateAuthConfig(data: { cookie: string; code: string }): Promise<ApiResponse<AuthConfig>> {
    return api.put('/config/auth', data)
  },
}
```

#### Pinia Stores
- Use setup stores with defineStore and arrow function
- Export state and actions from the store

```typescript
export const useConfigStore = defineStore('config', () => {
  const config = ref<Config | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchConfig() {
    try {
      loading.value = true
      const response = await configApi.getFullConfig()
      if (response.success) {
        config.value = response.data
      }
    } catch (e: any) {
      error.value = e.message || '获取配置失败'
    } finally {
      loading.value = false
    }
  }

  return { config, loading, error, fetchConfig }
})
```

#### Error Handling
- Use try-catch blocks
- Set error state for user feedback
- Log errors to console
- Show user-friendly error messages

```typescript
try {
  await configStore.updateAuth(cookie, code)
  alert('保存成功！')
} catch (error) {
  alert('保存失败，请重试')
} finally {
  saving.value = false
}
```

### General Guidelines

#### File Organization
- Backend: `backend/app/{models,services,routers,utils}/`
- Frontend: `frontend/src/{components,views,api,stores,types}/`
- One class/component per file
- Match file names with exported class/component name

#### Comments
- Use Chinese for comments and docstrings (project is in Chinese)
- Add docstrings for public functions/methods
- Comment complex logic

#### Security
- NEVER commit config.yaml (contains secrets)
- Validate all user inputs
- Use environment variables for sensitive data in production
- Don't expose internal errors to users

#### Testing Approach
Since no formal test framework exists:
1. Test backend APIs via Swagger UI (http://localhost:8000/docs)
2. Test frontend manually in browser (http://localhost:5174)
3. Run `python scripts\test_reserve.py` to validate configuration
4. Check logs in `logs/reserve_seat.log`

## Project-Specific Notes

- This is a library seat reservation system for Hunan Normal University
- Cookie/Code authentication expires after ~10 days
- Configuration is managed via config.yaml
- Frontend provides a visual interface for configuration management
- Backend exposes REST API for CRUD operations on config
- Main reservation script (reserve_seat.py) runs as scheduled task
