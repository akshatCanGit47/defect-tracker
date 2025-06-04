# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProjectForm, DefectForm, ProfileForm
from .models import Project, Defect, User, UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'core/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            project.members.add(request.user)
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user not in project.members.all():
        return redirect('project_list')
    
    defects = Defect.objects.filter(project=project)
    return render(request, 'core/project_detail.html', {
        'project': project,
        'defects': defects
    })

@login_required
def create_defect(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = DefectForm(request.POST)
        if form.is_valid():
            defect = form.save(commit=False)
            defect.project = project
            defect.created_by = request.user
            defect.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = DefectForm()
    return render(request, 'core/create_defect.html', {'form': form, 'project': project})

@login_required
def add_member(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.user != project.creator:
        return redirect('project_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            project.members.add(user)
        return redirect('project_detail', pk=project.pk)
    
    return render(request, 'core/add_member.html', {'project': project})


@login_required
def update_defect(request, pk):
    defect = get_object_or_404(Defect, pk=pk)
    
    # Check permission: Only creator or project manager can edit
    if request.user != defect.created_by and not request.user.is_project_manager:
        return redirect('project_detail', pk=defect.project.pk)
    
    if request.method == 'POST':
        form = DefectForm(request.POST, instance=defect)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=defect.project.pk)
    else:
        form = DefectForm(instance=defect)
    
    return render(request, 'core/update_defect.html', {'form': form, 'defect': defect})