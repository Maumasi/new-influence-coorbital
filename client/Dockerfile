# Build stage
FROM node:20 as build
WORKDIR /app
COPY package*.json ./
RUN npm run safe-install 
COPY . .
RUN npm run build

# Serve stage
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
