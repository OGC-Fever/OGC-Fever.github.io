from flask import render_template, request, redirect, url_for
import sqlite3
import random


from .form import check_file, dummy_msg, resize_img
from .msg_db import post
from config import msg


def get_data(page_limit, page):
    try:
        data = post.query.order_by(post.time.desc()).limit(
            page_limit).offset((page - 1) * page_limit)
        if data.count() == 0:
            data = None
    except:
        data = None
    return data


@msg.route("/", methods=["GET", "POST"])
def message(page=1):
    if request.method == "GET":  # normal
        data = get_data(page_limit, page)
        return render_template("msg.html", data=data)
    if request.method == "POST":  # new post
        name = request.form['name']
        msg = request.form['msg']
        file = request.files["upload"]
        if name == "":
            name = random.choice(["nobody", "anonymous", "路人甲", "無名"])
        if msg == "":  # msg isn't exist
            msg = dummy_msg()
        if check_file(file.filename):  # file exist
            def pack(type):
                return sqlite3.Binary(resize_img(file, type).getbuffer())
            image = pack("image")
            timg = pack("timg")
            data = post(name=name, msg=msg, image=image, timg=timg)
            data.post()
        return redirect(url_for("message"))


@msg.route("/more", methods=["POST"])
def msg_more():
    page = int(request.form["page"])
    data = get_data(page_limit, page)
    if not data:
        return ""
    record = {"id": [], "name": [], "msg": []}
    for rec in data:
        record['id'].append(rec.id)
        record['name'].append(rec.name)
        record['msg'].append(rec.msg)
    data = {"id": record['id'],
            "name": record['name'],
            "msg": record['msg']}
    return data


page_limit = 20
