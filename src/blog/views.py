from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# Create your views here.

# This is a function based view. It is totally created by the developer
def blog_view(request):
    context = {'posts' : Post.objects.all()}
    return render(request, 'blog/blog.html', context)

# This is a class based view that comes prepackaged with Django and requires much less set up. however, the variable naming conventions are needed to properly execute loops and such in the html file
class PostListView(ListView): #Blog Home Page
    model = Post
    #This next line changes the default template to our current template from {app/model_viewtype.html}
    template_name = 'blog/blog.html'
    #This next line changes the default class based list view variable from "object_list" to our previous function based list view variable "posts". This variable is in the for loop in the blog.html file
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView): #Blog page for a specific user
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    # This next function filters the page to a specific user. I will modify this for drugs 
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # This next line redirects the page to the blog home page. Right now it doesn't work because the url will not reset
    success_url = '/blog'
    # This function automaticlly assigns the loged in user to the author of the new post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # This next line redirects the page to the blog home page. Right now it doesn't work because the url will not reset
    success_url = '/blog'
    # This function automaticlly assigns the loged in user to the author of the new post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # If using the UserPassesTestMixin class you need to create the following function to test 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            # messages.error(request, f"Your cannot update someone else's post")
            # return redirect('blog')
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False