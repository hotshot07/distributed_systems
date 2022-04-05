FROM node:16.14.2
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@5.0.0 -g
COPY . ./
EXPOSE 3000
CMD ["npm ","start"];