from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Count
from .models import Topic, Reply
from blog.models import Category

class TopicListView(ListView):
    model = Topic
    template_name = 'community/topic_list.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_queryset(self):
        queryset = Topic.objects.all()
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Stats
        context['total_topics'] = Topic.objects.count()
        context['total_replies'] = Reply.objects.count()
        return context

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'community/topic_detail.html'
    context_object_name = 'topic'
    
    def get_object(self):
        obj = super().get_object()
        # Increment views
        obj.views_count += 1
        obj.save()
        return obj

@method_decorator(login_required, name='dispatch')
class CreateTopicView(CreateView):
    model = Topic
    fields = ['title', 'content', 'category']
    template_name = 'community/topic_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Topic created successfully!")
        return super().form_valid(form)

@login_required
def create_reply(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Reply.objects.create(
                topic=topic,
                content=content,
                author=request.user
            )
            messages.success(request, "Reply posted!")
    return redirect('community:topic_detail', slug=slug)
