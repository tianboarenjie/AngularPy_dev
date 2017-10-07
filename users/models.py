from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

__all__ = ["UserManager", "User"]


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(
            email,
            username=username,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):

    def __str__(self):
        return "<%s: %s>" % (self.username, self.get_email_field_name())

    def get_full_name(self):
        return self.username + self.get_email_field_name()

    def get_short_name(self):
        return self.username

    username = models.CharField(max_length=50, unique=True, verbose_name=u"用户名")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"手机号码")
    webchat = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"微信")
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"QQ")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name=u"注册时间")
    last_login = models.DateTimeField(auto_now=True, verbose_name=u"最后登录时间")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"备注")

    object = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = "angularpy_users"
        verbose_name = u"系统用户表"
        verbose_name_plural = u"系统用户表"
