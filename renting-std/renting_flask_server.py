# -*- coding: utf-8 -*-
# @Desc    :

from app import create_app
from app import logs

logs.logger('flask_server.log')
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
