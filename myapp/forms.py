from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from myapp.models import MyUser, Purchase


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ('product', 'quantily')

    def save(self, user):
        purchase = super().save(commit=False)
        purchase.user = user
        purchase.save()
        return purchase

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name')

    def save(self):
        MyUser = super().save(commit=False)
        MyUser.bank = 100.0
        MyUser.save()
        return MyUser
