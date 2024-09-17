import requests
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .tasks import add_online_user, reduce_online_user

# 这里需要使用celery来增加当日用户在线数量峰值
class LoginViewSet(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        result = add_online_user.delay(self.request.POST.get('username'),
                                       self.request.POST.get('csrfmiddlewaretoken'))
        task_id = result.id
        self.request.session.setdefault('celery_task_id', task_id)
        return HttpResponseRedirect(self.get_success_url())


class LogoutViewSet(LogoutView):
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        task_id = request.session['celery_task_id']
        auth_logout(request)
        reduce_online_user.delay(task_id)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    # Django5.0移除了get方法，所以继承LogoutView类的时候，还需要进行下面的设置才能正常走子类的post方法
    get = post

