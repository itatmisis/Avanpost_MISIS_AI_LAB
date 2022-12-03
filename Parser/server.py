#! /usr/bin/env python3

from fastapi import FastAPI
import uvicorn
import os
from main import get_links, get_page_selenium, save_images
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Parser")

app = FastAPI(title="Avanpost hack - 'MISIS AI LAB' team")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/get_images")
async def get_images(object, folder_name, galery_name):
    save_dir = "/datasets/" + galery_name + "/" + folder_name
    try:
        logger.info("Processing request for \"{}\", saving to \"{}\"".format(object, save_dir))
        save_images(get_links(get_page_selenium(object)), save_dir)
    except Exception as e:
        logger.error(e)
        return {'status': 'failed'}
    return {'status': '200'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)