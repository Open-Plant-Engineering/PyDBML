const vscode = require('vscode');
const { LanguageClient } = require('vscode-languageclient/node');
const path = require('path');

let client;

function activate(context) {
    console.log("🚀 PyDBML Extension Activated");

    // ✅ USE YOUR CONDA PYTHON
    const pythonPath = "C:\\SKRepo\\OPE_DB_API\\ope-db-api-env\\python.exe";

    // ✅ ABSOLUTE PATH TO SERVER (CRITICAL FIX)
    const serverPath = path.resolve(
        __dirname,
        "..",
        "pydbml-lsp",
        "server.py"
    );

    console.log("✅ Server Path:", serverPath);

    const serverOptions = {
        command: pythonPath,   // ✅ FIXED
        args: [serverPath]     // ✅ FIXED
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

function deactivate() {
    if (!client) return undefined;
    return client.stop();
}

module.exports = {
    activate,
    deactivate
};