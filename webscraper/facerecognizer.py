from ast import List
from deepface import DeepFace

objs: List[dict] = DeepFace.analyze(
  img_path = "img4.jpg", actions = ['age', 'gender', 'race', 'emotion']
)