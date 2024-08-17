import datetime
import decimal
import json


# The CustomJSONEncoder class extends the functionality of the JSONEncoder class in Python for custom
# JSON encoding.
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        The function converts datetime.date objects to ISO format and decimal.Decimal objects to float,
        while falling back to the default serialization method for other objects.
        
        :param obj: The `obj` parameter in the `default` method is the object that needs to be
        serialized into a JSON-serializable format. The method checks if the object is an instance of
        `datetime.date` or `decimal.Decimal` and converts it into a JSON-serializable format
        accordingly. If the
        :return: If the object is an instance of `datetime.date`, the `isoformat()` method of the object
        will be called and the result will be returned. If the object is an instance of
        `decimal.Decimal`, the object will be converted to a float and returned. If the object does not
        match any of these conditions, the `default` method of the superclass will be called to handle
        the object.
        """
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        
        return super().default(obj)
