from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import My_Planning, User, UserMyPlanning
from .forms import AddUsersToPlanningForm, UpdatePlanningForm, UserDeleteForm, UserUpdateForm, UserGroupChangeForm, AddUsersToPlanningInstructorForm, MyUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.contrib.auth.models import Group

""""
SELECT   : all(), get()

WHERE    : filter() ex. Users.objects.all().filter( email = "johnDoe@gmail.com" )
            __gt = >, __lt = <, __gte >=, __lte = <=, __startswith, ex. ( role__gt = 2 )

ORDER BY : order_by()

LIMIT    : [:X]

raw()    : requête sql en dur ex. raw("SELECT * FROM MyDrivingSchool_users") jsp si ;

ADMIN !!!!

username: adminwac
email: wac@gmail.com
mdp: wac

GROUPES !!!!!!!

user.groups.add("student")
user.groups.remove("student")

utiliser la table My_Planning avec "rdv_member"
"""


@login_required
def index(request):
    context = {
        "message": "Salut les terriens !",
        "testCondition": 10,
        "testForList": ['testi', 'testo', 'testa', 'testouiile'],
        "users": User.objects.all()
    }
    return render(request, "MyDrivingSchool/index.html", context)



# @permission_required('MyDrivingShcool.delete_users') # <app_name>.<action>_<model_name>
@login_required
def show(request, user_name):
    # user = {"user": get_object_or_404(User, username = user_name)}
    # return render(request, "MyDrivingSchool/show.html", user)
    user = get_object_or_404(User, username=user_name)

    if request.method == 'POST':
        # Si le formulaire de mise à jour est soumis
        if 'update' in request.POST:
            update_form = UserUpdateForm(request.POST, instance=user)
            if update_form.is_valid():
                update_form.save()
                return redirect('show', user_name=user.username)
        # Si le formulaire de suppression est soumis
        elif 'delete' in request.POST:
            My_Planning.objects.filter(rdv_member = user).delete()
            user.delete()
            return redirect('index')
    else:
        update_form = UserUpdateForm(instance=user)
        delete_form = UserDeleteForm()

        liste_rdv = My_Planning.objects.filter(rdv_member = user)
        rdv_forms = [(rdv, UpdatePlanningForm(instance=rdv)) for rdv in liste_rdv]
    context = {
        'user_show': user,
        'update_form': update_form,
        'delete_form': delete_form,
        'rdv_forms': rdv_forms
    }

    return render(request, "MyDrivingSchool/show.html", context)


@login_required
def add_users_planning(request):
    # planning = My_Planning.objects.get()
    # users = User.objects.filter(username__in=usernames)
    # planning.users.add(*users)
    if request.method == 'POST':
        form = AddUsersToPlanningForm(request.POST)
        form_instructor = AddUsersToPlanningInstructorForm(request.POST, user=request.user)
        if form.is_valid():
            planning = form.save(commit=False)
            planning.save()
            rdv_members = [form.cleaned_data['student'], form.cleaned_data['instructor']]
            planning.rdv_member.set(rdv_members)
            return redirect('index')
        if form_instructor.is_valid():
            planning = form_instructor.save(commit=False)
            planning.save()
            rdv_members = [form_instructor.cleaned_data['student'], form_instructor.cleaned_data['instructor']]
            planning.rdv_member.set(rdv_members)
            return redirect('index')
    else:
        form = AddUsersToPlanningForm()
        form_instructor = AddUsersToPlanningInstructorForm(user=request.user)
    return render(request, 'MyDrivingSchool/add_users_to_planning.html', {'form': form, 'form_instructor': form_instructor})

@login_required
def show_rdv(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            rdv_id = request.POST.get('id')
            rdv_instance = My_Planning.objects.get(id=rdv_id)
            rdv_instance.delete()
            return redirect('planning')
        else:
            rdv_id = request.POST.get('id')
            rdv_instance = My_Planning.objects.get(id=rdv_id)
            form = UpdatePlanningForm(request.POST, instance=rdv_instance)
            if form.is_valid():
                form.save()
                return redirect('planning')
    else:
        liste_rdv = My_Planning.objects.all()
        rdv_forms = [(rdv, UpdatePlanningForm(instance=rdv)) for rdv in liste_rdv]

    return render(request, 'MyDrivingSchool/show_rdv.html', {'rdv_forms': rdv_forms})


# @login_required
# def change_user_group(request):
#     if request.method == 'POST':
#         form = UserGroupChangeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')  # Redirige vers une page de succès
#     else:
#         form = UserGroupChangeForm()
#     return render(request, 'MyDrivingSchool/change_users_group.html', {'form': form})

@login_required
def change_user_group(request):
    if request.method == 'POST':
        group_form = UserGroupChangeForm(request.POST)
        user_form = MyUserCreationForm(request.POST)
        
        if 'change_group' in request.POST and group_form.is_valid():
            group_form.save()
            return redirect('index')  # Redirige vers une page de succès après changement de groupe

        elif 'create_user' in request.POST and user_form.is_valid():
            user = user_form.save()
            default_group, created = Group.objects.get_or_create(name='student')
            user.groups.add(default_group)
            return redirect('group')

    else:
        group_form = UserGroupChangeForm()
        user_form = MyUserCreationForm()

    context = {
        'group_form': group_form,
        'user_form': user_form,
    }
    return render(request, 'MyDrivingSchool/change_users_group.html', context)





# @login_required
# def add_profil(request):
#     users = Users.objects.create(firstname = "jean", lastname = "Dupont-morreti", username = "LaHaine", email = "gang@bsb.brr", password = "azertyuiop", role = 4)
#     return redirect("index")

# @login_required
# def delete_profil(request):
#     users = Users.objects.filter(username = 'LaHaine')
#     users.delete()
#     return redirect("index")

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = RegisterForm()
#     context = {"form": form}
#     return render(request, "MyDrivingSchool/register.html", context)