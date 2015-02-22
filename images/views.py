# Django libraries
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.template import RequestContext

# Application specific imports
from images.forms import FolderForm
from images.models import Image
from fossWebsite.helper import error_key, csrf_failure, logged_in
from fossWebsite.helper import get_session_variables

# Create your views here.


def upload_images(request):
    """
    View to store upload images specific to an event.
    Models used: Folder, Image
    """
    try:
        is_loggedin, username = get_session_variables(request)
        
        # User is not logged in
        if not is_loggedin:
            return HttpResponseRedirect('/register/login')
        
        # User is logged in
        else:
            if request.method == 'POST':
                form = FolderForm(request.POST, request.FILES)
    
                # form is not valid          
                if not form.is_valid():
                    error = "Invalid inputs"
                    return render_to_response('images/upload_images.html', \
                        {'form':form, 'error':error, }, \
                        RequestContext(request))
                
                # form is valid
                else:
                    cleaned_form_data = form.cleaned_data
                    folder_name = cleaned_form_data['folder_name']
                    # create a new folder
                    folder = form.save(commit=False)
                    folder.save()

                    # save images
                    image = request.FILES['image']
                    new_image_object = Image(img=image, \
                        folder_name = folder)
                    img_name = new_image_object.img.name 
                    new_image_object.save()
                    return render_to_response("images/success.html")
            else:
                return render_to_response('images/upload_images.html', \
                    {'form':FolderForm(), 'is_loggedin': is_loggedin },\
                     RequestContext(request))
    except KeyError:
        return error_key(request)

