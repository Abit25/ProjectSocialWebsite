from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm
from .models import Profile,Contact
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from action.utils import save_action
from action.models import Action


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    actions=Action.objects.exclude(user=request.user)
    following=request.user.following.all()
    actions=actions.filter(user__in=following)

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard','actions':actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
@login_required
def user_list(request):
    users=User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',{'users':users,"section":"people"})

@login_required
def user_detail(request,username):
    user=get_object_or_404(User,username=username)
    return render(request,'account/user/detail.html',{'user':user,"section":"people"})

@require_POST
@login_required
def follow(request):
    id=request.POST.get('id')
    action=request.POST.get('action')
    print(action+" "+id)
    if action and id:

        try:
            user=User.objects.get(id=id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                print('Working')
                save_action(user=request.user,verb=" started following ",target=user)

            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})

    return JsonResponse({'status':'ko'})
