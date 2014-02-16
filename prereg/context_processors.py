def include_registrant(request):
    return {
        'registrant': getattr(request.user, 'registrant', None),
    }
