from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import BlogPost, User


class UserRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=255, label="Address")
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=20)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "profile_picture",
            "address",
            "city",
            "state",
            "pincode",
            "password1",
            "password2",
        )
        widgets = {
            "user_type": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {classes}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        field_styles = {
            "title": {
                "class": "form-control",
                "placeholder": "Enter an engaging title",
            },
            "image": {"class": "form-control"},
            "category": {"class": "form-select"},
            "summary": {
                "class": "form-control",
                "rows": 3,
                "placeholder": "A concise overview",
            },
            "content": {
                "class": "form-control",
                "rows": 8,
                "placeholder": "Write your full article here",
            },
        }
        for name, attrs in field_styles.items():
            self.fields[name].widget.attrs.update(attrs)
        self.fields["is_draft"].widget.attrs.update({"class": "form-check-input"})

    def save(self, commit=True):
        obj = super().save(commit=False)
        if not obj.pk:
            obj.author = self._user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = BlogPost
        fields = ["title", "image", "category", "is_draft", "summary", "content"]
