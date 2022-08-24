class JsonLoadable:
    def LoadFromDict(self, D):
        for name, value in self.__dict__.items():
            if name in D:
                if isinstance(value, JsonLoadable):
                    value.LoadFromDict(D[name])
                else:     
                    setattr(self, name, D[name])
