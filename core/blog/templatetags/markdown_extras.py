"""
Template filters for markdown rendering
"""
from django import template
from django.utils.safestring import mark_safe
import markdown2

register = template.Library()


@register.filter(name='markdown')
def markdown_filter(text):
    """
    Convert markdown text to HTML with syntax highlighting
    """
    if not text:
        return ''

    # Configure markdown2 with extras
    extras = {
        'fenced-code-blocks': None,  # Support for ```code blocks```
        'code-friendly': None,       # Disable _ and __ for em and strong
        'cuddled-lists': None,       # Allow lists to be cuddled to the preceding paragraph
        'tables': None,              # Support for tables
        'header-ids': None,          # Add id attributes to headers
        'toc': None,                 # Generate table of contents
        'strike': None,              # Support for ~~strikethrough~~
        'highlightjs-lang': None,    # Add language class to code blocks
    }

    html = markdown2.markdown(text, extras=extras)
    return mark_safe(html)


@register.filter(name='markdown_safe')
def markdown_safe_filter(text):
    """
    Convert markdown text to HTML (alias for markdown filter)
    """
    return markdown_filter(text)
