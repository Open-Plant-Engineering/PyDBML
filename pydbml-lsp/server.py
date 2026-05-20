from pygls.server import LanguageServer
from pygls.lsp.types import CompletionItem, CompletionList, CompletionOptions
from pygls.lsp.types import Hover, MarkupContent
from pygls.lsp.methods import TEXT_DOCUMENT_COMPLETION, TEXT_DOCUMENT_HOVER

from pydbml.ide.completion_engine import get_completions
from pydbml.core.engine import Engine


server = LanguageServer("pydbml-lsp", "v0.1")

engine = Engine()


# =========================================================
# ✅ COMPLETION
# =========================================================
@server.feature(TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=["!", "."]))
def completions(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source
    pos = params.position

    offset = doc.offset_at_position(pos)

    result = get_completions(code, offset, evaluator=engine.evaluator)

    # ✅ NORMAL COMPLETIONS (list)
    if isinstance(result, list):
        items = [CompletionItem(label=item) for item in result]
        return CompletionList(is_incomplete=False, items=items)

    # ✅ SIGNATURE → show params
    if isinstance(result, dict) and "params" in result:
        items = [
            CompletionItem(label=result["name"]),
        ]
        return CompletionList(is_incomplete=False, items=items)

    return CompletionList(is_incomplete=False, items=[])


# =========================================================
# ✅ HOVER
# =========================================================
@server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source
    pos = params.position

    offset = doc.offset_at_position(pos)

    result = get_completions(code, offset, evaluator=engine.evaluator)

    if isinstance(result, dict):
        text = ""

        if result.get("kind") == "variable":
            text = f"{result['name']} : {result['type']}"

        elif result.get("kind") == "method":
            params = ", ".join(result.get("params", []))
            text = f"{result['name']}({params})"

        if text:
            return Hover(
                contents=MarkupContent(kind="plaintext", value=text)
            )

    return None


# =========================================================
# ✅ START SERVER
# =========================================================
if __name__ == "__main__":
    server.start_io()