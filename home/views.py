from typing import ContextManager
from django.contrib.auth.models import User
from django.shortcuts import render , HttpResponse , get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required , user_passes_test


#your files
def index_view(request):
    if request.user.is_authenticated:

        files = File.objects.filter(user=request.user).order_by('-id')
    else:
        files = []
    
    context = {'files':files}
    
    return render(request,'home/index.html',context)




#file detail page for reading comments
@login_required(login_url="/account/login")
def file_single(request,id):
    can_comment = False
    file = get_object_or_404(File.objects.all().prefetch_related('user'),id=id)
    comments = Comment.objects.filter(file=file)
    if request.user==file.user:
        can_comment = True
    elif Permission.objects.filter(file=file,user=request.user).exists():
        permission = Permission.objects.get(file=file,user=request.user)
        can_comment = True if permission.comment else False
    else:
        return HttpResponse("<h1>You dont have  access this file</h1>")
    
    context ={
        'can_comment':can_comment,
        'file':file,
        'comments':comments
    }

    return render(request,'home/file_detail.html',context)





    

    
#files which shared to you
@login_required(login_url='/account/login')
def shared_files(request):
    print(Permission.objects.filter(user=request.user))

    user = request.user
    files  = [x.file for x in Permission.objects.filter(user=request.user).select_related('file')]
    context = {'files':files}
    return render(request,'home/shared_files.html',context)


#file upload
@login_required(login_url='/account/login')
def add_file(request):
    message = ""
    if request.method == "POST":
        file = request.FILES.get('file')
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title == "" or file is None:
            message="File and Title must be set"
        else:
            File.objects.create(file_field=file,title=title,description=description,user=request.user)
            message = "File Created"
    
    context = {'message':message}

    return render(request,'home/add_file.html',context)



