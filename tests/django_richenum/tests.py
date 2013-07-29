import MySQLdb
from django.db import models, connection
from django.core.exceptions import ValidationError
from django_nose import FastFixtureTestCase

from richenum import OrderedRichEnum, OrderedRichEnumValue

from django_richenum.models import EnumField as ModelEnumField  # NB, this is a *model* field


class ModelEnumFieldTestSuite(FastFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        class NumberEnum(OrderedRichEnum):
            ONE = OrderedRichEnumValue(1, 'one', 'uno')
            TWO = OrderedRichEnumValue(2, 'two', 'deux')

        class EnumFieldTestModel(models.Model):
            number = ModelEnumField(NumberEnum, default=NumberEnum.ONE)
            parent = models.ForeignKey('self', null=True)

            class Meta:
                managed = False

        cursor = connection.cursor()
        try:
            # Clean up leftovers from old test runs, if necessary
            cursor.execute('DROP TABLE IF EXISTS `utils_enumfieldtestmodel`;')
        except MySQLdb.Warning:
            # Raised if the table didn't exist
            pass
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE `utils_enumfieldtestmodel` (
                `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                `number` int(11), /* Test as though DB didn't forbid nulls */
                `parent_id` int(11)
            );""")

        cls.enum = NumberEnum
        cls.model = EnumFieldTestModel
        super(ModelEnumFieldTestSuite, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cursor = connection.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS `utils_livefieldtestmodel`;')
        except MySQLdb.Warning:
            # Raised if the table didn't exist
            pass
        cursor.close()
        super(ModelEnumFieldTestSuite, cls).tearDownClass()

    def test_inits_with_default(self):
        # Verify that we can supply a default value
        default_instance = self.model()
        self.assertEqual(default_instance.number, self.enum.ONE)
        self.assertTrue(isinstance(default_instance.number, OrderedRichEnumValue))

    def test_fetch_with_enum(self):
        # Support fetching with enum, not index
        m = self.model(number=self.enum.ONE)
        m.save()
        display_name = self.model.objects.get(number=self.enum.ONE).number.display_name
        self.assertEqual(display_name, 'uno')

    def test_joins_with_enum(self):
        # Also support joins
        first = self.model()
        first.save()
        second = self.model(number=self.enum.TWO, parent=first)
        second.save()
        num_children = self.model.objects.filter(parent__number=self.enum.ONE).count()
        self.assertEqual(num_children, 1)

    def test_allows_index(self):
        # Though it breaks abstraction, allow using index instead of enum
        m = self.model(number=1)
        m.save()
        self.assertEqual(m.number.display_name, 'uno')
        self.assertEqual(self.model.objects.filter(number=1).count(), 1)

    def test_allows_canonical(self):
        # Also allow using canonical name
        m = self.model(number='one')
        m.save()
        self.assertEqual(m.number.display_name, 'uno')
        self.assertEqual(self.model.objects.filter(number='one').count(), 1)

    def test_default_forbids_nulls(self):
        with self.assertRaises(ValidationError):
            null = self.model(number=None)
            null.save()

    def test_can_allow_nulls(self):
        # Create a duplicate of test class, but allow nulls
        class EnumFieldTestModelNull(models.Model):
            number = ModelEnumField(self.enum, default=self.enum.ONE, null=True)
            parent = models.ForeignKey('self', null=True)

            class Meta:
                db_table = 'utils_enumfieldtestmodel'
                managed = False

        null_instance = EnumFieldTestModelNull(number=None)
        null_instance.save()
        self.assertIsNone(null_instance.number)
