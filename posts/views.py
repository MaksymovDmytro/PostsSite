from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import CreateView

from .forms import PostForm, CommentForm
from .models import Post


# Create your views here.

class PostList(ListView):
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
            return object_list
        else:
            return Post.objects.all()


class PostDetail(DetailView):
    template_name = 'posts/details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_liked'] = True if self.object.likes.filter(id=self.request.user.id).exists() else False
        context['likes_count'] = self.object.likes.count()
        context['form'] = CommentForm()
        return context


class PostCreate(CreateView):
    template_name = 'posts/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    template_name = 'posts/create.html'
    form_class = PostForm

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        user = self.request.user
        return get_object_or_404(Post, id=id_, author=user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdate, self).form_valid(form)


def delete_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.author == request.user:
        post.delete()
        return redirect('posts:list_view')
    else:
        raise Http404()


def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:details_view', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/create.html', {'form': form})


def like_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())
