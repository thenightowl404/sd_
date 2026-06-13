from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Notification
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return redirect('notifications')

@login_required
def notifications(request):
    filter_type = request.GET.get("filter", "all")

    noti = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if filter_type == "unread":
        noti = noti.filter(read=False)

    elif filter_type == "system":
        noti = noti.filter(type="system")

    elif filter_type == "course":
        noti = noti.filter(type="course")

    return render(
        request,
        "Notification.html",
        {
            "notifications": noti,
            "current_filter": filter_type   # 👈 HERE
        }
    )

def create_notification(user, text, icon="🔔", type="system"):
    Notification.objects.create(
        user=user,
        text=text,
        icon=icon,
        type=type
    )
@login_required
def mark_notification_read(request, id):
    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')

@login_required
def security(request):
    msg = ""

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(current_password):
            msg = "❌ Current password is wrong"

        elif new_password != confirm_password:
            msg = "❌ New passwords do not match"

        elif len(new_password) < 6:
            msg = "❌ Password must be at least 6 characters"

        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            create_notification(
                user,
                "Your password was changed successfully 🔐",
                "🔐",
                "system"
            )

            msg = "✅ Password updated successfully"

    return render(request, "security.html", {"msg": msg})

@login_required
def profile(request):

    if request.method == "POST":
        request.user.username = request.POST['username']
        request.user.email = request.POST['email']
        request.user.save()

        # 🔥 AUTO NOTIFICATION
        create_notification(
            request.user,
            "Your profile was updated successfully ✏️",
            "👤",
            "system"
        )

        return redirect('profile')

    return render(request, 'profile.html')
def ind(request):
    return render(request, 'index.html')
    
def home(request):
    return render(request, 'HoMe.html')

def more(request):
    return render(request, 'More.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'Image.html', {
                'error': 'Username already exists',
                'mode': 'register'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        create_notification(
            user,
            "Welcome to SkillOrbit 🎉 Your account has been created!",
            "🎉",
            "system"
        )

        return redirect('/login/')

    return render(request, 'Image.html', {'mode': 'register'})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 AUTO LOGIN NOTIFICATION
            create_notification(
                user,
                "You just logged in to SkillOrbit 🔐",
                "🔐",
                "system"
            )

            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'Image.html', {'mode': 'login'})

def user_logout(request):
    logout(request)
    return redirect('login')