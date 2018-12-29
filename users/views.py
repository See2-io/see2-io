from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm, ProfileForm


@login_required
def index(request):
    pass
    # user = request
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('users/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))


# @login_required
# def my_profile(request):
#     user_form = UserForm(request.GET, instance=request.user)
#     profile_form = ProfileForm(request.GET, instance=request.user.profile)
#     # return render(request, 'users/my_profile.html', {'user_form': user_form})
#     return render(request, 'users/my_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@transaction.atomic
def my_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/my_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })