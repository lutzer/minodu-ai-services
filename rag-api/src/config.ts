import path from 'path';

const config = {
    venvPath: path.join(__dirname, "../../rag/.venv/bin/python"),
    cliPath : path.join(__dirname, "../../rag/rag-cli.py"),
    model: "llama3.2:1b",
    language: "fr"
};

export default config;