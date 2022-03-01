
#build the container
FROM node:16 As build
#set working dir
WORKDIR /app
#copy the packages files
COPY package*.json .
#run the install of packages
RUN npm install
#copy all files
COPY ./ ./
#build the react app
RUN npm run build
#step to 
From nginx:latest
COPY ./nginx/nginx.conf etc/nginx/nginx.conf
copy --from=build /app/build /usr/share/nginx/html
