from .models import Publisher


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


def get_publishers_as_choices(group=None):
    """"""
    publishers = Publisher.objects.all()
    if group:
        members = get_group_members(group)
        publishers = publishers.filter(id__in=members)

    # transform into (pk, value) Tuple
    publishers = [(p.pk, p.name) for p in publishers if p.group]
    publishers.insert(0, ('', '[Select a publisher]'))
    return publishers


def get_authorized_publishers():
    pass