// vscode-extension/extension.js
const vscode = require('vscode');
const axios = require('axios');

// API endpoint for the CodeCrafter backend
const API_ENDPOINT = 'http://localhost:8501';

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('CodeCrafter extension is now active!');

    // Register the generate code command
    let generateCodeDisposable = vscode.commands.registerCommand('codecrafter.generateCode', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        if (!text) {
            vscode.window.showInformationMessage('Please select some text to generate code');
            return;
        }

        vscode.window.showInformationMessage('Generating code...');

        try {
            const response = await axios.post(`${API_ENDPOINT}/generate-code`, {
                prompt: text,
                language: vscode.window.activeTextEditor.document.languageId
            });

            editor.edit(editBuilder => {
                editBuilder.insert(selection.end, '\n\n' + response.data.code);
            });

            vscode.window.showInformationMessage('Code generated successfully!');
        } catch (error) {
            vscode.window.showErrorMessage('Error generating code: ' + error.message);
        }
    });

    // Register the explain code command
    let explainCodeDisposable = vscode.commands.registerCommand('codecrafter.explainCode', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        if (!text) {
            vscode.window.showInformationMessage('Please select some code to explain');
            return;
        }

        vscode.window.showInformationMessage('Explaining code...');

        try {
            const response = await axios.post(`${API_ENDPOINT}/explain-code`, {
                code: text,
                language: vscode.window.activeTextEditor.document.languageId
            });

            // Show explanation in a new document
            const doc = await vscode.workspace.openTextDocument({ 
                content: response.data.explanation, 
                language: 'markdown' 
            });
            await vscode.window.showTextDocument(doc);

            vscode.window.showInformationMessage('Code explanation generated!');
        } catch (error) {
            vscode.window.showErrorMessage('Error explaining code: ' + error.message);
        }
    });

    context.subscriptions.push(generateCodeDisposable);
    context.subscriptions.push(explainCodeDisposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};