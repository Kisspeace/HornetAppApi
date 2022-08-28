class JsonLoadable:
    def load_from_dict(self, source: dict):
        """
        set properties from dictionary
        Args:
            source (dict): dictionary object
        """
        for name, value in self.__dict__.items():
            if name in source:
                if isinstance(value, JsonLoadable) and (source[name] is not None):
                    value.load_from_dict(source[name])
                else:
                    setattr(self, name, source[name])
