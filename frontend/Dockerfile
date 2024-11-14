FROM public.ecr.aws/docker/library/node:21.2.0-alpine3.17
ENV HTTP_PROXY "http://10.158.100.2:8080/"
ENV HTTPS_PROXY "http://10.158.100.2:8080/"

# make the 'app' folder the current working directory
WORKDIR /app/

COPY package.json ./

RUN npm cache verify

# install project dependencies
#RUN npm install --legacy-peer-deps
RUN npm install

RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

#RUN chown -R node /app/node_modules
# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

EXPOSE 8002

CMD ["npm", "run", "serve"]
