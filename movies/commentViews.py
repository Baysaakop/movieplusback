# from django.http import Http404
# from django.db.models import Q, Count
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from .models import Comment, Review, Movie
# from .serializers import CommentSerializer
# from rest_framework import viewsets

# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()

#     def get_queryset(self):
#         queryset = Comment.objects.all().order_by('-created_at')
#         movie = self.request.query_params.get('movie', None)
#         review = self.request.query_params.get('review', None)
#         if movie is not None:
#             movie_obj = Movie.objects.get(id=movie)
#             queryset = movie_obj.comments.all().annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')
#         if review is not None:
#             review_obj = Review.objects.get(id=review)
#             queryset = review_obj.comments.all().annotate(likes_count=Count('likes')).order_by('-likes_count', '-created_at')
#         return queryset


#     def create(self, request, *args, **kwargs):
#         user = Token.objects.get(key=request.data['token']).user
#         text = request.data['comment']
#         comment = Comment.objects.create(
#             user=user,
#             comment=text
#         )
#         if 'movie' in request.data:
#             movie = Movie.objects.get(id=int(request.data['movie']))
#             movie.comments.add(comment)
#             movie.save()
#             score_obj = movie.scores.filter(user=user).first()
#             if score_obj is not None:
#                 comment.score = score_obj.score
#         if 'review' in request.data:
#             review = Review.objects.get(id=int(request.data['review']))
#             review.comments.add(comment)
#             review.save()
#         comment.save()
#         serializer = CommentSerializer(comment)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         comment = self.get_object()
#         user = Token.objects.get(key=request.data['token']).user
#         if 'comment' in request.data:
#             comment.comment = request.data['comment']
#         if 'like' in request.data:
#             if user in comment.likes.all():
#                 comment.likes.remove(user)
#             else:
#                 comment.likes.add(user)
#         if 'dislike' in request.data:
#             if user in comment.dislikes.all():
#                 comment.dislikes.remove(user)
#             else:
#                 comment.dislikes.add(user)
#         comment.save()
#         serializer = CommentSerializer(comment)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
