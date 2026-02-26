from django.shortcuts import render, get_object_or_404
from .models import Documentation, DocCategory


def doc_list(request):
    """Documentation Index - Using Documentation model"""
    docs = Documentation.objects.filter(
        status='published',
        is_published=True
    ).order_by('chapter_number', 'section_number', 'created_at')
    return render(request, 'docs/doc_list.html', {'docs': docs})


def category_docs(request, slug):
    """Documentation by Category"""
    category = get_object_or_404(DocCategory, slug=slug, is_active=True)
    docs = Documentation.objects.filter(
        category=category,
        status='published',
        is_published=True
    ).order_by('chapter_number', 'section_number', 'created_at')
    return render(request, 'docs/category_docs.html', {
        'category': category,
        'docs': docs
    })


def doc_detail(request, slug):
    """Documentation Detail - Using Documentation model"""
    post = get_object_or_404(
        Documentation,
        slug=slug,
        status='published',
        is_published=True
    )
    all_docs = Documentation.objects.filter(
        status='published',
        is_published=True
    ).order_by('chapter_number', 'section_number', 'created_at')

    # Calculate Previous and Next
    docs_list = list(all_docs)
    current_index = -1
    for i, doc in enumerate(docs_list):
        if doc.slug == slug:
            current_index = i
            break

    prev_doc = docs_list[current_index - 1] if current_index > 0 else None
    next_doc = docs_list[current_index + 1] if current_index < len(docs_list) - 1 else None

    return render(request, 'docs/doc_detail.html', {
        'post': post,
        'all_docs': all_docs,
        'prev_doc': prev_doc,
        'next_doc': next_doc,
    })
