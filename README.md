# rag_test

A RAG system that answers questions about cryptocurrency quotes from Kraken exchange using time-stamped documents and Google Gemini.

## What It Does

Answers analytical questions about cryptocurrency market data, such as:
- "What is the 7-day moving average change in the last month?"
- "What was the price at noon on January 15th?"
- "How did the price change between these two dates?"

The system retrieves relevant historical quotes and uses an LLM to perform calculations and analysis.

## How It Works

1. **Extract timestamps**: The LLM analyzes your question to identify relevant timestamps
2. **Find documents**: The system locates Kraken quote documents closest to those timestamps from a partitioned directory structure (\`year=*/month=*/day=*/*.json\`)
3. **Build context**: Retrieved quote documents are loaded and formatted with their timestamps
4. **Generate answer**: The LLM receives your question + quote data and generates a response with calculations
5. **Token monitoring**: Each step tracks token usage to stay under the 1M token limit

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Create \`secrets.yml\`:
```yaml
google_api_key: "YOUR_API_KEY_HERE"
```

## Usage

```bash
python -m src.runner --question "What is the 7-day moving average change in the last month?"
```

Options:
- `--config` - Config file path (default: `config/config.yml`)
- `--secrets` - Secrets file path (default: `secrets.yml`)
- `--question` - Your question about the crypto quotes

## Document Format

Kraken quote documents should be organized as:
```
documents/year=2024/month=01/day=15/20240115120000.json
```

They are JSON files with format:

```json
{
    "0GUSD": {
        "a": [
            "0.9780000",
            "409",
            "409.000"
        ],
        "b": [
            "0.9770000",
            "3583",
            "3583.000"
        ],
        ...
    },
    "1INCHUSD": {
        ...
    },
    ...
}
```
