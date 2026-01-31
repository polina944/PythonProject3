from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from board.models import User, Post, Comment
from board.forms import PostForm, CommentForm
from board.filters import CommentFilter


def home(request):
    return render(request, 'board/home.html')


def activate_user(request):
    if 'code' in request.POST:
        code = request.POST['code']
        user = User.objects.filter(code=code)
        if user.exists():
            user.update(is_active=True)
            return redirect('account_login')
    return render(request, 'account/invalid_code.html')


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'board/post_list.html'
    ordering = ['-created_at']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'board/post_detail.html'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = self.request.user
            comment.save()
            send_mail(
                subject='Новый отклик на ваше объявление',
                message=f'Привет, {post.user.username}! На ваше объявление был оставлен отклик!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post.user.email],
            )
        return redirect('board_detail', pk=post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'board/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'board/post_edit.html'
    form_class = PostForm
    success_url = '/board/'


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'board/user_comments.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(post__user=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset, user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def comment_accept(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.status = True
    comment.save()
    send_mail(
        subject='Принятие отклика!',
        message=f'Привет, {comment.user.username}! Ваш отклик на объявление {comment.post.title} '
                f'был принят автором объявления!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[comment.user.email],
    )
    return redirect(request.META['HTTP_REFERER'])


def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])




