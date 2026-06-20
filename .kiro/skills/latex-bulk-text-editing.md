# LaTeX Bulk Text Editing Workflow

## Purpose
This skill provides a workflow for bulk text editing operations in LaTeX files (e.g., citation conversion, text replacements) while temporarily disabling the auto-compilation hook to prevent multiple unnecessary compilations during the editing process.

## When to Use
- Converting multiple inline citations to footnotes
- Performing batch text replacements across sections
- Making multiple sequential edits to LaTeX files
- Any operation involving 5+ consecutive file modifications

## Workflow Steps

### 1. Disable Auto-Compilation Hook
Before starting any bulk text editing:

```javascript
// Read the hook file
const hookPath = "c:\\development\\PrivProjects\\BachlorsThesis\\.kiro\\hooks\\latex-compile-after-tool-edit.kiro.hook";
const hook = JSON.parse(readFile(hookPath));

// Set enabled to false
hook.enabled = false;

// Write back
writeFile(hookPath, JSON.stringify(hook, null, 2));
```

Use the file editing tools to:
1. Read `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
2. Change `"enabled": true` to `"enabled": false`
3. Save the file

### 2. Perform Bulk Edits
Now perform all your text editing operations:
- Use `str_replace` for each citation conversion
- Make multiple sequential edits
- Work through all target sections

The hook will NOT trigger during these edits, preventing multiple compilations.

### 3. Re-Enable Auto-Compilation Hook
After ALL edits are complete:

```javascript
// Read the hook file again
const hook = JSON.parse(readFile(hookPath));

// Set enabled back to true
hook.enabled = true;

// Write back
writeFile(hookPath, JSON.stringify(hook, null, 2));
```

Use the file editing tools to:
1. Read `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
2. Change `"enabled": false` back to `"enabled": true`
3. Save the file

### 4. Final Compilation
After re-enabling the hook, run ONE final compilation:

```powershell
.\scripts\compile.ps1
```

This ensures the document compiles successfully with all changes applied.

## Example: Citation Conversion Workflow

### Step 1: Disable Hook
```
str_replace on latex-compile-after-tool-edit.kiro.hook:
  "enabled": true  →  "enabled": false
```

### Step 2: Convert Citations
```
For each inline citation like "(vgl. Author 2016, S. 123)":
  - Use str_replace to convert to \vglfootcite[123]{Author2016}
  - Repeat for all citations in target sections
```

### Step 3: Re-Enable Hook
```
str_replace on latex-compile-after-tool-edit.kiro.hook:
  "enabled": false  →  "enabled": true
```

### Step 4: Compile
```
execute_pwsh: .\scripts\compile.ps1
```

## Benefits
- **Performance**: Prevents 10-15 unnecessary compilations during bulk edits
- **Efficiency**: Each LaTeX compilation takes ~10 seconds, saving 2-3 minutes
- **Clarity**: Single compilation at the end provides clear feedback
- **Hook Safety**: Hook remains functional for future single-file edits

## Important Notes
1. **Always re-enable the hook** after bulk editing is complete
2. The hook file is located at: `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
3. Only the `"enabled"` field should be toggled (true ↔ false)
4. Do not modify other hook properties
5. If you forget to re-enable, the hook won't work for future edits

## Verification
After re-enabling the hook, verify it's active:
1. Make a small test edit to any .tex file
2. Save the file
3. The auto-compilation should trigger
4. You should see a notification when compilation completes

## Hook Configuration Reference
```json
{
  "enabled": true,  // ← Toggle this field
  "name": "Auto-compile LaTeX after edits",
  "description": "Automatically compiles the thesis when .tex or .bib files are modified",
  "version": "1",
  "when": {
    "type": "postToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "runCommand",
    "command": "pwsh -ExecutionPolicy Bypass -Command \"...\""
  }
}
```
