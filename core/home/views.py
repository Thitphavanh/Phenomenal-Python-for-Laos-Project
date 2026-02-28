from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone

from blog.models import Post
from courses.models import Course
from events.models import Event
from community.models import Topic
from docs.models import Documentation
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json as _json
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import JsonResponse



# Create your views here.
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


# Authentication Views
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify the backend since multiple auth backends (e.g. allauth) are configured
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'ຍິນດີຕ້ອນຮັບ {user.username}! ລົງທະບຽນສຳເລັດ.')

            # Redirect to next or index
            next_url = request.GET.get('next', 'home:index')
            return redirect(next_url)
    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home:index')

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
                next_url = request.GET.get('next', 'home:index')
                return redirect(next_url)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'ທ່ານໄດ້ອອກຈາກລະບົບສຳເລັດແລ້ວ.')
    return redirect('home:login')



@csrf_exempt
@require_POST
def line_auth_view(request):
    """Authenticate Django session after LINE LIFF login"""
    try:
        data = _json.loads(request.body)
        line_user_id = data.get('userId', '').strip()
        display_name = data.get('displayName', '').strip()
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    if not line_user_id:
        return JsonResponse({'success': False, 'error': 'userId is required'}, status=400)

    username = f'line_{line_user_id}'
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'first_name': display_name[:30] if display_name else ''}
    )

    # Update displayName if it changed on LINE
    if not created and display_name and user.first_name != display_name[:30]:
        user.first_name = display_name[:30]
        user.save(update_fields=['first_name'])

    # Logout any existing session (e.g. admin2) before logging in as LINE user
    if request.user.is_authenticated and request.user != user:
        logout(request)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return JsonResponse({'success': True})
