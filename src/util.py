import logging
import hashlib
from typing import Dict, Any

from fastapi import UploadFile

LOG_FORMAT = "[%(asctime)s][%(levelname)s] %(message)s"
LOG_DATEFMT = "%d/%m/%Y %H:%M:%S"
CHUNK = 1024


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATEFMT
    )


def mquery_version() -> str:
    return "1.4.0"


def make_sha256_tag(filename: str) -> Dict[str, Any]:
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return {"display_text": sha256_hash.hexdigest(), "hidden": True}


def get_sha256(file: UploadFile) -> str:
    m = hashlib.sha256()

    while c := file.file.read(CHUNK):
        m.update(c)

    return m.hexdigest()


def write_file(filename: str, file_source: UploadFile) -> None:
    with open(filename, 'wb') as fout:
        while c := file_source.file.read(CHUNK):
            fout.write(c)
