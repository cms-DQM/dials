import numpy as np
from onnxruntime import InferenceSession

from ...env import MODEL_REGISTRY_PATH


def predict(workspace_name: str, model_file: str, input_data: np.array) -> list[dict]:
    model_path = f"{MODEL_REGISTRY_PATH}/{workspace_name}/{model_file}"
    sess = InferenceSession(model_path)

    # Predict
    input_name = sess.get_inputs()[0].name
    result = sess.run(None, {input_name: input_data})

    return result
