# ----------------------------
# Stage 1: Build
# ----------------------------
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

# Copy dependency files first
COPY package*.json ./

# Install all deps (including dev, needed for build)
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the NestJS app (tsc via nest cli or your build script)
RUN npm run build


# ----------------------------
# Stage 2: Production
# ----------------------------
FROM node:20-alpine AS production

WORKDIR /usr/src/app

# Copy package.json first
COPY package*.json ./

# Install only production deps
RUN npm install --omit=dev

# Copy built app from builder stage
COPY --from=builder /usr/src/app/dist ./dist

# Expose port
EXPOSE 3000

# Start the app
CMD ["node", "dist/main.js"]
