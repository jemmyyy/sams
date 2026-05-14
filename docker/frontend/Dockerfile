FROM node:22-slim

WORKDIR /app/frontend

# Install global dependencies
RUN npm install -g @quasar/cli

# Copy all project files first to satisfy Quasar's strict validation
COPY frontend/ .

# Install local dependencies
RUN npm install

EXPOSE 8080

CMD ["quasar", "dev", "-m", "spa"]
