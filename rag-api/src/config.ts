import path from 'path';

const config = {
    venvPath: path.join(__dirname, "../../rag/.venv/bin/python"),
    cliPath : path.join(__dirname, "../../rag/src/rag.py"),
    language: "fr"
};

export default config;