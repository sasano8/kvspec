import os

from fastapi import FastAPI, Request, Header, Response
from fastapi.responses import FileResponse
from urllib.parse import quote
import os


app = FastAPI()


@app.get("/files/{file_path:path}")
def get_file(
    request: Request,
    file_path: str,
    # loader: dict = {"type": "csv_to_dict", "header": True},
    # dumper: dict = {"content-type": "application/jsonlines"}
    accept: str = Header("application/octet-stream"),
):
    full_url_str = str(request.url)
    url = f"relfile://{file_path}"
    # return {"url": url, "loader": loader, "dumper": dumper}
    # {"url": full_url_str}

    headers = {"content-type": "application/octet-stream"}
    file_name = os.path.basename(file_path)
    file_name_encoded = quote(file_name)
    headers["Content-Disposition"] = f"attachment; filename={file_name_encoded}"
    return Response(b"abc", media_type=accept, headers=headers)


@app.get("/tables/{table_path:path}")
def get_table(
    request: Request,
    table_path: str,
    # loader: dict = {"type": "csv_to_dict", "header": True},
    # dumper: dict = {"content-type": "application/jsonlines"}
):
    parts = table_path.split("/")
    if len(parts) != 2:
        raise Exception({"error": "invalid table path"})

    full_url_str = str(request.url)
    return {"url": full_url_str}
