"""
Compatibility shim: patches missing langchain_community.chat_models.vertexai
module that ragas 0.4.x imports but was removed in langchain-community 0.4.x.
Must be imported before any ragas import.
"""
import sys
from types import ModuleType

try:
    from langchain_community.chat_models.vertexai import ChatVertexAI  # noqa: F401
except ImportError:
    try:
        from langchain_google_vertexai import ChatVertexAI as _ChatVertexAI  # type: ignore[import]
    except ImportError:
        _ChatVertexAI = None  # type: ignore[assignment]

    _stub = ModuleType("langchain_community.chat_models.vertexai")
    _stub.ChatVertexAI = _ChatVertexAI  # type: ignore[attr-defined]
    sys.modules["langchain_community.chat_models.vertexai"] = _stub

try:
    from langchain_community.llms.vertexai import VertexAI  # noqa: F401
except ImportError:
    try:
        from langchain_google_vertexai import VertexAI as _VertexAI  # type: ignore[import]
    except ImportError:
        _VertexAI = None  # type: ignore[assignment]

    _stub_llm = ModuleType("langchain_community.llms.vertexai")
    _stub_llm.VertexAI = _VertexAI  # type: ignore[attr-defined]
    sys.modules["langchain_community.llms.vertexai"] = _stub_llm
