import { Router, Request, Response } from 'express';
import { RagService } from '../services/ragService'; // Assuming you have a service to handle RAG logic
import { Readable } from 'stream';

const router = Router();

export function setupApiRoutes(app: any) {
    app.use('/api', router);

    router.post('/ask', async (req: Request, res: Response) => {
        const question = req.body.question;

        if (!question) {
            return res.status(400).json({ error: 'Question is required' });
        }

        try {
            const webStream = await RagService.askQuestion(question);

            res.setHeader('Content-Type', 'text/event-stream');
            res.setHeader('Cache-Control', 'no-cache');
            res.setHeader('Connection', 'keep-alive');

            Readable.fromWeb(webStream).pipe(res);
        } catch (error) {
            console.error('Error:', error);
            res.status(500).json({ error: 'Internal server error' });
        }

        // callRagCli(question, (data: string) => {
        //     res.write(`data: ${data}\n\n`);
        // }).then(() => {
        //     res.end();
        // }).catch((error: Error) => {
        //     res.status(500).json({ error: error.message });
        // });
    });
}