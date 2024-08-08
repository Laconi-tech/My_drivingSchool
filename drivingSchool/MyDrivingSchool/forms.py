from django import forms
from .models import User, Group, My_Planning
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm


class AddUsersToPlanningForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='student'),
        label="Étudiant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    instructor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='instructor'),
        label="Instructeur",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    rdv_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'jj/mm/aaaa hh:mm'
        }),
        input_formats=['%d/%m/%Y %H:%M']
    )

    class Meta:
        model = My_Planning
        fields = ['rdv_date', 'title', 'student', 'instructor']



class UpdatePlanningForm(forms.ModelForm):
    class Meta:
        model = My_Planning
        fields = ['title', 'rdv_date']
        widgets = {
            'rdv_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder': 'jj/mm/aaaa hh:mm'
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UserDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(label='Confirmer la suppression', required=True)



# class UserGroupChangeForm(forms.Form):
#     # user = forms.ModelChoiceField(queryset=User.objects.all())
#     group = forms.ChoiceField(choices=[('student', 'étudiant'), ('instructor', 'instructeur')])


#     user = forms.ModelChoiceField(
#         queryset=User.objects.filter(Q(groups__name='instructor') | Q(groups__name='student')).distinct(),
#         label="Membre: ",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     def save(self):
#         user = self.cleaned_data['user']
#         group_name = self.cleaned_data['group']
#         group = Group.objects.get(name=group_name)
#         user.groups.clear()  # Supprime tous les groupes existants
#         user.groups.add(group)  # Ajoute l'utilisateur au nouveau groupe

class UserGroupChangeForm(forms.Form):
    group = forms.ChoiceField(choices=[('student', 'étudiant'), ('instructor', 'instructeur')])
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(Q(groups__name='instructor') | Q(groups__name='student')).distinct(),
        label="Utilisateur",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def save(self):
        user = self.cleaned_data['user']
        group_name = self.cleaned_data['group']
        user.groups.clear()
        group = Group.objects.get(name=group_name)
        user.groups.add(group)



class AddUsersToPlanningInstructorForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='student'),
        label="Étudiant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    instructor = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='instructor'),
        label="Instructeur",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    rdv_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'jj/mm/aaaa hh:mm'
        }),
        input_formats=['%d/%m/%Y %H:%M']
    )

    class Meta:
        model = My_Planning
        fields = ['rdv_date', 'title', 'student', 'instructor']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['instructor'].queryset = User.objects.filter(id=user.id)
            self.fields['instructor'].initial = user
            self.fields['instructor'].widget.attrs['readonly'] = True  # Rend le champ non modifiable
            self.fields['instructor'].widget.attrs['class'] = 'form-control'

    def clean_instructor(self):
        return self.fields['instructor'].initial
    


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


































# class  AddUsersToPlanningForm(forms.ModelForm):
#         def __init__(self, *args, **kwargs):
#             super(AddUsersToPlanning, self).__init__(*args, **kwargs)
#             self.fields['username'].queryset = User.objects.filter(groups__name='student')

#         usernames = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
                                               
        # student = forms.ModelChoiceField(queryset=User.objects.all().filter(groups__name='student'))
        # instructor = forms.ModelChoiceField(queryset=User.objects.all().filter(groups__name='instructor'))
        # class Meta:
        #     model = My_Planning
        #     fields = ['rdv_member']
            # label = {"username de l'étudiant", "username de l'instructeur"}

# liste déroulante
    # liste_role = [(1, "étudiant"), (2, "instructeur"), (3, "secrétaire")]
    # role = forms.ChoiceField(label= "role de l'utilisateur", choices= liste_role)

# class RegisterForm(forms.Form):
#     firstname = forms.CharField(label="Prénom: ", max_length = 20, min_length = 3)
#     lastname = forms.CharField(label="Nom: ", max_length = 20, min_length = 3)
#     username = forms.CharField(label="Nom d'utilasateur: ", max_length = 22, min_length = 5)
#     email = forms.CharField(label="email: ", max_length = 35, widget= forms.EmailInput)
#     password = forms.CharField(label="Mot de passe: ", widget= forms.PasswordInput)

# class RegisterForm(forms.ModelForm):
#     # role = forms.ModelChoiceField(queryset = Users.object.all(), label = "Role") faut juste trouver comment afficher les role a coté de son user si le compte est secretaire
#     class Meta:
#         model = Users
#         fields = ['firstname', 'lastname', 'username', 'email', 'password']
#         labels = {
#             "firstname": "Prénom: ",
#               "lastname": "Nom: ",
#               "username": "Nom d'utilisateur: ",
#               "email": "Email: ",
#               "password": "Mot de passe: "
#             }
#         widgets = {
#             'password': forms.PasswordInput(),
#         }