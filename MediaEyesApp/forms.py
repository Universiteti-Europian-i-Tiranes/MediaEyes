from django import forms
from .models import Contact , Video 


# si do te kete e paraqitur ne panelin e adminit per file kontaktetfrom django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'country', 'phone', 'email', 'subject']
        widgets = {
            'subject': forms.Textarea(attrs={'rows': 5}),
        }

#forms per videoshow.html

class VideoLinkForm(forms.Form):
    link = forms.URLField(label="YouTube Video Link", required=True)
