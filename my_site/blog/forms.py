from django import forms

from .models import Comment, Detail


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        exclude = ["post"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment"
        }
        
        
        
class InformationForm(forms.Form):
    user_name = forms.CharField()
    
    

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail 
        exclude = ["post"]
        labels = {
            "user_name": "שם",
            "user_email": "אימייל",
            "text": "תוכן הודעה"
        }