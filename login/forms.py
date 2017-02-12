from django import forms
from models import Profile, Studies

# class ParticipantForm(forms.Form):
# 	years = [x for x in range(1920,2018)]
# 	dateOfBirth = forms.DateField(widget=forms.SelectDateWidget(years=years))

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['dateOfBirth','sex','height','weight']
        widgets = { 'dateOfBirth':forms.SelectDateWidget(years=[x for x in range(1920,2018)]), 'sex':forms.RadioSelect,
                    'height':forms.NumberInput(),'height':forms.NumberInput(),
                    }


class StudyForm(forms.ModelForm):

    class Meta:
        model = Studies
        fields = ['name','description','inclusion','exclusion']
        widgets = {'name':forms.TextInput(attrs={"size":"20"}),'description':forms.Textarea,'exclusion':forms.Textarea,'inclusion':forms.Textarea}

    # studyName = forms.CharField(label='Study Name', max_length=100)
    # description = forms.CharField(widget=forms.Textarea, label = "Description")
    # exclusion = forms.CharField(widget=forms.Textarea,label = "Exclusion Criteria")
    # inclusion = forms.CharField(widget=forms.Textarea,label = "Inclusion Criteria")
    # profile = ProfileForm()

    def populate_Form(self, study):
    	self.studyName = forms.CharField(label='Study Name: ', max_length=100, initial = study.name)
    	self.description = forms.CharField(widget=forms.Textarea, label = "Description", initial = study.description)
    	self.exclusion = forms.CharField(widget=forms.Textarea,label = "Exclusion Criteria", initial = study.exclusion)
    	self.inclusion = forms.CharField(widget=forms.Textarea,label = "Inclusion Criteria", initial = study.inclusion)

