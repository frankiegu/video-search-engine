from flask import request, jsonify, session

from flaskapp.shared_variables import *
from flaskapp.mysql_schema import VideoLog, SearchLog
from flaskapp.routes import routes_module
from flaskapp.routes.process import *


# Suggest videos and channels when searching
@routes_module.route("/suggest", methods=["POST"])
def search_suggestions():
    if request.method == "POST":
        input_query = request.form["input_query"]
        res = fetch_suggestion_results(input_query)
        return jsonify(res)


# Add video to user's watch later list
@routes_module.route("/add-watch-later", methods=["POST"])
def add_watch_later():
    if request.method == "POST":
        doc_id = request.form["doc_id"]
        try:
            res = add_watch_later_video(doc_id)
            res = True
            if res is True:
                return jsonify({"success": True})
        except:
            return jsonify({"success": False})


# Remove video from user's watch later list
@routes_module.route("/remove-watch-later", methods=["POST"])
def remove_watch_later():
    if request.method == "POST":
        doc_id = request.form["doc_id"]
        try:
            res = remove_watch_later_video(doc_id)
            if res is True:
                return jsonify({"success": True})
        except:
            return jsonify({"success": False})


# Store log of click when watching a video
@routes_module.route("/log/video", methods=["POST"])
def add_video_log():
    user_name = session.get("user_name") or "anon"
    if request.method == "POST":
        new_log = VideoLog(user_name,
                           request.form["clicked_video"],
                           request.form["current_video"])
        log_data = repr(new_log)
        try:
            mysql.session.add(new_log)
            mysql.session.commit()
        except Exception as e:
            return jsonify({"error": str(e)})
        else:
            return jsonify(log_data)


# Store log of click from search results
@routes_module.route("/log/search", methods=["POST"])
def add_search_log():
    user_name = session.get("user_name") or "anon"
    if request.method == "POST":
        new_log = SearchLog(user_name,
                            request.form["clicked_video"],
                            request.form["search_query"])
        log_data = repr(new_log)
        try:
            mysql.session.add(new_log)
            mysql.session.commit()
        except Exception as e:
            return jsonify({"error": str(e)})
        else:
            return jsonify(log_data)
