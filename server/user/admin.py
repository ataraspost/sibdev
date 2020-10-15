
from django.contrib import admin

from user.models import User, Precedent, EmailConfirmationToken

admin.site.register(User)
admin.site.register(Precedent)
admin.site.register(EmailConfirmationToken)
