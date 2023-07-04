from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, PostForm, PasswordChangeForm
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User, Board, Post
from urllib.parse import quote
from django.contrib.auth.views import LoginView
import uuid
import os


port = os.environ.get("PORT")


# Create your views here.
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.user.login_count += 1
        self.request.user.save()
        return response


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('email'):
                user.is_active = False
                user.save()
                mail_subject = '電子信箱確認信'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': f"{request.get_host()}:{port}",
                    'uid': quote(urlsafe_base64_encode(force_bytes(user.pk))),
                    'token': quote(account_activation_token.make_token(user)),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.content_subtype = 'html'
                email.send()
                return HttpResponse('請至電子信箱收信驗證以完成您的註冊手續。<br />您可以放心關閉此頁面。<br />如果您在五分鐘後仍未收到信件，請與開發者聯繫。')
            else:
                user.is_active = True
                user.save()
                return HttpResponse(f'註冊成功！你現在可以登入了！<br /><a href=http://{request.get_host()}:{port}>現在就登入！</a>')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(f'驗證成功！你現在可以登入了！<br /><a href=http://{request.get_host()}:{port}>現在就登入！</a>')
    else:
        return HttpResponse('驗證無效！請與開發者聯繫回報以完成註冊。')


@login_required
def index(request):
    boards = Board.objects.all()
    return render(request, 'index.html', {'boards': boards})


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.user.username
        user = User.objects.get(username=username)
        user.nickname = request.POST.get('nickname')
        if user.email and request.POST.get('email') and user.email != request.POST.get('email'):
            user.email = request.POST.get('email')
            user.is_active = False
            user.save()
            mail_subject = '電子信箱確認信'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': f"{request.get_host()}:{port}",
                'uid': quote(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': quote(account_activation_token.make_token(user)),
            })
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = 'html'
            email.send()
            return HttpResponse('請至電子信箱收信驗證。<br />您可以放心關閉此頁面。<br />如果您在五分鐘後仍未收到信件，請與開發者聯繫。')
        else:
            user.save()
            return HttpResponseRedirect(f"?username={ username }")
    else:
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
            return render(request, 'profile.html', {'user': user})
        except User.DoesNotExist:
            error_message = f'錯誤。帳號「{username}」並不存在。'
            return render(request, 'profile.html', {'error_message': error_message})


@login_required
def board(request):
    board_name = request.GET.get('board')
    board = Board.objects.get(name=board_name)
    posts = Post.objects.filter(board=board)
    is_moderator = board.moderators.filter(id=request.user.id).exists()

    return render(request, 'board.html', {'posts': posts, 'is_moderator': is_moderator})


@login_required
def post(request):
    id = request.GET.get('post')
    post = Post.objects.get(id=id)

    return render(request, 'post.html', {'post': post})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.image:
                post.image.name = f"{uuid.uuid4().hex}"
            post.save()
            request.user.post_count += 1
            request.user.save()
            return HttpResponseRedirect(f"/board/?board={ post.board }")
    else:
        form = PostForm()
    boards = Board.objects.all()
    return render(request, 'create_post.html', {'form': form, 'boards': boards})


@login_required
def delete_post(request):
    id = request.GET.get('post')
    post = Post.objects.get(id=id)
    board = post.board
    if request.method == 'POST':
        if post.board.moderators.filter(id=request.user.id).exists():
            post.author.post_count -= 1
            post.author.save()
            post.delete()
            return HttpResponseRedirect(f"/board/?board={ board }")
        else:
            return HttpResponse(f"你並沒有權限進行此操作。<br /><a href=http://{request.get_host()}:{port}>回首頁</a>")
    else:
        return render(request, 'delete_confirmation.html', {'post': post})
