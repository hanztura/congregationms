from django.contrib import messages


def user_has_no_user_group_middleware(get_response):
    """Check if user has no user group."""

    def middleware(request):
        user = request.user
        if not user.is_anonymous and not user.is_superuser:
            try:
                groups = user.publisher_groups.prefetch_related('group').all()
            except Exception as e:
                groups = user.publisher_groups.empty()
            request.authorized_groups = groups
            if not request.authorized_groups:
                msg = 'You have no authorization to work on any groups. Please \
                        inform your administrator.'
                messages.warning(request, msg)

        response = get_response(request)

        return response

    return middleware
