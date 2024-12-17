from django.test import TestCase, Client
from django.urls import reverse
from .models import Note
from django.utils.timezone import now
import os
from django.conf import settings
import shutil
from django.utils import timezone

class NoteModelTests(TestCase):
    def test_note_creation(self):
        """ทดสอบการสร้าง Note ว่าทำงานได้ถูกต้อง"""
        note = Note.objects.create(title="Test Note", content="Content", pub_date=timezone.now())
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.content, "Content")
    
    def test_note_list(self):
        """ทดสอบว่ารายการ Note ถูกต้อง"""
        Note.objects.create(title="Note 1", content="Content 1", pub_date=timezone.now())
        Note.objects.create(title="Note 2", content="Content 2", pub_date=timezone.now())
        self.assertEqual(Note.objects.count(), 2)

    def test_note_edit(self):
        """ทดสอบการแก้ไข Note ว่าอัปเดตข้อมูลได้ถูกต้อง"""
        note = Note.objects.create(title="Original Title", content="Original Content", pub_date=timezone.now())
        note.title = "Updated Title"
        note.save()
        self.assertEqual(note.title, "Updated Title")

class IndexViewTests(TestCase):
    def setUp(self):
        self.note1 = Note.objects.create(
            title="Note 1", pub_date=now(), content="Content of Note 1"
        )
        self.note2 = Note.objects.create(
            title="Note 2", pub_date=now(), content="Content of Note 2"
        )

    def test_index_view_status_code(self):
        """ตรวจสอบว่า IndexView ทำงานได้"""
        response = self.client.get(reverse("notes:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        """ตรวจสอบ context ใน IndexView"""
        Note.objects.create(title="Note 1", content="Content 1", pub_date=timezone.now())
        Note.objects.create(title="Note 2", content="Content 2", pub_date=timezone.now())
        
        response = self.client.get('/notes/')
        
        # ตรวจสอบว่า response มีสถานะ 200
        self.assertEqual(response.status_code, 200)
        
        # ตรวจสอบว่า context มี key 'note_list'
        self.assertIn('latest_notes_list', response.context)

        # ตรวจสอบ queryset ของ 'note_list'
        self.assertQuerySetEqual(
            response.context['latest_notes_list'],
            Note.objects.all(),
            ordered=False
        )

class DetailViewTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="Note Detail", pub_date="2024-12-12 12:00:00", content="Content of Detail"
        )

    def test_detail_view_status_code(self):
        """ตรวจสอบว่า DetailView ทำงานได้"""
        response = self.client.get(reverse("notes:detail", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        """ตรวจสอบ template ของ DetailView"""
        response = self.client.get(reverse("notes:detail", args=[self.note.id]))
        self.assertTemplateUsed(response, "notes/detail.html")


class DirectoryBrowserTests(TestCase):
    def setUp(self):
        self.test_dir = os.path.join(settings.BASE_DIR, "test_directory")
        os.makedirs(self.test_dir, exist_ok=True)

        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("This is a test file.")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_directory_browser_directory(self):
        """ตรวจสอบการแสดงรายการ directory"""
        response = self.client.get(reverse("notes:directory_browser_with_path", args=["test_directory"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_file.txt")

    def test_directory_browser_file(self):
        """ตรวจสอบการดาวน์โหลดไฟล์"""
        response = self.client.get(reverse("notes:directory_browser_with_path", args=["test_directory/test_file.txt"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/octet-stream")

    def test_directory_browser_404(self):
        """ตรวจสอบการแสดงผล 404 เมื่อ directory หรือไฟล์ไม่มีอยู่"""
        response = self.client.get(reverse("notes:directory_browser_with_path", args=["non_existing_path"]))
        self.assertEqual(response.status_code, 404)


class HomePageViewTests(TestCase):
    def test_home_page_status_code(self):
        """ตรวจสอบว่า HomePageView ทำงานได้"""
        response = self.client.get(reverse("notes:index"))  # เปลี่ยนเป็น index เพราะไม่มี route `home`
        self.assertEqual(response.status_code, 200)

