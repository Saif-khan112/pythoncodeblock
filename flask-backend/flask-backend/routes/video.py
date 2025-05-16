from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Video
from schemas import VideoSchema

video_bp = Blueprint('video', __name__)
video_schema = VideoSchema()
video_list_schema = VideoSchema(many=True)

# Get all videos
@video_bp.route('/videos', methods=['GET'])
@jwt_required()
def get_videos():
    videos = Video.query.all()
    return jsonify(video_list_schema.dump(videos)), 200

# Create a new video
@video_bp.route('/videos', methods=['POST'])
@jwt_required()
def create_video():
    data = request.get_json()
    video = Video(**data)
    db.session.add(video)
    db.session.commit()
    return jsonify(video_schema.dump(video)), 201

# Delete a video
@video_bp.route('/videos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_video(id):
    video = Video.query.get(id)
    if not video:
        return jsonify({"msg": "Video not found"}), 404
    db.session.delete(video)
    db.session.commit()
    return jsonify({"msg": "Video deleted"}), 200
