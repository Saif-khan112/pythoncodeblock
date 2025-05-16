# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
# from models import db, Stories, StoryType, Video
# from services.mux_service import upload_video
# from schemas import StorySchema

# stories_bp = Blueprint('stories', __name__)
# stories_schema = StorySchema()
# stories_list_schema = StorySchema(many=True)

# # Get all stories
# @stories_bp.route('/stories', methods=['GET'])
# @jwt_required()
# def get_stories():
#     stories = Stories.query.all()
#     return jsonify(stories_list_schema.dump(stories)), 200

# # Create a new story
# @stories_bp.route('/stories', methods=['POST'])
# @jwt_required()
# def create_story():
#     data = request.form  # For mixed data and file input
#     video_file = request.files.get('video_file')  # Retrieve the video file

#     # Validate required fields
#     if not data.get('title') or not data.get('type'):
#         return jsonify({"message": "Title and type are required"}), 400
#     if not video_file:
#         return jsonify({"message": "Video file is required"}), 400

#     # Step 1: Upload video to Mux
#     try:
        
#         mux_response = upload_video(video_file)
#         playback_id = mux_response.get('playback_id')
#         video_url = mux_response.get('video_url')
#     except Exception as e:
#         return jsonify({"message": "Failed to upload video to Mux", "error": str(e)}), 500

#     # Step 2: Save video details in Videos table
#     video = Video(mux_playback_id=playback_id, video_url=video_url)
#     db.session.add(video)
#     db.session.commit()

#     # Step 3: Create the story
#     story = Stories(
#         title=data['title'],
#         description=data.get('description'),
#         type=data['type'],
#         video_id=video.id  # Link the video ID
#     )

#     # Step 4: Validate and set fields based on story type
#     if story.type == 'shoppable':
#         if not isinstance(data.getlist('product_ids[]'), list) or not data.getlist('product_ids[]'):
#             return jsonify({"message": "Product IDs must be a non-empty array for shoppable stories"}), 400
#         story.product_ids = data.getlist('product_ids[]')  # Parse product IDs as a list
#     elif story.type == 'cta':
#         if not data.get('cta_text') or not data.get('cta_link'):
#             return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400
#         story.cta_text = data['cta_text']
#         story.cta_link = data['cta_link']
#     else:
#         return jsonify({"message": "Invalid story type"}), 400

#     # Step 5: Save the story
#     db.session.add(story)
#     db.session.commit()

#     return jsonify({"message": "Story created successfully", "story": story.id}), 201


# # Update a story
# @stories_bp.route('/stories/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_story(id):
#     story = Stories.query.get(id)
#     if not story:
#         return jsonify({"msg": "Story not found"}), 404
#     data = request.get_json()
#     story.title = data.get('title', story.title)
#     story.description = data.get('description', story.description)
#     db.session.commit()
#     return jsonify(stories_schema.dump(story)), 200

# # Delete a story
# @stories_bp.route('/stories/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_story(id):
#     story = Stories.query.get(id)
#     if not story:
#         return jsonify({"msg": "Story not found"}), 404
#     db.session.delete(story)
#     db.session.commit()
#     return jsonify({"msg": "Story deleted"}), 200




from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
from models import Product, db, Stories, Video
from services.mux_service import  create_upload_url, get_asset_id, get_playback_id, upload_video
from schemas import StorySchema
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.utils import secure_filename

stories_bp = Blueprint('stories', __name__)
stories_schema = StorySchema()
stories_list_schema = StorySchema(many=True)

@stories_bp.route('/stories', methods=['GET'])
@jwt_required()
def get_all_stories():
    try:
        stories = Stories.query.all()
        story_list = []
        for story in stories:
            story_data = {
                "id": story.id,
                "title": story.title,
                "description": story.description,
                "type": story.type,
                "video": {
                    "id": story.video.id,
                    "url": story.video.url,
                    "mux_playback_id": story.video.mux_playback_id,
                } if story.video else None,
                "products": [
                    {"id": product.id, "name": product.name, "price": product.price}
                    for product in story.products
                ] if story.products else []
            }
            story_list.append(story_data)
        return jsonify({"stories": story_list}), 200
    except SQLAlchemyError as db_error:
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


@stories_bp.route('/stories/<int:story_id>', methods=['GET'])
@jwt_required()
def get_story_by_id(story_id):
    try:
        story = Stories.query.get_or_404(story_id)
        story_data = {
            "id": story.id,
            "title": story.title,
            "description": story.description,
            "type": story.type,
            "video": {
                "id": story.video.id,
                "url": story.video.url,
                "mux_playback_id": story.video.mux_playback_id,
            } if story.video else None,
            "products": [
                {"id": product.id, "name": product.name, "price": product.price}
                for product in story.products
            ] if story.products else []
        }
        return jsonify({"story": story_data}), 200
    except SQLAlchemyError as db_error:
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


