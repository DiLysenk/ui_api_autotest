class Helper:

    @staticmethod
    def get_unique_entity(list_of_entity):
        unique = []
        for entity in list_of_entity:
            if entity not in unique:
                unique.append(entity)
        return unique

    @staticmethod
    def get_unique_in_column(list_of_entity):
        entity = Helper.get_unique_entity(list_of_entity)
        while " " in entity:
            entity.remove(" ")
        return entity

    @staticmethod
    def filter_in_column(value):
        if " " != value:
            return value

    @staticmethod
    def filter_for_pagination(value):
        if "..." != value.text:
            try:
                return value
            except ValueError:
                raise AssertionError("Проверить пагинацию, ожидалось число")

    @staticmethod
    def find_in_elements_by_text(list_of_elements, text):
        for element in list_of_elements:
            if element.text == str(text):
                return element