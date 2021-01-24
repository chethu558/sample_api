from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer


#regular django views
@csrf_exempt
def list_posts(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=400)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def post_details(request, pk, format=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method=='GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    if request.method=='PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()

        return JsonResponse(serializer.data)

    if request.method=='DELETE':
        post.delete()
        return HttpResponse(status=204)

@method_decorator(csrf_exempt, name='dispatch')
class PostListCreate(View):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=400)
        return JsonResponse(serializer.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostDeatail(View):
    def get_post(self, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse(status=404)

    def get(self, request, pk):
        post = self.get_post(pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        post = self.get_post(pk)
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse(serializer.data)

    def delete(self, request, pk):
        post = self.get_post(pk)
        post.delete()
        return HttpResponse(status=204)



        


#regular django views end








