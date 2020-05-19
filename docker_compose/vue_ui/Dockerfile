FROM node:lts-alpine

# make the 'app' folder the current working directory
WORKDIR /vue_ui

ADD . .

# add `/vue_ui/node_modules/.bin` to $PATH
ENV PATH /vue_ui/node_modules/.bin:$PATH

# # install simple http server for serving static content
# RUN npm install -g http-server

# # copy both 'package.json' and 'package-lock.json' (if available)
# COPY package*.json ./

# install project dependencies
RUN npm install

# # copy project files and folders to the current working directory (i.e. 'app' folder)
# COPY . .

# # build app for production with minification
# RUN npm run build

# EXPOSE 8000
# CMD [ "http-server", "-p  8050", "dist" ]