from django.contrib import admin
from .models import Post,  Comment, SearchKeyword

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'publish', 'status']
    list_filter = ['status', 'author', 'publish', 'created']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'body']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


class SearchKeywordInline(admin.StackedInline):
    model = SearchKeyword


class PostAdminWithKeywords(PostAdmin):
    inlines = [SearchKeywordInline]


admin.site.unregister(Post)
admin.site.register(Post, PostAdminWithKeywords)

