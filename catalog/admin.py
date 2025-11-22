from django.contrib import admin
from .models import Profile, Question, Vote

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    search_fields = ['user__username']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'expires_at', 'is_active', 'votes_count']
    list_filter = ['created_at', 'expires_at', 'is_active']
    search_fields = ['title', 'short_description', 'full_description']
    readonly_fields = ['created_at', 'votes_count']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'voted_at']
    list_filter = ['voted_at', 'question']
    search_fields = ['user__username', 'question__title']
    readonly_fields = ['voted_at']