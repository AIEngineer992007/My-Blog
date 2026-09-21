from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, ContactMessage, Comment
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm, CommentForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

# Create your views here.
def home(request):
    posts = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', posts)

def about(request):
    context = {
            'posts': Post.objects.all(),
        }
    return render(request, 'blog/about.html', context)

def latest_posts(request):
    posts = {
            'posts': Post.objects.order_by('-date_posted')[:5],
        }
    return render(request, 'blog/latest_post.html', posts)

def oldest_posts(request):
    posts = {
            'posts': Post.objects.all()[:5],
        }
    return render(request, 'blog/oldest_post.html', posts)

def contact(request):
    return render(request, 'blog/contact.html')

@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your feedback is sent!")
            return redirect('/')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.disliked_by.filter(id=request.user.id).exists():
        post.disliked_by.remove(request.user)
        post.liked_by.add(request.user)
        
    elif post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('posts-detail', pk)

@login_required
def post_disliked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.disliked_by.filter(id=request.user.id).exists():
        post.disliked_by.remove(request.user)
        
    elif post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
        post.disliked_by.add(request.user)
        
    else:
        post.disliked_by.add(request.user)
    return redirect('posts-detail', pk)
    
@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        return JsonResponse({
            'success': False,
            'error': "Comment is not yours",
        }, status=403)
    
    post = comment.post
    comment.delete()
    
    return JsonResponse({
        'success': True,
        'comment_count': post.comments.count(),
    })

def intro(request):
    return render(request, 'blog/introduction.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostDetailView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context
    
class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not request.user.is_authenticated:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Login needed!'})
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.object
            new_comment.author = request.user
            new_comment.save()
            
            if is_ajax:
                comment_html = render_to_string('blog/comment_item.html', {'comment': new_comment}, request=request)
                return JsonResponse({
                    'success': True,
                    'comment_html': comment_html,
                    'comment_count': self.object.comments.count(),
                })
            return redirect('posts-detail', pk=self.object.pk)
        
        if is_ajax:
            return JsonResponse({
                'success': False,
                'error': 'What did you write?'
            }, status=400)
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
