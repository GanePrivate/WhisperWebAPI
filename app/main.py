from typing import Union
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import response as res
import time
from starlette.middleware.cors import CORSMiddleware
import whisper
from util.text_summarization import Summarizer
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
# import torch


# モデルのロード
models = {
    "tiny": whisper.load_model("tiny"),
    "base": whisper.load_model("base"),
    "small": whisper.load_model("small"),
    "medium": whisper.load_model("medium"),
    "large": whisper.load_model("large")
}

app = FastAPI()

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


@app.post("/upload/",
          response_description="uploaded",
          response_model=res.UploadResponseModel,
          responses={
              200: {"model": res.UploadResponseModel},
              400: {"model": res.UploadErrorResponseModel}
          },
          tags=["FileController"])
def receive_file(
    file: UploadFile = File(description="Audio File"),
    model_name: Union[str, None] = Form(default="small", description="使用するモデル名(tiny, base, small, medium, largeのどれか)<br>※未指定の場合はsmall"),
):

    start = time.time()

    # GPUが使えるかどうかの確認
    # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    # print(DEVICE)

    # 受け取ったファイルを一時ファイルとして保存
    tmp_path = save_upload_file_tmp(file)
    try:
        model = models[model_name]
        result = model.transcribe(str(tmp_path))
    except:
        raise HTTPException(detail=f"文字起こし処理に失敗しました", status_code=status.HTTP_400_BAD_REQUEST)
    finally:
        tmp_path.unlink()  # 一時ファイルを削除する

    # dictからリストのキーの値のみ取得
    result = {k: result[k] for k in ['text']}

    # 文章の要約を生成
    # result['summary'] = Summarizer(result["text"]).get_summary_text()
    print(result)
    print(f'TIME = {time.time() - start} sec')
    return JSONResponse(content=jsonable_encoder(result))