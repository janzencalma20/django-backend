from django.contrib import messages
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Organisation(models.Model):
    name = models.CharField(max_length=100, null=True)
    projects = models.ManyToManyField('Project', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None, organisation=None):
        user = self.create_user(email, name, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'organisation']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)


class Slot(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True, default=list)


class Loss(models.Model):
    type = models.CharField(max_length=100, null=True)
    data = models.JSONField(blank=True, null=True)


class Winding(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True, default=list)


class Conductor(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True, default=list)


class Material(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True, default=list)


class Hole(models.Model):
    type = models.CharField(max_length=100)
    data = models.JSONField(blank=True, null=True)


class Results(models.Model):
    type = models.CharField(max_length=100, null=True)
    data = models.JSONField(blank=True, null=True, default=list)


class Housing(models.Model):
    type = models.CharField(max_length=100, null=True)
    data = models.JSONField(blank=True, null=True, default=list)


class Stator(models.Model):
    type = models.CharField(max_length=100, null=True)
    data = models.JSONField(blank=True, null=True, default=list)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    winding = models.ForeignKey(Winding, on_delete=models.SET_NULL, null=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True)


class Rotor(models.Model):
    type = models.CharField(max_length=100, null=True)
    data = models.JSONField(blank=True, null=True, default=list)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    winding = models.ForeignKey(Winding, on_delete=models.SET_NULL, null=True)
    conductor = models.ForeignKey(Conductor, on_delete=models.SET_NULL, null=True)
    hole = models.ForeignKey(Hole, on_delete=models.SET_NULL, null=True)


class Cooling(models.Model):
    type = models.CharField(max_length=100, null=True)
    htc = models.JSONField(blank=True, null=True, default=list)
    flow = models.JSONField(blank=True, null=True, default=list)


class LPTN(models.Model):
    input = models.JSONField(blank=True, null=True, default=list)
    result = models.JSONField(blank=True, null=True, default=list)


class Machine(models.Model):
    name = models.CharField(max_length=100, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stator = models.ForeignKey(Stator, on_delete=models.SET_NULL, null=True)
    rotor = models.ForeignKey(Rotor, on_delete=models.SET_NULL, null=True)
    housing = models.ForeignKey(Housing, on_delete=models.SET_NULL, null=True)
    cooling = models.ForeignKey(Cooling, on_delete=models.SET_NULL, null=True)
    loss = models.ForeignKey(Loss, on_delete=models.SET_NULL, null=True)
    lptn = models.ForeignKey(LPTN, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('Machine detail', kwargs={'id': self.id})

    def post(self, request):
        if request.method == 'POST':
            for key in request.POST.getlist('id'):
                update = Machine.objects.get(id=key)
                form = Machine(request.POST, instance=update)
                if form.is_valid():
                    form.save()
                messages.success(request, message='value changed')
            return redirect('machine')
