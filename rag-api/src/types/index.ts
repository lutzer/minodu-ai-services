export interface RagResponse {
    success: boolean;
    data?: any;
    error?: string;
}

export interface RagQuestion {
    question: string;
}

export interface RagDocument {
    filePath: string;
}