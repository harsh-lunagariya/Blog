from django.contrib import admin
from .models import Article,Profile, Comment,CommentReply

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display= ['user','article_id','created_at','title','short_content']
    
    def short_content(self, obj):
        return (obj.content[:50]+'...' if len(obj.content)>50 else obj.content)
    short_content.short_description = 'content'


admin.site.register(Article,ArticleAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(CommentReply)
