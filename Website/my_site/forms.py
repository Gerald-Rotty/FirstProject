from django import forms
from .models import Comment
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info("Sending email...")
        message = "From: {0}\n{1}".format(
            self.cleaned_data["name"],
            self.cleaned_data["message"],
        )
        send_mail(
            "Site message",
            message,
            "admin@admin.com",
            ["admin@admin.com"],
            fail_silently=False,
        )

