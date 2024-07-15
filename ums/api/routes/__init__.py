from flask import Flask, jsonify
from ums.api.routes.v1 import api_v1
from ums.api.common.http_status import HTTP_200_OK


def register_routes(app: Flask):
    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "message": "pong"}), HTTP_200_OK

    app.register_blueprint(api_v1(), url_prefix="/api/v1")
