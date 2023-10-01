from django.core.mail import send_mail
from typing import Any, Dict
from django.core.mail import EmailMessage, get_connection
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post
from .forms import CommentForm
from django.shortcuts import render,redirect
from .forms import DetailForm
from django import forms



# Create your views here.
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data


def GalleryPageView(request):
    return render(request, "blog/gallery.html")


   

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"



class SinglePostsView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later
    
    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        stored_posts = request.session.get("stored_posts")
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)

        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args = [slug]))
        
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {

        }
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in = stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")



    # def information(request):
    #     if request.method == 'POST':
    #         form = InformaionForm(request.POST)
            
    #         if form.is_valid():
    #          print(froms.cleaned_data)
    #          return HttpResponseRedirect("/thank-you")
    #     else:
    #         forms = InformationForm()
            
    #     return render(request, "blog/index.html", {
    #       "forms": form 
    #     })
  
     

class DetailFormView(DetailView):
    template_name = "blog/post-details.html"
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all(())
        context["detail_form"] = DetailForm()
        return context


def indexview(request):
    if request.method == 'POST':
        
        form = DetailForm(request.POST)
        
        if form.is_valid():
            
            name = form.cleaned_data['שם']
            number = form.cleaned_data['טלפון']
            email = form.cleaned_data['מייל']
            subject = form.cleaned_data['נושא']
            content = form.cleaned_data['תוכן']
            
            html = render_to_string('blog/emails/contactform.html',{
                
                'name': name,
                'number': number,
                'email': email,
                'subject': subject,
                'content': content
                
                
            })
            
            send_mail(
            "Subject here",
            "Here is the message.",
            "fitness.oryehuda@gmail.com",
            ["moranfriedman92@gmail.com"],
            html_message=html,
            fail_silently=False,)
            
            return redirect('indexview-page')
            
        else: 
            
            print('form not valid')
            return redirect('indexview-page')
    else:
        
        form = DetailForm()
            
            
    return render(request,'blog/index2.html',{
        
        'form': form
        
    })
   