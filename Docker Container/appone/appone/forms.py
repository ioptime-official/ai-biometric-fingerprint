# from django import forms

# class RegistrationForm(forms.Form):
#     username = forms.CharField(max_length=30)
#     image = forms.ImageField()

#     def clean_username(self):
#         name = self.cleaned_data.get('username')
#         if len(name) < 4:
#             raise forms.ValidationError('Username must be at least 4 characters.')
#         return name

#     def clean_image(self):
#         image = self.cleaned_data.get('image')
#         if image and not image.content_type.startswith('image/'):
#             raise forms.ValidationError('File must be an image.')
#         return image


from django import forms
class RegistrationForm(forms.Form):
    name = forms.CharField(label='Enter your name', max_length=100)
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.content_type.startswith('image/'):
            raise forms.ValidationError('File must be an image.')
        return image

class LoginForm(forms.Form):
    # name = forms.CharField(label='Enter your name', max_length=100)
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.content_type.startswith('image/'):
            raise forms.ValidationError('File must be an image.')
        return image
