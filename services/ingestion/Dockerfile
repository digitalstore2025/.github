FROM node:20-alpine
WORKDIR /app
COPY package.json .
COPY services/ingestion/package.json services/ingestion/package.json
RUN npm install
COPY services/ingestion ./services/ingestion
WORKDIR /app/services/ingestion
RUN npm run build
CMD ["node", "dist/index.js"]
