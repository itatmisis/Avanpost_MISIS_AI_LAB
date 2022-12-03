from fastapi import FastAPI
import uvicorn
import os
from main import get_links, get_page_selenium, save_images


app = FastAPI(title="Avanpost hack - 'MISIS AI LAB' team")



@app.get("/get_images")
async def get_images(object, folder_name, galery_name):
    try:
        save_images(get_links(get_page_selenium(object)), folder_name=folder_name, galery_name=galery_name)
    except:
        return {'status': 'failed'}
    return {'status': '200'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.1", port=8000)