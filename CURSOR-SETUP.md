# Cursor Desktop — 用户级配置位置（macOS）

| 用途 | 路径 |
|------|------|
| 编辑器 settings.json | `~/Library/Application Support/Cursor/User/settings.json` |
| 全局状态 DB（模型 / YOLO / Base URL 等） | `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb` |
| 本机 User Rules 文件（不同步账号） | `~/.cursor/rules/*.mdc` |
| MCP / CLI | `~/.cursor/mcp.json`、`~/.cursor/cli-config.json` |
| 账号云同步 User Rules | Cursor Settings → Rules（存云端，不在本地纯文本） |

## 本机已落地的三层（对齐 Codex）

1. **指令**：`~/.cursor/rules/execution-first-unrestricted.mdc`
2. **运行免打扰**：`state.vscdb` → Agent `fullAutoRun` + `yoloEnableRunEverything`（脚本：`main/agent/unrestrict/gpt-bypass/scripts/apply-cursor-bypass-settings.py`）
3. **speculative 网关**：`main/agent/unrestrict/gpt-bypass` → `127.0.0.1:8999`，上游 CPA

详见 `ops/inventory/.secrets/gpt-bypass/README.md`。
