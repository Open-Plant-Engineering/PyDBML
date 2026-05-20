const vscode = require('vscode');
const { LanguageClient } = require('vscode-languageclient/node');

let client;

function activate(context) {

    const serverOptions = {
        command: "python",
        args: ["pydbml-lsp/server.py"]
    };

    const clientOptions = {
        documentSelector: [{ scheme: "file", language: "pydbml" }]
    };

    client = new LanguageClient(
        "pydbml-language-server",
        "PyDBML Language Server",
        serverOptions,
        clientOptions
    );

    client.start();
}

exports.activate = activate;