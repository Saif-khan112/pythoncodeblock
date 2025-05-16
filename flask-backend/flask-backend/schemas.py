from models import BubbleItem, User, Product, Stories, Video, Bubble , Settings

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class StorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stories

class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video

# class BubbleSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Bubble

class BubbleItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BubbleItem
        include_fk = True  # Include foreign keys in the serialization

class BubbleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bubble

    # Include related BubbleItems as a nested field
    items = ma.Nested(BubbleItemSchema, many=True)
    
class SettingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Settings