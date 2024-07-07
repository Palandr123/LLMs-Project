class Detector:
    """
    Base class for detecting objects.

    Attributes:
        object_lists (list[tuple[str, list[str | None]]]): A list of tuples containing
            object names and their corresponding attribute lists. None values in an attribute list
            represent primitive objects without attributes.
        primitive_count (dict[str, int]): A dictionary that stores the count of each primitive object.
        attribute_count (dict[str, int]): A dictionary that stores the count of each unique attribute
            combined with its corresponding object name.
        pred_primitive_count (dict[str, int]): A dictionary that stores the predicted count of each
            primitive object (initially 0, intended for future prediction functionality).
        pred_attribute_count (dict[str, int]): A dictionary that stores the predicted count of each
            unique attribute combined with its corresponding object name (initially 0, intended for
            future prediction functionality).
    """

    def __init__(self):
        self.object_lists: list[tuple[str, list[str | None]]] = []
        self.primitive_count: dict[str, int] = {}
        self.attribute_count: dict[str, int] = {}
        self.pred_primitive_count: dict[str, int] = {}
        self.pred_attribute_count: dict[str, int] = {}

    def register_objects(self, object_list: list[tuple[str, list[str | None]]]) -> None:
        """
        Registers objects and their attributes from the given object lists.

        Resets all internal data structures before processing the new object list.
        Then, iterates through the object list and updates the counts for:
            - Primitive objects (objects with no attributes)
            - Unique attribute combinations with their corresponding object names

        Args:
            object_list (list[tuple[str, list[str | None]]]): A list of tuples containing
                object names and their corresponding attribute lists. None values in an attribute list
                represent primitive objects without attributes.
        """
        # Reset class variables
        self.object_lists = object_list
        self.primitive_count: dict[str, int] = {}
        self.attribute_count: dict[str, int] = {}
        self.pred_primitive_count: dict[str, int] = {}
        self.pred_attribute_count: dict[str, int] = {}

        for name, attribute_list in object_list:
            self.pred_primitive_count[name] = 0
            for attribute in attribute_list:
                if attribute is not None:
                    self.attribute_count[f"{attribute} {name}"] = (
                        self.attribute_count.get(f"{attribute} {name}", 0) + 1
                    )
                    self.pred_attribute_count[f"{attribute} {name}"] = 0
                else:
                    self.primitive_count[name] = self.primitive_count.get(name, 0) + 1
                    self.pred_primitive_count[name] = 0
