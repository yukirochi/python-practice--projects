import json
from deepface import DeepFace

objs: list[dict] = DeepFace.analyze(
  img_path = "img2.jpg", actions = ['age', 'gender', 'race', 'emotion']
)

print(json.dumps(objs, indent=2, default=str))