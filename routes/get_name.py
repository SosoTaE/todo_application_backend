from flask import jsonify


def get_name(config):
    return jsonify({"name":config.ADMIN_USERNAME}), 200