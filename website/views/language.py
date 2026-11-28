from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


@require_POST
def switch_language(request):
    language = request.POST.get("language")
    if language not in {"en", "hi"}:
        return HttpResponseBadRequest("Unsupported language.")

    request.session["site_language"] = language
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect("home")
