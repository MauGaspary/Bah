import os
from typing import Optional

from fastapi import Depends, Request


def get_embedding_model(request: Request) -> Optional[object]:
    if os.getenv("TESTING", "false").lower() == "true":

        class MockEmbeddingModel:
            def encode(self, texts, **kwargs):
                import numpy as np

                dim = int(os.getenv("MODEL_DIMENSIONS", "768"))
                if isinstance(texts, str):
                    return np.random.rand(dim).tolist()
                return [np.random.rand(dim).tolist() for _ in texts]

        return MockEmbeddingModel()

    return request.app.state.embedding_model
