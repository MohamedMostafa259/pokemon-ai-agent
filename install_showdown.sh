#!/bin/bash
echo "Installing Local Pokemon Showdown Server..."
git clone https://github.com/smogon/pokemon-showdown.git server
cd server
npm install
cp config/config-example.js config/config.js
cd ..

echo "Installing Local Pokemon Showdown Client..."
git clone https://github.com/smogon/pokemon-showdown-client.git client
cd client
npm install
cp config/config-example.js config/config.js
# Adjust client config to point to local server
sed -i "s/exports.server = {id/exports.server = {id: 'localhost', host: 'localhost', port: 8000, httpport: 8000};\/\//" config/config.js
cd ..
echo "Done!"
