from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Item, Post

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'created_by', 'updated_by', 'created_at', 'updated_at')        

class PostSerializer(serializers.ModelSerializer):       
    token = serializers.CharField(write_only=True)        
    thumbnail = serializers.ImageField(required=False, use_url=True)            
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'thumbnail', 'created_at', 'created_by', 'token'            
        ) 

    def create(self, validated_data):                   
        user = Token.objects.get(key=validated_data['token']).user                
        post = Post(
            title=validated_data['title'],
            content=validated_data['content'],
            thumbnail=validated_data['thumbnail'],
            created_by=user 
        )
        post.save()
        return post

    def update(self, instance, validated_data):                
        user = Token.objects.get(key=validated_data['token']).user   
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.updated_by = user        
        instance.save()
        return instance