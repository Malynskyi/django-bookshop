# from django.contrib import admin
# from books.models import Book


# admin.site.register(Book)



from django.contrib import admin
from .models import Book, Category, Meeting, Publisher
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class PublisherInline(admin.TabularInline):
    model = Publisher
    fields = ('contact_phone',)
    extra = 0

User = get_user_model()
admin.site.unregister(User)
admin.site.register(Publisher)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [PublisherInline]
    list_display = ('username', 'email', 'full_name', 'is_active', 'is_publisher')
    ordering = ('email',)

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip()
    full_name.short_description = 'Full_name'

    def is_publisher(self, obj):
        return hasattr(obj, 'publisher')
    is_publisher.short_description = 'Is publisher'


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



