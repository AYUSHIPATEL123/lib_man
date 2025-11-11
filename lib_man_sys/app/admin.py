print("✅ app.admin loaded")
from django.contrib import admin
from .models import User,Book,BookIssue
from django.core.exceptions import PermissionDenied
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'available_copies')
    prepopulated_fields = {'slug': ('title',)}
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issue_date', 'return_date', 'renual_date', 'status') 

        
admin.site.register(User,UserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookIssue,BookIssueAdmin)
