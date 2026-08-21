# SOVRA.NEXUS - Elite Cross-Platform Container
# Build Stage
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Stage (Air-gapped deployment image)
FROM python:3.11-slim

# Create a non-root user for security (The "Skull" boundary)
RUN useradd -m -r sovranexus && \
    mkdir -p /app && \
    chown -R sovranexus:sovranexus /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/sovranexus/.local
ENV PATH=/home/sovranexus/.local/bin:$PATH

# Copy Organism Code
COPY --chown=sovranexus:sovranexus nexus_agent_core.py .

# Switch to non-root
USER sovranexus

# Expose the isolated port
EXPOSE 8080

# Run the Triad Orchestrator
ENTRYPOINT ["python", "nexus_agent_core.py"]
