import unittest
import datetime
from hydra import h

class TestHydra(unittest.TestCase):
    def test_string(self):
        string_validator = h.string()
        self.assertTrue(string_validator.is_valid("hello"))
        self.assertFalse(string_validator.is_valid(1))
        self.assertEqual(string_validator.get_error_message(1), "Expected string, but got int")

    def test_integer(self):
        integer_validator = h.integer()
        self.assertTrue(integer_validator.is_valid(1))
        self.assertFalse(integer_validator.is_valid("hello"))
        self.assertEqual(integer_validator.get_error_message("hello"), "Expected integer, but got str")
    
    def test_list(self):
        list_validator = h.list(h.string())
        self.assertTrue(list_validator.is_valid(["hello", "world"]))
        self.assertFalse(list_validator.is_valid(["hello", 1]))
        self.assertEqual(list_validator.get_error_message(["hello", 1]), "Expected string, but got int")


    def test_object_validator(self):
        schema = {
            "name": h.string(),
            "age": h.integer(),
        }
        object_validator = h.object(schema)

        # Test valid data
        data = {
            "name": "John",
            "age": 30,
        }
        self.assertTrue(object_validator.is_valid(data))

        # Test invalid data
        data = {
            "name": "John",
            "age": "30",
        }
        self.assertFalse(object_validator.is_valid(data))
        self.assertEqual(object_validator.get_error_message(data), "Expected integer, but got str")


    def test_deeply_nested_object_validator(self):
        schema = {
            "name": h.string(),
            "age": h.integer(),
            "friends": h.list(h.object({
                "name": h.string(),
                "age": h.integer(),
            }))
        }
        object_validator = h.object(schema)

        # Test valid data
        data = {
            "name": "John",
            "age": 30,
            "friends": [
                {
                    "name": "Jane",
                    "age": 25,
                },
                {
                    "name": "Jack",
                    "age": 28,
                },
            ]
        }
        self.assertTrue(object_validator.is_valid(data))

        # Test invalid data
        data = {
            "name": "John",
            "age": 30,
            "friends": [
                {
                    "name": "Jane",
                    "age": 25,
                },
                {
                    "name": "Jack",
                    "age": "28",
                },
            ]
        }
        self.assertFalse(object_validator.is_valid(data))
        self.assertEqual(object_validator.get_error_message(data), "Expected integer, but got str")

    def test_boolean(self):
        boolean_validator = h.boolean()
        self.assertTrue(boolean_validator.is_valid(True))
        self.assertTrue(boolean_validator.is_valid(False))
        self.assertFalse(boolean_validator.is_valid("hello"))
        self.assertEqual(boolean_validator.get_error_message("hello"), "Expected boolean, but got str")

    def test_number(self):
        number_validator = h.number()
        self.assertTrue(number_validator.is_valid(1))
        self.assertTrue(number_validator.is_valid(1.0))
        self.assertFalse(number_validator.is_valid("hello"))
        self.assertEqual(number_validator.get_error_message("hello"), "Expected number, but got str")
    
    def test_float(self):
        float_validator = h.float()
        self.assertTrue(float_validator.is_valid(1.0))
        self.assertFalse(float_validator.is_valid("hello"))
        self.assertEqual(float_validator.get_error_message("hello"), "Expected float, but got str")
    
    def test_any(self):
        any_validator = h.any()
        self.assertTrue(any_validator.is_valid(1))
        self.assertTrue(any_validator.is_valid("hello"))
        self.assertTrue(any_validator.is_valid(True))
        self.assertTrue(any_validator.is_valid(1.0))
        self.assertTrue(any_validator.is_valid([1, 2, 3]))
        self.assertTrue(any_validator.is_valid({"a": 1, "b": 2}))
        self.assertTrue(any_validator.is_valid(None))
    
    def test_none(self):
        none_validator = h.none()
        self.assertTrue(none_validator.is_valid(None))
        self.assertFalse(none_validator.is_valid(1))
        self.assertEqual(none_validator.get_error_message(1), "Expected None, but got int")

    def test_optional(self):
        optional_validator = h.object({
            "name": h.string().optional(),
            "age": h.integer()
        })
        self.assertTrue(optional_validator.is_valid({"age": 30}))
        self.assertTrue(optional_validator.is_valid({"name": "John", "age": 30}))
        self.assertFalse(optional_validator.is_valid({"name": 1, "age": 30}))
        self.assertEqual(optional_validator.get_error_message({"name": 1, "age": 30}), "Expected string, but got int")


    def test_date(self):
        date_validator = h.date()
        date = datetime.date(2020, 1, 1)
        self.assertTrue(date_validator.is_valid(date))
        self.assertTrue(date_validator.is_valid("2020-01-01"))
        self.assertFalse(date_validator.is_valid("hello"))
        self.assertEqual(date_validator.get_error_message("hello"), "Expected date, but got str")
    
    def test_datetime(self):
        datetime_validator = h.datetime()
        dt = datetime.datetime(2020, 1, 1, 12, 0, 0)
        self.assertTrue(datetime_validator.is_valid(dt))
        self.assertTrue(datetime_validator.is_valid("2020-01-01T12:00:00"))
        self.assertFalse(datetime_validator.is_valid("hello"))
        self.assertFalse(datetime_validator.is_valid(datetime.date(2020, 1, 1)))
        self.assertEqual(datetime_validator.get_error_message(datetime.date(2020, 1, 1)), "Expected datetime, but got date")
        self.assertEqual(datetime_validator.get_error_message("hello"), "Expected datetime, but got str")        

if __name__ == "__main__":
    unittest.main()
