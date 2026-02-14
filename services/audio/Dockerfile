FROM node:20-alpine
WORKDIR /app
COPY package.json .
COPY services/audio/package.json services/audio/package.json
RUN npm install
COPY services/audio ./services/audio
WORKDIR /app/services/audio
RUN npm run build
CMD ["node", "dist/index.js"]
