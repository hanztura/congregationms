from django.contrib import messages

from publishers.models import Member

def user_has_no_user_group_middleware(get_response):
    """Check if user has no user group."""

    def middleware(request):
        user = request.user
        # anonymous and superusers has no groups allowed
        if not user.is_anonymous and not user.is_superuser:
            if request.path not in ('/', '/dashboard'):
                print(request.path)
                try:
                    groups = user.publisher_groups.prefetch_related('group').all()
                    _groups = [g.group for g in groups]
                except Exception as e:
                    groups = user.publisher_groups.empty()

                members= Member.objects.filter(group__in=_groups, is_active=True).select_related('publisher')
                authorized_publisher_pks = [m.publisher_id for m in members]
                if not request.authorized_groups:
                    msg = 'You have no authorization to work on any groups. Please \
                            inform your administrator.'
                    messages.warning(request, msg)
        else:
            groups = user.publisher_groups.empty()
            authorized_publisher_pks = []

        request.authorized_groups = groups
        request.authorized_publisher_pks = authorized_publisher_pks

        response = get_response(request)
        return response

    return middleware
