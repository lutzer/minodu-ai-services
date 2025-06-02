import request from 'supertest';
import express from 'express';
import { setupApiRoutes } from '../src/routes/api';
import { RagService } from '../src/services/ragService';
import { describe, it, expect, beforeEach } from '@jest/globals';

describe('API Routes', () => {
    let app: express.Application;

    beforeEach(() => {
        app = express();
        app.use(express.json());
        setupApiRoutes(app);
    });

    it.skip('should stream response for a valid question from the cli', async () => {
        const question = "Hello";

        const webStream = await RagService.askQuestion(question);

        const reader = webStream.getReader();

        let result = ""
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            result += value
        }

        expect(result.length).toBeGreaterThan(0)
    }, 100000);

    it('should stream response for a valid question to the api/ask', async () => {
        const question = "Hello";
        const response = await request(app)
            .post('/api/ask')
            .send({ question })
            .set('Accept', 'text/event-stream');

        expect(response.status).toBe(200);
        expect(response.headers['content-type']).toMatch(/text\/event-stream/);
        
        const streamData = response.text;
        expect(streamData.length).toBeGreaterThan(0)
    }, 100000);
});
