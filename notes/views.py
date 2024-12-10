from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Note

class IndexView(generic.ListView):
    model = Note
    template_name = "notes/index.html"
    context_object_name = "latest_notes_list"

    def get_queryset(self):
        """Return all notes ordered by the publication date."""
        return Note.objects.order_by("-pub_date")



class DetailView(generic.DetailView):
    model = Note
    template_name = "notes/detail.html"

