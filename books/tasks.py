from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.management import call_command
from django.db.models import Count, Sum

from .models import Book, Category


@shared_task
def send_email_task(subject, message, recipient_list):
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def generate_books_report():
    report = {
        "total_books": Book.objects.count(),
        "available_books": Book.objects.filter(is_available=True).count(),
        "total_stock": Book.objects.aggregate(total=Sum("stock"))["total"] or 0,
        "categories": list(
            Category.objects.annotate(book_count=Count("books")).values(
                "name",
                "book_count",
            )
        ),
    }

    cache.set("reports:books", report, 60 * 60)
    return report


@shared_task
def cleanup_expired_sessions():
    call_command("clearsessions")
    return "Expired sessions cleaned"