from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Notes API")

NOTES_FILE = Path(os.getenv("NOTES_FILE", "data/notes.txt"))


def _read_notes() -> list[str]:
    if not NOTES_FILE.exists():
        return []
    content = NOTES_FILE.read_text(encoding="utf-8")
    return [line.strip() for line in content.splitlines() if line.strip()]


def _append_note(note: str) -> None:
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with NOTES_FILE.open("a", encoding="utf-8") as fh:
        fh.write(note.replace("\n", " ").strip() + "\n")


@app.get("/")
def root() -> JSONResponse:
    return JSONResponse({"message": "This is V2 for the Rolling Update test"})


@app.post("/add/{note}")
def add_note(note: str) -> JSONResponse:
    _append_note(note)
    return JSONResponse({"status": "ok", "note": note})


@app.get("/list")
def list_notes() -> JSONResponse:
    return JSONResponse({"notes": _read_notes()})
