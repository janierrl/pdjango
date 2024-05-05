from django.utils import timezone
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponseRedirect

class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                now = timezone.localtime(timezone.now())

                idle_duration = now - last_activity
                max_idle_duration = timezone.timedelta(seconds=settings.SESSION_IDLE_TIMEOUT_SECONDS)

                if idle_duration > max_idle_duration:
                    auth.logout(request)
                    del request.session['last_activity']
                    return HttpResponseRedirect(settings.LOGIN_URL)
            else:
                request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
