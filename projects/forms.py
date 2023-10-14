# created seperately from the original django files
# used to store all the models used for forms

from django.forms import ModelForm
from django import forms
from .models import Project, Review

# by convention, suggested syntax is <ModelName>Form
class ProjectForm(ModelForm):
    # Model Meta is used to change order options, verbose_name (its optional) in the
    class Meta:
        model = Project
        # can create a list or use '__all__'
        fields = ["title", "description", "featured_image", "demo_link", "source_link", "tags"]

        # Q: what is django doing when you declare field?
            # A: it is taking all the required fields from the project model
            # and turning them into input fields (less those with attribute editable=False
            # and auto_now_add=True) (aka non-editable fields)

        widgets = {
            # turns the tags field into a custom multicheckbox field
            'tags': forms.CheckboxSelectMultiple
        }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # update the class where title is an input
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add description here'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]

        # widgets = {
        #     "value": forms.Select
        # }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
        
        self.fields['body'].widget.attrs.update({'class': 'input', 'placeholder': 'Type your review here'})





