from .models import Publisher, Group


class OrderByPublisherMixin():

    class Meta:
        ordering = ('publisher__last_name', 'publisher__first_name',
                    'publisher__middle_name')


def get_group_members(group):
    """Return a list of group members PK."""
    members = group.group_members.filter(is_active=True).select_related('publisher')
    members = [m.publisher.pk for m in members]  # member pk
    return members


def get_user_groups_members(authorized_groups):
    _members = [g.group.members_as_pk for g in authorized_groups]
    members = []
    for m in _members:
        members.extend(m)
    return members


def get_publishers_as_choices(request=None, as_queryset=False):
    """Returns a list of publisher tuple (pk, name).

    If request is given it will return only allowed publishers.
    """
    publishers = Publisher.objects.all()
    if request:
        members = request.authorized_publisher_pks
        publishers = publishers.filter(id__in=members)

    if not as_queryset:
        # transform into (pk, value) Tuple
        publishers = [(p.pk, p.name) for p in publishers]
        publishers.insert(0, ('', '[Select a publisher]'))

    return publishers


def get_groups_as_choices():
    q = Group.objects.all().select_related('congregation')
    q = [(g.pk, str(g)) for g in q]

    return q
