# -*- coding: utf-8 -*-


import random

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from app.config import FDC_API_UPLOAD_URL
from app.models.std_case import *

logger = logging.getLogger(__name__)


def upload(file_paths):
    files = file_paths.split(';')
    for file in files:
        with open(file, 'rb') as f:
            name = f.name[f.name.rfind('\\') + 1:]
            multipart_encoder = MultipartEncoder(
                fields={
                    'file': (name, f, 'application/vnd.ms-excel')
                },
                boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
            )
            headers = {'Content-Type': multipart_encoder.content_type}
            try:
                r = requests.post(url=FDC_API_UPLOAD_URL + '?cityId={}&taskName={}'.format(1, name),
                                  headers=headers, data=multipart_encoder)
            except Exception as e:
                msg = traceback.format_exc() + ', 案例自动入库，上传文件失败, 文件: {}'.format(file)
                raise Exception(msg)
            logger.info('案例自动入库，上传文件: {}, 调用结果 -> code: {}, content: {}'
                        .format(file, r.status_code, str(r.content, encoding='utf-8')))
