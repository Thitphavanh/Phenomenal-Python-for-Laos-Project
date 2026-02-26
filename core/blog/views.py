from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Post, Category, Tag, Comment, PostVote
from .forms import PostForm, CommentForm, CustomUserCreationForm, CustomAuthenticationForm
from courses.models import Course
from events.models import Event
from community.models import Topic
from docs.models import Documentation

def index(request):
    """Landing Page - Home Feed"""
    # Fetch recent posts (excluding docs if needed, or all)
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    # Fetch Courses (3 latest published)
    courses = Course.objects.filter(status='published').order_by('-created_at')[:3]

    # Fetch Events (3 upcoming published)
    upcoming_events = Event.objects.filter(
        status='published', 
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')[:3]

    # Fetch Community Topics (5 recent)
    recent_topics = Topic.objects.all().order_by('-created_at')[:5]

    # Fetch Docs (5 recent published)
    recent_docs = Documentation.objects.filter(status='published').order_by('-updated_at')[:5]
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'courses': courses,
        'upcoming_events': upcoming_events,
        'recent_topics': recent_topics,
        'recent_docs': recent_docs,
    }
    
    return render(request, 'index.html', context)

def post_list(request):
    """
    Unified Community Feed
    - Filter by 'type': 'blog' (Articles) or 'post' (Discussions)
    - Default: All types
    """
    filter_type = request.GET.get('type')
    
    # Base Query
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    # Apply Filter
    if filter_type == 'blog':
        posts = posts.filter(post_type='blog')
    elif filter_type == 'post':
        posts = posts.filter(post_type='post')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'filter_type': filter_type, # Pass to template for active tab state
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', slug=slug)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    

    return render(request, 'blog/blog_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)


# Voting Views
@require_POST
def vote_post(request, post_id):
    """Handle post voting (Reddit-style)"""
    post = get_object_or_404(Post, id=post_id)
    vote_type = int(request.POST.get('vote_type', 0))

    if vote_type not in [1, -1]:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)

    # Get or create session key for anonymous users
    if not request.session.session_key:
        request.session.create()

    user = request.user if request.user.is_authenticated else None
    session_key = None if user else request.session.session_key

    # Check if user/session already voted
    existing_vote = PostVote.objects.filter(
        post=post,
        user=user if user else None,
        session_key=session_key if session_key else None
    ).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if clicking same button
            existing_vote.delete()
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        # Create new vote
        PostVote.objects.create(
            post=post,
            user=user,
            session_key=session_key,
            vote_type=vote_type
        )

    return JsonResponse({
        'score': post.get_vote_score(),
        'upvotes': post.get_upvotes(),
        'downvotes': post.get_downvotes(),
    })


# Authentication Views
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('blog:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'ຍິນດີຕ້ອນຮັບ {user.username}! ລົງທະບຽນສຳເລັດ.')

            # Redirect to next or index
            next_url = request.GET.get('next', 'blog:index')
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('blog:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'ຍິນດີຕ້ອນຮັບກັບຄືນ {username}!')

                # Redirect to next or index
                next_url = request.GET.get('next', 'blog:index')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'ທ່ານໄດ້ອອກຈາກລະບົບສຳເລັດແລ້ວ.')
    return redirect('blog:index')
