import { spawn } from 'child_process';
import config from '../config'

export class RagService {

    static async askQuestion(question: string): Promise<ReadableStream> {
        return new ReadableStream({
            start: (controller) => {
                const pythonProcess = spawn(config.venvPath, [
                    config.cliPath,
                    '--model', config.model,
                    '--question', question
                ]);


                pythonProcess.stdout.on('data', (data) => {
                    controller.enqueue(data.toString());
                });

                pythonProcess.stderr.on('data', (data) => {
                    controller.error(`Error: ${data}`);
                });

                pythonProcess.on('close', (code) => {
                    if (code !== 0) {
                        controller.error(`Process exited with code ${code}`);
                    }
                    controller.close();
                });
            }
        });
    }

    // static async addDocument(filePath: string): Promise<string> {
    //     return new Promise((resolve, reject) => {
    //         const pythonProcess = spawn(config.venvPath, [
    //             config.cliPath,
    //             '--add-doc', filePath
    //         ]);

    //         let output = '';

    //         pythonProcess.stdout.on('data', (data) => {
    //             output += data.toString();
    //         });

    //         pythonProcess.stderr.on('data', (data) => {
    //             console.error(`Error: ${data}`);
    //         });

    //         pythonProcess.on('close', (code) => {
    //             if (code === 0) {
    //                 resolve(output);
    //             } else {
    //                 reject(`Process exited with code ${code}`);
    //             }
    //         });
    //     });
    // }

    // static async listDocuments(): Promise<string> {
    //     return new Promise((resolve, reject) => {
    //         const pythonProcess = spawn(config.venvPath, [
    //             config.cliPath,
    //             '--list-docs'
    //         ]);

    //         let output = '';

    //         pythonProcess.stdout.on('data', (data) => {
    //             output += data.toString();
    //         });

    //         pythonProcess.stderr.on('data', (data) => {
    //             console.error(`Error: ${data}`);
    //         });

    //         pythonProcess.on('close', (code) => {
    //             if (code === 0) {
    //                 resolve(output);
    //             } else {
    //                 reject(`Process exited with code ${code}`);
    //             }
    //         });
    //     });
    // }
}