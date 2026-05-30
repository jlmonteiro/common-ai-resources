FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

COPY resources/knowledge-bases/ /data/

ENV KB_PATH=/data
ENV EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

# Pre-download the embedding model at build time
RUN python -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5')"

ENTRYPOINT ["python", "-m", "common_ai.mcp_server"]
