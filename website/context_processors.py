from logo.models import CollegeLogo

def college_logo(request):
    return {
        'college_logo': CollegeLogo.objects.first()
    }