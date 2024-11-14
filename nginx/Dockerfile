# dev
FROM public.ecr.aws/docker/library/node:16.13.0-alpine3.11 as build-stage
ENV HTTP_PROXY "http://10.158.100.2:8080/"
ENV HTTPS_PROXY "http://10.158.100.2:8080/"

WORKDIR /app/
COPY frontend/package.json /app/
RUN npm cache verify
RUN npm install
COPY frontend /app/
RUN npm run build

# prod
FROM public.ecr.aws/docker/library/nginx:1.23.1-alpine as production-stage
COPY nginx/prod.conf /etc/nginx/nginx.conf
COPY backend/static /usr/src/app/static/
COPY --from=build-stage /app/dist /dist/
EXPOSE 8001
CMD ["nginx", "-g", "daemon off;"]
