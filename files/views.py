from django.shortcuts import render, redirect

from django.views.generic import ListView
from django.contrib import messages

from .Metadata import getmetadata
from .forms import DocumentForm
from .models import Document
from .predict import predict_gen



# Create your views here.
class IndexView(ListView):
    template_name= 'index.html'
    def get_queryset(self):
        return True

def model_form_upload(request):

    documents = Document.objects.all()
    if request.method == 'POST':
        if len(request.FILES) == 0:
            messages.error(request,'Upload a file')
            return redirect("files:index")

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploadfile = request.FILES['document']
            print(uploadfile.name)
            print(uploadfile.size)
            if not uploadfile.name.endswith('.wav'):
                messages.error(request,'Only .wav file type is allowed')
                return redirect("files:index")
            meta = getmetadata(uploadfile)
            
            genre = predict_gen(meta)
            print(genre)

            context = {'genre':genre}
            return render(request,'result.html',context)

    else:
        form = DocumentForm()

    return render(request,'result.html',{'documents':documents,'form':form})