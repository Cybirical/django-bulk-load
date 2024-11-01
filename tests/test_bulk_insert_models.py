from datetime import datetime, timezone
import string

from django.test import TestCase
from django_bulk_load import bulk_insert_models
from django.db import IntegrityError
from .test_project.models import (
    TestComplexModel,
    TestForeignKeyModel,
    TestGISModel,
)

from django.contrib.gis.geos import Point


class E2ETestBulkInsertModelsTest(TestCase):
    def test_empty_upsert(self):
        self.assertEqual(bulk_insert_models([]), None)

    def test_single_insert_new(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        unsaved_model = TestComplexModel(
            integer_field=123,
            string_field="hello",
            json_field=dict(fun="run"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        bulk_insert_models([unsaved_model])

        saved_model = TestComplexModel.objects.get()
        self.assertIsNotNone(saved_model.id)
        for attr in ["integer_field", "string_field", "json_field", "test_foreign_id"]:
            self.assertEqual(getattr(saved_model, attr), getattr(unsaved_model, attr))

    def test_inserts_with_all_special_characters_tested(self):
        # This test is to ensure that all special characters are handled correctly
        # when inserting into the database
        # Added 2024-10-30. Prior to this date, the package was having trouble with
        # certain special characters.

        foreign = TestForeignKeyModel()
        foreign.save()

        for special_character in string.punctuation:
            unsaved_model = TestComplexModel(
                integer_field=123,
                string_field=special_character,
                json_field=dict(fun="run"),
                datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
                test_foreign=foreign,
            )
            bulk_insert_models([unsaved_model])

            saved_model = TestComplexModel.objects.get(string_field=special_character)
            self.assertIsNotNone(saved_model.id)
            for attr in ["integer_field", "string_field", "json_field", "test_foreign_id"]:
                self.assertEqual(getattr(saved_model, attr), getattr(unsaved_model, attr))
            self.assertEqual(saved_model.string_field, unsaved_model.string_field)

    def test_single_insert_new_with_pk(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        unsaved_model = TestComplexModel(
            id=10,
            integer_field=123,
            string_field="hello",
            json_field=dict(fun="run"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        bulk_insert_models([unsaved_model])

        saved_model = TestComplexModel.objects.get()
        self.assertEqual(saved_model.id, 10)
        for attr in ["id", "integer_field", "string_field", "json_field", "test_foreign_id"]:
            self.assertEqual(getattr(saved_model, attr), getattr(unsaved_model, attr))

    def test_pointfield_single_insert_new_with_pk(self):
        unsaved_model = TestGISModel(
            id=10,
            integer_field=123,
            location=Point(y=30, x=90),
        )
        bulk_insert_models([unsaved_model])

        saved_model = TestGISModel.objects.get()
        self.assertEqual(saved_model.id, 10)
        for attr in ["id", "integer_field", "location"]:
            self.assertEqual(getattr(saved_model, attr), getattr(unsaved_model, attr))

    def test_duplicate_insert_fails(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        saved_model = TestComplexModel.objects.create(
            integer_field=123,
            string_field="hello",
            json_field=dict(fun="run"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        with self.assertRaises(IntegrityError):
            bulk_insert_models([saved_model])

    def test_duplicate_insert_ignore_conflicts_success(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        saved_model = TestComplexModel.objects.create(
            integer_field=123,
            string_field="hello",
            json_field=dict(fun="run"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        self.assertEqual(TestComplexModel.objects.count(), 1)

        # This will throw an error without ignore_conflicts=True
        bulk_insert_models([saved_model], ignore_conflicts=True)

        # Check we still only have 1 record
        self.assertEqual(TestComplexModel.objects.count(), 1)

    def test_multiple_inserts(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        unsaved_model1 = TestComplexModel(
            integer_field=1,
            string_field="hello1",
            json_field=dict(fun="run1"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        unsaved_model2 = TestComplexModel(
            integer_field=2,
            string_field="hello2",
            json_field=dict(fun="run2"),
            datetime_field=datetime(2018, 2, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        unsaved_model3 = TestComplexModel(
            integer_field=3,
            string_field="hello3",
            json_field=dict(fun="run3"),
            datetime_field=datetime(2018, 3, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        unsaved_models = [unsaved_model1, unsaved_model2, unsaved_model3]
        bulk_insert_models(unsaved_models)

        unsaved_by_integer_field = {model.integer_field: model for model in unsaved_models}
        for saved_model in TestComplexModel.objects.all():
            self.assertIsNotNone(saved_model.id)
            for attr in ["integer_field", "string_field", "json_field", "test_foreign_id"]:
                self.assertEqual(
                    getattr(saved_model, attr), getattr(unsaved_by_integer_field[saved_model.integer_field], attr)
                )

    def test_return_models(self):
        foreign = TestForeignKeyModel()
        foreign.save()

        unsaved_model1 = TestComplexModel(
            integer_field=1,
            string_field="hello1",
            json_field=dict(fun="run1"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )
        unsaved_model2 = TestComplexModel(
            integer_field=2,
            string_field="hello2",
            json_field=dict(fun="run2"),
            datetime_field=datetime(2018, 2, 5, 3, 4, 5, tzinfo=timezone.utc),
            test_foreign=foreign,
        )

        unsaved_models = [unsaved_model1, unsaved_model2]

        # This may return models in any order
        saved_models = bulk_insert_models(unsaved_models, return_models=True)
        unsaved_by_integer_field = {model.integer_field: model for model in unsaved_models}
        for saved_model in saved_models:
            self.assertIsNotNone(saved_model.id)
            for attr in ["integer_field", "string_field", "json_field", "test_foreign_id"]:
                self.assertEqual(
                    getattr(saved_model, attr), getattr(unsaved_by_integer_field[saved_model.integer_field], attr)
                )

    def test_errors_when_mix_of_pk_and_not(self):
        unsaved_model_with_pk = TestComplexModel(
            id=1,
            integer_field=1,
            string_field="hello1",
            json_field=dict(fun="run1"),
            datetime_field=datetime(2018, 1, 5, 3, 4, 5, tzinfo=timezone.utc),
        )
        unsaved_model_without_pk = TestComplexModel(
            integer_field=2,
            string_field="hello2",
            json_field=dict(fun="run2"),
            datetime_field=datetime(2018, 2, 5, 3, 4, 5, tzinfo=timezone.utc),
        )

        with self.assertRaises(ValueError):
            bulk_insert_models([unsaved_model_with_pk, unsaved_model_without_pk])

    def test_errors_when_uploading_binary(self):
        unsaved_model1 = TestComplexModel(
            binary_field=b"hello2",
        )
        unsaved_model2 = TestComplexModel(
            binary_field=b"hello2",
        )

        with self.assertRaises(ValueError):
            bulk_insert_models([unsaved_model1, unsaved_model2])
