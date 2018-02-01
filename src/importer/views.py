from urllib.parse import urljoin

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, RedirectView

from .forms import CSVUploadForm
from .models import CSVUpload


class UploadCSVView(FormView):

    form_class = CSVUploadForm
    template_name = 'upload_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SaveUploadView(RedirectView):

    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.url = reverse('importer-list')

        CSVUpload.objects.create(
            file_name=kwargs.get('file_name'),
            link=urljoin(settings.S3_URL_TEMPLATE, kwargs.get('file_name')),
            user=auth.get_user(self.request),
        )

        return super().dispatch(*args, **kwargs)



class UploadsView(ListView):
    
    model = CSVUpload
    template_name = 'uploads.html'
    context_object_name = 'ups'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)