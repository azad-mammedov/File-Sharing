from django.contrib.auth.models import User
from django.shortcuts import render , HttpResponse , get_object_or_404
from .models import *

def index_view(request):
    files = File.objects.filter(user=request.user).order_by('-id')
    context = {'files':files}
    
    return render(request,'home/index.html',context)

def file_single(request,id):
    file = get_object_or_404(File.objects.all().prefetch_related('user'),id=id)
    if Permission.objects.filter(file=file,user=request.user).exists():
        permission = Permission.objects.get(file=file,user=request.user)
    context = {'file':file,}

    return render(request,'home/file_detail.html',context)

def shared_files(request):
    user = request.user
    files  = [x for x in Permission.objects.filter(user=request.user).select_related('file_f')]
    context = {'files':files}
    return HttpResponse('test')

    
def add_file(request):
    message = ""
    if request.method == "POST":
        file = request.POST.get('file')
        title = request.POST.get('title')
        description = request.POST.get('title')
        if title == "" or file is None:
            message="File and Title must be set"
        else:
            File.objects.create(file=file,title=title,description=description)
            message = "File Created"
    return render(request,'home/add_file.html')



