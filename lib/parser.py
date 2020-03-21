class Parser:
    _json: dict

    def __init__(self, json):
        self._json = json
        pass

    def _parse_headers(self):
        headers = self._json["headers"]

    @classmethod
    def from_json(cls, json):
        return cls(json)
