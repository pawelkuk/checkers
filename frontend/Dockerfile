# pull official base image
FROM node:13.12.0-alpine

# set working directory
WORKDIR /frontend

# install app dependencies
COPY package*.json ./

RUN npm install
# RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY . .
