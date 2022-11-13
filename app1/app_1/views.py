from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UploadForm,UserForm
from .models import Document,User,Role,Student_Document
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseNotAllowed
import os
from django.db.models import Q
import time
import datetime
from django.core.paginator import Paginator
from django.db.models import Count


def document_count(request):
    if request.user.role.id == 1 or request.user.is_superuser:
        context = {}
        teachers = User.objects.filter(role_id = 3).annotate(num_docs = Count('document'))
        context['prof'] = teachers
        return render(request, 'admin/document_count.html', context)

def student_count(request):
    if request.user.role.id == 1 or request.user.is_superuser:
        context = {}
        stud_count = Document.objects.annotate(num_stud = Count('student_document'))
        context['stud'] = stud_count
        return render(request, 'admin/student_count.html', context)

@login_required(login_url="/login/")
def document_details(request, document_id):
  context = {}
  context["data"] = Document.objects.get(id=document_id)
  context["users"] = Student_Document.objects.filter(document_id_id=document_id)
  return render(request, "admin/document_details.html", context)

@login_required(login_url="/login/")
def professor_details(request, user_id):
  context = {}
  context["data"] = User.objects.get(id=user_id)
  context["docs"] = Document.objects.filter(created_by_id=user_id)
  return render(request, "admin/professor_details.html", context)

#UNUSED
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document'] if 'document' in request.FILES else None
        if uploaded_file:
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name,uploaded_file)
                fileurl = fs.url(name)
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.path = fileurl
                    form.created_by = request.user
                    form.time_uploaded = time.localtime()
                    form.date_uploaded = datetime.datetime.today() 
                    form.save()
                    return redirect('document_all')

#HOME PAGE
@login_required(login_url='/login/')
def home(request):
    context = {}
    users = User.objects.all()
    documents = Document.objects.all()
    context['users'] = users
    context['documents'] = documents
    return render(request, 'home.html', context)

#DOCUMENT ADD
@login_required(login_url='/login/')
def document_add(request):
    if request.user.role.id == 3:
        if request.method == 'POST':
            uploaded_file = request.FILES['document'] if 'document' in request.FILES else None
            if uploaded_file:
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name,uploaded_file)
                fileurl = fs.url(name)
                form = UploadForm(request.POST, request.FILES)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.path = fileurl
                    form.created_by = request.user
                    form.time_uploaded = time.localtime()
                    form.date_uploaded = datetime.datetime.today() 
                    form.save()
                    return redirect('document_all')
            else: 
                form = UploadForm()
                form.save()
        else:
            form = UploadForm()
            return render(request, 'prof/document_add.html', {'form': form})
    return redirect('home')

#DOCUMENT LIST (PROFESSOR)
@login_required(login_url='/login/')
def document_all(request):
    if request.user.role.id == 3:
        documents = Document.objects.all()
        paginator = Paginator(documents, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'prof/document_all.html',{'page_obj':page_obj})
    return redirect('home')

#DOCUMENT LIST (STUDENT)
@login_required(login_url='/login/')
def document_list_shared(request, sort = "-time", filter = 0):
    if request.user.role.id == 2:
        documents = Student_Document.objects.filter(student_id_id = request.user.id)
        teachers = User.objects.filter(role_id = 3)

        shared = []
        filtered = []
        for doc in documents:    
            shared.append(doc.document_id)

        if sort == "-time":
            shared.sort(key=lambda x: x.time_uploaded, reverse=False)
        elif sort == "-date":
            shared.sort(key=lambda x: x.date_uploaded, reverse=False)

        else:
            shared.sort(key=lambda x: x.title, reverse=False)
        if (filter != 0):
            for hit in shared:
                if hit.created_by_id == filter:
                    filtered.append(hit)
            shared = filtered

        paginator = Paginator(shared, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'stud/document_list_shared.html', {'prof': teachers, 'page_obj': page_obj})
    return redirect('home')

#DOCUMENT DELETION
@login_required(login_url='/login/')
def document_delete(request, document_id):
    doc = Document.objects.get(pk = document_id)
    if request.user.role.id == 3 and request.user.is_authenticated:
        os.remove(doc.path)
        doc.delete()
        return redirect('document_all')
    return redirect('home')

#DOCUMENT EDIT (SHARE/UNSHARE)
@login_required(login_url='/login/')
def document_edit(request, document_id):
    if request.user.role.id == 3:
        if request.method == 'POST':   
            Student_Document.objects.filter(document_id = document_id).delete()
            Document.objects.filter(id=document_id).update(last_edited=datetime.datetime.now())
            for id in request.POST:
                if id != "csrfmiddlewaretoken":
                    share = Student_Document(document_id_id = document_id, student_id_id = id)
                    share.save()
                else: continue  
        else:
            users = User.objects.filter(role = 2)
            shared = Student_Document.objects.filter(document_id = document_id)
            for u in users:
                for s in shared:
                    if u.id == s.student_id_id:
                        u.shared = True
                        break
            return render(request, 'prof/document_edit.html', {'users': users})
        return redirect('document_all')
    return redirect('home')

#USER ADD/CREATE USER
@login_required(login_url='/login/')
def user_add(request):
  if request.method == 'GET':
    userform = UserForm()
    if request.user.is_authenticated and request.user.role_id==1:
      return render (request,'admin/user_add.html',{'form':userform})
    else:
      return HttpResponse ("You're not authorized to do that.")
  elif request.method == 'POST':
    userform = UserForm(request.POST)
    if request.user.is_authenticated and userform.is_valid() and request.user.role_id==1:
      form = userform.save(commit=False)
      form.password = make_password(userform.cleaned_data['password'])
      form.save()
      return redirect('user_all')
    else:
      return HttpResponse("You're not authorized to add new users.")

#USER EDIT
@login_required(login_url='/login/')
def user_edit(request, user_id):           
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        data_to_update = UserForm(instance=user)
        return render(request, 'admin/user_edit.html', {'form': data_to_update})
    elif request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated and request.user.role_id==1:
          data_to_update = UserForm(request.POST, instance=user)
          if data_to_update.is_valid():
              form = data_to_update.save(commit=False)
              form.password = make_password(data_to_update.cleaned_data['password'])
              data_to_update.save()
              return redirect('user_all')
        else:
          return HttpResponse ("You're not authorized to edit user info.")
    else:
        return HttpResponse("Something went wrong.")

#USER LIST (ADMIN)
@login_required(login_url='/login/')
def user_all(request):
    if request.user.is_superuser or request.user.role.id == 1:
        users = User.objects.filter(Q(role=2) | Q(role=3)).order_by('role')
        paginator = Paginator(users, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/user_all.html', {'page_obj': page_obj})
    return redirect('home')

#USER DELETION
@login_required(login_url='/login/')
def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_superuser and request.user.is_authenticated:
        user.delete()
        return redirect('user_all')
    return HttpResponse ("You're not authorized to delete this user.")




