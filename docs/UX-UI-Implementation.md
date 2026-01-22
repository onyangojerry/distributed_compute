# UX/UI Implementation

## Current Improvements
- Shared API client (`src/api.js`) and config (`src/config.js`).
- StatusBar with connectivity, nodes, and files count.
- UploadForm: drag-and-drop via `react-dropzone`, progress bar, clear statuses.
- FileList: action buttons with open/download/delete and better visual states.

## Plan
- Confirm UI state and fix dev server/start commands.
- Introduce a reusable API client and config to stop hardcoding URLs.
- Improve the layout: status bar, better upload UX (drag-and-drop + progress), cleaner file list actions.
- Run the UI locally and verify it renders and talks to the backend.

## Next Steps
- Add top navigation and a light/dark theme toggle.
- Inline toasts for upload/delete actions and a “Refresh” button on the file list.
- Optionally pull a clean copy of the original repo into a new folder and port UI improvements.
