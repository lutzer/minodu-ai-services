# RAG API

This project is a Node.js application that interfaces with the `rag-cli.py` script to provide a streaming API for Retrieval Augmented Generation (RAG) functionality.

## Project Structure

```
rag-api
├── src
│   ├── routes
│   │   └── api.ts        # API route definitions
│   ├── services
│   │   └── ragService.ts  # Service to call the rag-cli.py script
│   ├── types
│   │   └── index.ts       # Type definitions and interfaces
│   ├── config.ts          # Configuration settings
│   └── app.ts             # Entry point of the application
├── tests
│   └── api.test.ts        # Unit tests for API routes
├── package.json            # npm configuration file
├── tsconfig.json           # TypeScript configuration file
└── README.md               # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag-api
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the application:**
   ```bash
   npm start
   ```

4. **Access the API:**
   The API will be available at `http://localhost:3000/api`.

## Usage

- To call the RAG functionality, send a request to the `/api` endpoint with the necessary parameters.
- The response will be streamed back from the `rag-cli.py` script.

## Testing

To run the tests, use the following command:

```bash
npm test
```

This will execute the unit tests defined in `tests/api.test.ts`.

## License

This project is licensed under the MIT License.