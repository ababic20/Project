#!/usr/bin/env bash
set -e

echo "⚙️ Installing dependencies..."
npm install

echo "🏗️ Building project..."
npm run build

echo "🔁 Forcing _redirects for SPA routing..."
# Napravi _redirects i kopiraj ga unutar dist
echo "/* /index.html 200" > _redirects
cp _redirects dist/_redirects

echo "✅ Build complete and _redirects copied!"
