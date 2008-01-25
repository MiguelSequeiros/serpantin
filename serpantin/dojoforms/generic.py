class GenericManyToManyField(models.ManyToManyField):
    def __init__(self, to, **kwargs):
        super(GenericManyToManyField, self).__init__(to, **kwargs)
