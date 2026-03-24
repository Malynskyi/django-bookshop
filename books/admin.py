# from django.contrib import admin
# from books.models import Book


# admin.site.register(Book)



from django.contrib import admin
from .models import Book, Category, Meeting, Publisher
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class PublisherInline(admin.TabularInline):
    model = Publisher
    fields = ('contact_phone',)
    extra = 0

admin.site.register(Publisher)


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'category')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author')
    fields = ['title', 'author', 'published_at', 'price', 'stock', 'category', 'description', 'is_available']
    # readonly_fields = ('published_at',)

admin.site.register(Meeting)



