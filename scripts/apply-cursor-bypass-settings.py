#!/usr/bin/env python3
"""Patch Cursor Desktop reactiveStorage for GptBypass + stronger auto-run.

Prefer quitting Cursor before running. If Cursor is open, it may overwrite
on quit — re-run after quit, or set Override Base URL in the UI.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import time
from pathlib import Path

DB = Path.home() / "Library/Application Support/Cursor/User/globalStorage/state.vscdb"
KEY = "src.vs.platform.reactivestorage.browser.reactiveStorageServiceImpl.persistentStorage.applicationUser"
BASE_URL = os.environ.get("CURSOR_GPT_BYPASS_BASE_URL", "http://127.0.0.1:8999/v1")


def main() -> None:
    if not DB.exists():
        raise SystemExit(f"missing {DB}")
    bak = DB.with_suffix(f".vscdb.bak-gptbypass-{time.strftime('%Y%m%d%H%M%S')}")
    shutil.copy2(DB, bak)
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    row = cur.execute("SELECT value FROM ItemTable WHERE key=?", (KEY,)).fetchone()
    if not row:
        raise SystemExit(f"missing key {KEY}")
    data = json.loads(row[0])

    data["openAIBaseUrl"] = BASE_URL
    data["useOpenAIKey"] = True

    cs = data.setdefault("composerState", {})
    cs["yoloEnableRunEverything"] = True
    cs["yoloOutsideWorkspaceDisabled"] = False
    cs["doNotShowFullYoloModeWarningAgain"] = True
    cs["autoAcceptWebSearchTool"] = True
    for mode in cs.get("modes4") or []:
        if mode.get("id") == "agent":
            mode["autoRun"] = True
            mode["fullAutoRun"] = True

    cur.execute("UPDATE ItemTable SET value=? WHERE key=?", (json.dumps(data, ensure_ascii=False), KEY))
    con.commit()
    con.close()
    print(f"ok: openAIBaseUrl={BASE_URL} useOpenAIKey=true yoloEnableRunEverything=true")
    print(f"backup: {bak}")
    print("UI still required: Settings → Models → paste OpenAI API Key (CPA key or any placeholder)")
    print("Add custom model name: gpt-6-astra  then select it in Agent")


if __name__ == "__main__":
    main()
