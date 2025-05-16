from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import BubbleItem, db, Bubble
from schemas import BubbleSchema
from sqlalchemy.exc import SQLAlchemyError

bubbles_bp = Blueprint('bubbles', __name__)
bubble_schema = BubbleSchema()
bubble_list_schema = BubbleSchema(many=True)

# Get all bubbles
# @bubbles_bp.route('/bubbles', methods=['GET'])
# @jwt_required()
# def get_bubbles():
#     bubbles = Bubble.query.all()
#     return jsonify(bubble_list_schema.dump(bubbles)), 200

# Create a new bubble
# @bubbles_bp.route('/bubbles', methods=['POST'])
# @jwt_required()
# def create_bubble():
#     data = request.get_json()
#     bubble = Bubble(**data)
#     db.session.add(bubble)
#     db.session.commit()
#     return jsonify(bubble_schema.dump(bubble)), 201
# @bubbles_bp.route('/bubbles', methods=['POST'])
# @jwt_required()
# def create_bubble():
#     data = request.json
#     title = data.get('title')
#     size = data.get('size')
#     items = data.get('items')  # List of story IDs with order [{ "story_id": 1, "order": 1 }, ...]

#     if not title:
#         return jsonify({"error": "Title is required"}), 400

#     bubble = Bubble(title=title, size=size)
#     db.session.add(bubble)
#     db.session.flush()

#     for item in items:
#         bubble_item = BubbleItem(
#             bubble_id=bubble.id,
#             story_id=item.get('story_id'),
#             order=item.get('order')
#         )
#         db.session.add(bubble_item)

#     db.session.commit()
#     return jsonify({"id": bubble.id, "message": "Bubble created successfully"}), 201



@bubbles_bp.route('/bubbles', methods=['POST'])
@jwt_required()
def create_bubble():
    try:
        data = request.json

        # Step 1: Create the bubble
        bubble = Bubble(title=data['title'], size=data.get('size'))
        db.session.add(bubble)

        # Step 2: Create associated bubble items
        for item_data in data.get('items', []):
            story_id = item_data.get('story_id', None)
            item = BubbleItem(
                order=item_data['order'],
                story_id=story_id,
                bubble=bubble
            )
            db.session.add(item)

        # Step 3: Commit changes to the database
        db.session.commit()
        return jsonify({"message": "Bubble created successfully", "bubble_id": bubble.id}), 201
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


# @bubbles_bp.route('/bubbles/<int:bubble_id>', methods=['PUT'])
# def update_bubble(bubble_id):
#     data = request.json
#     bubble = Bubble.query.get_or_404(bubble_id)

#     bubble.title = data.get('title', bubble.title)
#     bubble.size = data.get('size', bubble.size)

#     items = data.get('items')  # Updated items
#     if items:
#         BubbleItem.query.filter_by(bubble_id=bubble_id).delete()
#         for item in items:
#             bubble_item = BubbleItem(
#                 bubble_id=bubble.id,
#                 story_id=item.get('story_id'),
#                 order=item.get('order')
#             )
#             db.session.add(bubble_item)

#     db.session.commit()
#     return jsonify({"message": "Bubble updated successfully"}), 200


# @bubbles_bp.route('/bubbles', methods=['GET'])
# def get_all_bubbles():
#     bubbles = Bubble.query.all()
#     result = []
#     for bubble in bubbles:
#         result.append({
#             "id": bubble.id,
#             "title": bubble.title,
#             "size": bubble.size,
#             "items": [
#                 {
#                     "story_id": item.story_id,
#                     "order": item.order
#                 } for item in bubble.items
#             ],
#             "created_at": bubble.created_at,
#             "updated_at": bubble.updated_at
#         })
#     return jsonify(result), 200

@bubbles_bp.route('/bubbles', methods=['GET'])
@jwt_required()
def get_all_bubbles():
    try:
        bubbles = Bubble.query.all()
        bubble_list = []

        for bubble in bubbles:
            bubble_data = {
                "id": bubble.id,
                "title": bubble.title,
                "size": bubble.size,
                "created_at": bubble.created_at,
                "updated_at": bubble.updated_at,
                "items": []
            }

            for item in bubble.items:
                item_data = {
                    "id": item.id,
                    "order": item.order,
                    "story": {
                        "id": item.story.id if item.story else None,
                        "title": item.story.title if item.story else None,
                        "video_url": item.story.video.url if item.story and item.story.video else None,
                        "description": item.story.description if item.story else None
                    } if item.story else None
                }
                bubble_data["items"].append(item_data)
            
            bubble_list.append(bubble_data)

        return jsonify({"bubbles": bubble_list}), 200
    except SQLAlchemyError as db_error:
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500



@bubbles_bp.route('/bubbles/<int:bubble_id>', methods=['GET'])
@jwt_required()
def get_bubble_by_id(bubble_id):
    try:
        bubble = Bubble.query.get_or_404(bubble_id)
        bubble_data = {
            "id": bubble.id,
            "title": bubble.title,
            "size": bubble.size,
            "created_at": bubble.created_at,
            "updated_at": bubble.updated_at,
            "items": []
        }

        for item in bubble.items:
            item_data = {
                "id": item.id,
                "order": item.order,
                "story": {
                    "id": item.story.id if item.story else None,
                    "title": item.story.title if item.story else None,
                    "video_url": item.story.video.url if item.story and item.story.video else None,
                    "description": item.story.description if item.story else None
                } if item.story else None
            }
            bubble_data["items"].append(item_data)

        return jsonify({"bubble": bubble_data}), 200
    except SQLAlchemyError as db_error:
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


# @bubbles_bp.route('/bubbles/<int:bubble_id>', methods=['GET'])
# def get_bubble_by_id(bubble_id):
#     bubble = Bubble.query.get_or_404(bubble_id)
#     result = {
#         "id": bubble.id,
#         "title": bubble.title,
#         "size": bubble.size,
#         "items": [
#             {
#                 "story_id": item.story_id,
#                 "order": item.order
#             } for item in bubble.items
#         ],
#         "created_at": bubble.created_at,
#         "updated_at": bubble.updated_at
#     }
#     return jsonify(result), 200


@bubbles_bp.route('/bubbles/<int:bubble_id>', methods=['PUT'])
@jwt_required()
def update_bubble(bubble_id):
    try:
        bubble = Bubble.query.get_or_404(bubble_id)
        data = request.json

        # Step 1: Update bubble details
        bubble.title = data.get('title', bubble.title)
        bubble.size = data.get('size', bubble.size)

        # Step 2: Update associated bubble items
        if 'items' in data:
            # Remove existing items
            for item in bubble.items:
                db.session.delete(item)
            
            # Add new items
            for item_data in data['items']:
                story_id = item_data.get('story_id', None)
                item = BubbleItem(
                    order=item_data['order'],
                    story_id=story_id,
                    bubble=bubble
                )
                db.session.add(item)

        # Step 3: Commit changes
        db.session.commit()
        return jsonify({"message": "Bubble updated successfully"}), 200
    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500
