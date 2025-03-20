from rest_framework import serializers
from .models import Post, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author_full_name', 'content', 'created_at']
        
    def get_author_full_name(self, obj):
        full_name = obj.author.get_full_name()  # built-in method
        return full_name if full_name else (obj.author.username or "Anonymous")

class PostSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'content',
            'image',
            'author_full_name',  # using full name instead of username
            'categories',
            'comments',
            'likes_count',
            'created_at',
            'updated_at'
        ]
    
    def get_author_full_name(self, obj):
        full_name = obj.author.get_full_name()
        return full_name if full_name else (obj.author.username or "Anonymous")
    
    def get_likes_count(self, obj):
        return obj.likes.count()
