import sys, os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)


from pygls.server import LanguageServer
from pygls.lsp.types import (
    CompletionItem, 
    CompletionList, 
    CompletionOptions, 
    Hover, 
    MarkupContent,
    SignatureHelp, 
    SignatureInformation, 
    ParameterInformation,
    Diagnostic, 
    DiagnosticSeverity, 
    Range, 
    Position,
)
from pygls.lsp.methods import SIGNATURE_HELP, TEXT_DOCUMENT_DID_CHANGE, COMPLETION, HOVER, TEXT_DOCUMENT_DID_OPEN

from pydbml.ide.completion_engine import get_completions
from pydbml.core.engine import Engine
from pydbml.parser.parser import Parser

server = LanguageServer()

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source

    diagnostics = []

    try:
        parser = Parser(code)
        parser.parse()

    except Exception as e:
        token = getattr(e, "node", None)
        token = getattr(token, "token", None)

        if token:
            line = token.line - 1
            col = token.column - 1

            diagnostics.append(
                Diagnostic(
                    range=Range(
                        start=Position(line=line, character=col),
                        end=Position(line=line, character=col + 1),
                    ),
                    message=str(e),
                    severity=DiagnosticSeverity.Error,
                    source="pydbml",
                )
            )

    ls.publish_diagnostics(doc.uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source

    diagnostics = []

    try:
        parser = Parser(code)
        parser.parse()

    except Exception as e:
        # ✅ handle PyDBMLError
        token = getattr(e, "node", None)
        token = getattr(token, "token", None)

        if token:
            line = token.line - 1
            col = token.column - 1

            diagnostics.append(
                Diagnostic(
                    range=Range(
                        start=Position(line=line, character=col),
                        end=Position(line=line, character=col + 1),
                    ),
                    message=str(e),
                    severity=DiagnosticSeverity.Error,
                    source="pydbml",
                )
            )

    ls.publish_diagnostics(doc.uri, diagnostics)

# =========================================================
# ✅ COMPLETION
# =========================================================
@server.feature(COMPLETION, CompletionOptions(trigger_characters=["!", "."]))
def completions(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source
    pos = params.position

    offset = doc.offset_at_position(pos)

    engine = get_engine_for_code(code)
    result = get_completions(code, offset, evaluator=engine.evaluator)

    # ✅ NORMAL COMPLETIONS (list)
    if isinstance(result, list):
        items = []

        for item in result:
            # ✅ ONLY functions should add ()
            if item.startswith("!!"):
                items.append(
                    CompletionItem(
                        label=item,
                        insert_text=f"{item}($1)",
                        insert_text_format=2
                    )
                )
            else:
                # ✅ variables / methods → NO brackets
                items.append(
                    CompletionItem(
                        label=item,
                        insert_text=item
                    )
                )

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
@server.feature(HOVER)
def hover(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source
    pos = params.position

    offset = doc.offset_at_position(pos)

    engine = get_engine_for_code(code)
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

@server.feature( SIGNATURE_HELP)
def signature_help(ls, params):
    doc = ls.workspace.get_document(params.text_document.uri)

    code = doc.source
    pos = params.position
    offset = doc.offset_at_position(pos)

    engine = get_engine_for_code(code)
    result = get_completions(code, offset, evaluator=engine.evaluator)

    if isinstance(result, dict) and "params" in result:
        params_list = result.get("params", [])

        return SignatureHelp(
            signatures=[
                SignatureInformation(
                    label=f"{result['name']}({', '.join(params_list)})",
                    parameters=[ParameterInformation(label=p) for p in params_list],
                )
            ],
            active_signature=0,
            active_parameter=0
        )

    return None

def get_engine_for_code(code):
    e = Engine()
    try:
        e.execute(code)
    except:
        pass
    return e

# =========================================================
# ✅ START SERVER
# =========================================================
if __name__ == "__main__":
    server.start_io()