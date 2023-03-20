from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, ContactForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView
from my_site import forms
from django.db.models import Q, Count
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'my_site/post/list.html',
                  {'posts': posts,
                   'tag': tag})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tag_ids = post.tag.values_list('id', flat=True)
    similar_posts = Post.published.filter(tag__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tag=Count('tag')).order_by('-same_tag', '-publish')[:4]
    return render(request,
                  'my_site/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@admin.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,
                  'my_site/post/share.html',
                  {"post": post,
                   'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'my_site/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def search(request):
    query = request.GET.get('q', '')
    keyword_results = results = []
    if query:
        keyword_results = Post.objects.filter(searchkeyword__keyword__in=query.split()).distinct()
        if keyword_results.count() == 1:
            return HttpResponseRedirect(keyword_results[0].get_absolute_url())
        results = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    return render(request, 'my_site/search.html',
                  {'query': query,
                   'keyword_results': keyword_results,
                   'results': results})


class ContactView(FormView):
    template_name = "my_site/post/contact.html"
    form_class = forms.ContactForm
    success_url = "/ajax/contact"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
