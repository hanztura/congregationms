class OrderByPublisherMixin():

    class Meta:
        ordering = ('publisher__last_name', 'publisher__first_name',
                    'publisher__middle_name')
