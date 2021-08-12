from django.views.generic.base import TemplateView

class CvView(TemplateView):
    template_name = "cv.html"
