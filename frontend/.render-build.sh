#!/usr/bin/env bash
# Build Vite project
npm install
npm run build

# Ensure _redirects file exists in the dist folder (for React Router SPA)
echo "/* /index.html 200" > dist/_redirects
