# API Standards

- Versioning: Prefix endpoints with `/v1` when introducing breaking changes.
- Auth: Use `X-API-KEY` header; reject missing/wrong keys with 401.
- Consistency: JSON responses; snake_case keys; include `message` or `error` field.
- Pagination: For lists, support `?page=&page_size=` in future.
- Errors: Return meaningful messages, avoid stack traces. Use standard HTTP codes.
- CORS: Allow known dev ports (5173, 5174) and production host.

## Endpoints (current)
- GET `/files` → `{ files: string[] }`
- POST `/upload` (multipart `file`) → `{ message, used_nodes }`
- GET `/download/{filename}` → FileResponse
- DELETE `/delete/{filename}` → `{ message } | { error }`
- POST `/register` → `{ message, total }`
- GET `/nodes` → `{ nodes: string[] }`
