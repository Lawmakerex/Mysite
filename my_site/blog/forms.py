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
    
    


class DetailForm(forms.Form):
    
   שם = forms.CharField(max_length=255)
   טלפון = forms.CharField(max_length=10)
   מייל = forms.EmailField()
   נושא = forms.CharField(max_length=255)
   תוכן = forms.CharField(widget=forms.Textarea,required=True)