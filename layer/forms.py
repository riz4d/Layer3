from django.forms import ModelForm
from .models import userlog,usercr

class user_login(ModelForm):
	class Meta:
		model = userlog
		fields = '__all__'

class user_cr(ModelForm):
	class Meta:
		model = usercr
		fields = '__all__'