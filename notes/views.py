from django.shortcuts import  render
from django.views import generic
from .models import Note
import datetime
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from urllib.parse import unquote
from django.views.generic import TemplateView

class IndexView(generic.ListView):
    model = Note
    template_name = "notes/index.html"
    context_object_name = "latest_notes_list"

    def get_queryset(self):
        """Return all notes ordered by the publication date."""
        return Note.objects.order_by("-pub_date")
    
    def get_context_data(self, **kwargs):
        """Add current time to the context."""
        context = super().get_context_data(**kwargs)
        context["current_time"] = datetime.datetime.now()
        context["database_path"] = settings.DATABASES["default"]["NAME"]
        return context



class DetailView(generic.DetailView):
    model = Note
    template_name = "notes/detail.html"


def directory_browser(request, path=""):
    # Decode URL-encoded path (for cases where special characters exist)
    path = unquote(path)
    
    # Root directory for browsing
    base_dir = settings.BASE_DIR  # กำหนด directory หลัก
    target_dir = os.path.join(base_dir, path)

    # ตรวจสอบว่ามี directory หรือไฟล์นั้นอยู่จริงหรือไม่
    if not os.path.exists(target_dir):
        raise Http404("Directory does not exist")

    # ถ้าเป็นไฟล์ ให้ดาวน์โหลดหรือแสดงผลไฟล์
    if os.path.isfile(target_dir):
        with open(target_dir, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/octet-stream")
            response["Content-Disposition"] = f'inline; filename="{os.path.basename(target_dir)}"'
            return response

    # ถ้าเป็น directory ให้แสดงรายการโฟลเดอร์และไฟล์
    items = os.listdir(target_dir)
    item_paths = [
        {
            "name": item,
            "path": os.path.join(path, item).replace("\\", "/"),  # สร้าง path แบบ UNIX-friendly
            "is_file": os.path.isfile(os.path.join(target_dir, item)),
        }
        for item in items
    ]

    return render(request, "notes/directory_browser.html", {
        "items": item_paths,
        "current_path": path,
    })
class HomePageView(TemplateView):
    template_name = "notes/home.html"