@stories_bp.route('/stories', methods=['POST'])
@jwt_required()
def create_story():
    try:
        # Step 1: Validate request data
        data = request.form
        video_file = request.files.get('video_file')
        if not data.get('title') or not data.get('type'):
            return jsonify({"message": "Title and type are required"}), 400
        if not video_file:
            return jsonify({"message": "Video file is required"}), 400

        # Step 2: Save video file locally
        video_url = save_video_to_server(video_file)

        # Step 3: Create video and story objects
        video = Video(url=video_url, mux_playback_id=None)
        story = Stories(
            title=data['title'],
            description=data.get('description'),
            type=data['type'],
            video=video
        )

        # Additional type-specific validations
        if story.type == 'shoppable':
            product_ids = request.form.getlist('product_ids[]')
            if not product_ids:
                return jsonify({"message": "Product IDs are required for shoppable stories"}), 400

            products = Product.query.filter(Product.id.in_(product_ids)).all()
            if len(products) != len(product_ids):
                return jsonify({"message": "Some product IDs are invalid"}), 400

            story.products = products
        elif story.type == 'cta':
            cta_text = data.get('cta_text')
            cta_link = data.get('cta_link')
            if not cta_text or not cta_link:
                return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400

            story.cta_text = cta_text
            story.cta_link = cta_link

        # Step 4: Save both objects in the same transaction
        save_to_db([video, story])

        return jsonify({"message": "Story created successfully", "story": story.id}), 201

    except SQLAlchemyError as db_error:
        db.session.rollback()
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


def save_to_db(instances):
    """
    Handles database save operations for multiple objects with proper exception handling.
    """
    try:
        if not isinstance(instances, list):
            instances = [instances]
        for instance in instances:
            db.session.add(instance)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Database save failed: {str(e)}")



# def save_video_to_server(video_file):
#     """Saves the video file to the server and returns its URL."""
#     try:
#         # Define the directory to save videos
#         upload_dir = os.path.join(current_app.root_path, 'videos')
#         os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist

#         # Save the file with a secure name
#         filename = secure_filename(video_file.filename)
#         file_path = os.path.join(upload_dir, filename)
#         video_file.save(file_path)

#         # Return the relative URL of the video
#         return f"/videos/{filename}"
#     except Exception as e:
#         raise Exception(f"Failed to save video file: {str(e)}")


def save_video_to_server(video_file):
    """Saves the video file to the parent directory of the backend folder and returns its URL."""
    try:
        # Define the directory to save videos in the parent folder
        backend_root = current_app.root_path  # Current backend folder
        parent_dir = os.path.dirname(backend_root)  # Parent directory of backend folder
        upload_dir = os.path.join(parent_dir, 'videos')  # Create 'videos' folder in the parent directory
        os.makedirs(upload_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Save the file with a secure name
        filename = secure_filename(video_file.filename)
        file_path = os.path.join(upload_dir, filename)
        video_file.save(file_path)

        # Return the relative URL of the video
        return f"/videos/{filename}"
    except Exception as e:
        raise Exception(f"Failed to save video file: {str(e)}")



# Update a story
@stories_bp.route('/stories/<int:story_id>', methods=['PUT'])
@jwt_required()
def update_story(story_id):
    try:
        story = Stories.query.get_or_404(story_id)
        data = request.json

        # Update basic story details
        story.title = data.get('title', story.title)
        story.description = data.get('description', story.description)
        story.type = data.get('type', story.type)

        # Update associated video if needed
        if data.get('video_url'):
            if not story.video:
                story.video = Video(url=data['video_url'], mux_playback_id=None)
            else:
                story.video.url = data['video_url']

        # Update associated products
        if story.type == 'shoppable' and 'product_ids' in data:
            product_ids = data['product_ids']
            products = Product.query.filter(Product.id.in_(product_ids)).all()
            if len(products) != len(product_ids):
                raise ValueError("Some product IDs are invalid")
            story.products = products

        # Update CTA details
        if story.type == 'cta':
            story.cta_text = data.get('cta_text', story.cta_text)
            story.cta_link = data.get('cta_link', story.cta_link)

        # Save changes
        save_to_db(story)
        return jsonify({"message": "Story updated successfully"}), 200
    except SQLAlchemyError as db_error:
        return jsonify({"message": "Database operation failed", "error": str(db_error)}), 500
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500


# Delete a story
@stories_bp.route('/stories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_story(id):
    story = Stories.query.get(id)
    if not story:
        return jsonify({"msg": "Story not found"}), 404
    db.session.delete(story)
    db.session.commit()
    return jsonify({"msg": "Story deleted"}), 200
