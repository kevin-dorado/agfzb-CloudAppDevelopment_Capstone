from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view

    # path for contact us view

    # path for registration

    # path for login

    # path for logout

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
  path(route='static/', view=views.static_template_view, name='static_template'),

  path(route='about/', view=views.get_about, name='about'),
    # path for add a review view
 path(route='contact/', view=views.get_contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)