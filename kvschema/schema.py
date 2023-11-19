from jsonschema import validate
import jsonschema

# JSON Schema
schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["created_at", "geom"],
  "properties": {
    "created_at": {
        "type": "number",
        "cast": "datetime",
        "description": "Unix timestamp"
    },
    "geom": {
        "type": "string",
        "cast": "geometry",
        "description": "Geometry"
    }
  }
}

# バリデーションするデータ
data = {"created_at": 0.00001, "geom": "POINT(0, 0)"}

# バリデーションの実行
validate(instance=data, schema=schema)
print(data)


class Caster:
    def specialize(self, value):
        """ある操作に特化した型に変換する"""
        if value is None:
            return None
        
        from datetime import datetime
        
        return datetime.fromtimestamp(value)
        

    def generalize(self, value):
        """ある型を一般的な表現に汎化する"""
        if value is None:
            return None
        
        from datetime import datetime
        
        return datetime.utcnow().timestamp()
    