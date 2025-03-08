"""Server"""

__version__ = "0.1.0"
import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

import backend.login
import backend.register
import backend.get_blog
import backend.get_cfp
import backend.select_cfp
import backend.cfp.receive_customer
import backend.cfp.customer
import backend.cfp.customer.asset
import backend.cfp.customer.liability
import backend.cfp.customer.income
import backend.cfp.customer.expense
import backend.cfp.customer.goal
import backend.cfp.customer.save
import backend.cfp.upload_blog
import backend.admin.receive_customer
import backend.admin.cfp_list
import backend.admin.cfp.receive_customer
import backend.admin.getall_blog
import backend.admin.blog_approval

if __name__ == '__main__':
    app.run()
