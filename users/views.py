from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from .models import Profile



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            # Create a user but don't save it to the DB just yet
            user = form.save(commit=False)

            # Ensure email is stored
            user.email = form.cleaned_data['email']
            user.save() 

            # Assign user to their chosen group, with some error handling
            role = form.cleaned_data.get('role')
            try: 
                group = Group.objects.get(name=role)
                group.user_set.add(user)
            except Group.DoesNotExist:
                messages.warning(request, f"Group '{role}' does not exist")
            
            # Log the user in straight away
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('dashboard')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
    

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile
