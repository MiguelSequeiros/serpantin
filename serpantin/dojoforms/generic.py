from django.db import connection, transaction
from django.db.models.fields.related import create_many_related_manager, ManyRelatedObjectsDescriptor, ReverseManyRelatedObjectsDescriptor, ManyToManyField
from django.utils.functional import curry
from django.contrib.contenttypes.models import ContentType

def create_generic_many_related_manager(superclass):
    class GenericManyRelatedManager(create_many_related_manager(superclass)):
        def __init__(self, model=None, core_filters=None, instance=None, symmetrical=None,
                     join_table=None, source_col_name=None, target_col_name=None, content_type=None,
                     content_type_field_name=None, object_id_field_name=None):
            super(GenericManyRelatedManager, self).__init__(model, core_filters, instance, symmetrical,
                  join_table, source_col_name, target_col_name)
            self.content_type = content_type
            self.content_type_field_name = content_type_field_name
            self.object_id_field_name = object_id_field_name

        def _add_items(self, source_col_name, target_col_name, *objs):
            # join_table: name of the m2m link table
            # source_col_name: the PK colname in join_table for the source object
            # target_col_name: the PK colname in join_table for the target object
            # *objs - objects to add. Either object instances, or primary keys of object instances.

            # If there aren't any objects, there is nothing to do.
            if objs:
                # Check that all the objects are of the right type
                new_ids = set()
                for obj in objs:
                    if isinstance(obj, self.model):
                        new_ids.add(obj._get_pk_val())
                    else:
                        new_ids.add(obj)
                # Add the newly created or already existing objects to the join table.
                # First find out which items are already added, to avoid adding them twice
                cursor = connection.cursor()
                cursor.execute("SELECT %s FROM %s WHERE %s = %%s AND %s = %%s AND %s IN (%s)" % \
                    (target_col_name, self.join_table, self.content_type_field_name,
                    source_col_name, target_col_name, ",".join(['%s'] * len(new_ids))),
                    [content_type.id, self._pk_val] + list(new_ids))
                existing_ids = set([row[0] for row in cursor.fetchall()])

                # Add the ones that aren't there already
                for obj_id in (new_ids - existing_ids):
                    cursor.execute("INSERT INTO %s (%s, %s, %s) VALUES (%%s, %%s)" % \
                        (self.join_table, source_col_name, target_col_name),
                        [content_type.id, self._pk_val, obj_id])
                transaction.commit_unless_managed()

        def _remove_items(self, source_col_name, target_col_name, *objs):
            # source_col_name: the PK colname in join_table for the source object
            # target_col_name: the PK colname in join_table for the target object
            # *objs - objects to remove

            # If there aren't any objects, there is nothing to do.
            if objs:
                # Check that all the objects are of the right type
                old_ids = set()
                for obj in objs:
                    if isinstance(obj, self.model):
                        old_ids.add(obj._get_pk_val())
                    else:
                        old_ids.add(obj)
                # Remove the specified objects from the join table
                cursor = connection.cursor()
                cursor.execute("DELETE FROM %s WHERE %s = %%s AND %s = %%s AND %s IN (%s)" % \
                    (self.join_table, self.content_type_field_name,
                    source_col_name, target_col_name, ",".join(['%s'] * len(old_ids))),
                    [content_type.id, self._pk_val] + list(old_ids))
                transaction.commit_unless_managed()

        def _clear_items(self, source_col_name):
            # source_col_name: the PK colname in join_table for the source object
            cursor = connection.cursor()
            cursor.execute("DELETE FROM %s WHERE %s = %%s AND %s = %%s" % \
                (self.join_table, self.content_type_field_name, source_col_name),
                [content_type.id, self._pk_val])
            transaction.commit_unless_managed()

    return GenericManyRelatedManager

class GenericManyRelatedObjectsDescriptor(ManyRelatedObjectsDescriptor):
    # This class provides the functionality that makes the related-object
    # managers available as attributes on a model class, for fields that have
    # multiple "remote" values and have a GenericManyToManyField pointed at them by
    # some other model (rather than having a GenericManyToManyField themselves).
    # In the example "publication.article_set", the article_set attribute is a
    # GenericManyRelatedObjectsDescriptor instance.
    pass
    # TODO: add code here

class ReverseGenericManyRelatedObjectsDescriptor(ReverseManyRelatedObjectsDescriptor):
    # This class provides the functionality that makes the related-object
    # managers available as attributes on a model class, for fields that have
    # multiple "remote" values and have a GenericManyToManyField defined in their
    # model (rather than having another model pointed *at* them).
    # In the example "article.publications", the publications attribute is a
    # ReverseGenericManyRelatedObjectsDescriptor instance.
    def __get__(self, instance, instance_type=None):
        if instance is None:
            raise AttributeError, "Manager must be accessed via instance"

        # Dynamically create a class that subclasses the related
        # model's default manager.
        rel_model=self.field.rel.to
        superclass = rel_model._default_manager.__class__
        RelatedManager = create_generic_many_related_manager(superclass)

        qn = connection.ops.quote_name
        content_type = ContentType.objects.get_for_model(self.field.model)
        manager = RelatedManager(
            model=rel_model,
            core_filters={
                '%s__pk' % self.field.content_type_field_name: content_type.id,
                '%s__exact' % self.field.object_id_field_name: instance._get_pk_val(),
            },
            instance=instance,
            symmetrical=(self.field.rel.symmetrical and instance.__class__ == rel_model),
            join_table=qn(self.field.m2m_db_table()),
            source_col_name=qn(self.field.m2m_column_name()),
            target_col_name=qn(self.field.m2m_reverse_name()),
            content_type = content_type,
            content_type_field_name = self.field.content_type_field_name,
            object_id_field_name = self.field.object_id_field_name
        )

        return manager

class GenericManyToManyField(ManyToManyField):
    def __init__(self, to, **kwargs):
        # Override content-type/object-id field names on the m2m table
        self.object_id_field_name = kwargs.pop("object_id_field", "object_id")
        self.content_type_field_name = kwargs.pop("content_type_field", "content_type")
        super(GenericManyToManyField, self).__init__(to, **kwargs)

    def _get_m2m_db_table(self, opts):
        "Function that can be curried to provide the m2m table name for this relation"
        if self.db_table:
            return self.db_table
        else:
            return '%s_m2m' % opts.db_table

    def _get_m2m_column_name(self, related):
        "Function that can be curried to provide the source column name for the m2m table"
        return self.object_id_field_name

    def _get_m2m_reverse_name(self, related):
        "Function that can be curried to provide the related column name for the m2m table"
        return related.parent_model._meta.object_name.lower() + '_id'

    def contribute_to_class(self, cls, name):
        super(ManyToManyField, self).contribute_to_class(cls, name)
        # Save a reference to which model this class is on for future use
        self.model = cls
        # Add the descriptor for the m2m relation
        setattr(cls, self.name, ReverseGenericManyRelatedObjectsDescriptor(self))

        # Set up the accessor for the m2m table name for the relation
        self.m2m_db_table = curry(self._get_m2m_db_table, cls._meta)

    def contribute_to_related_class(self, cls, related):
        # m2m relations to self do not have a ManyRelatedObjectsDescriptor,
        # as it would be redundant - unless the field is non-symmetrical.
        if related.model != related.parent_model or not self.rel.symmetrical:
            # Add the descriptor for the m2m relation
            setattr(cls, related.get_accessor_name(), GenericManyRelatedObjectsDescriptor(related))

        # Set up the accessors for the column names on the m2m table
        self.m2m_column_name = curry(self._get_m2m_column_name, related)
        self.m2m_reverse_name = curry(self._get_m2m_reverse_name, related)
