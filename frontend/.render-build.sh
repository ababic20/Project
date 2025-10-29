#!/usr/bin/env bash
set -e

echo "⚙️ Installing dependencies..."
npm install

echo "🏗️ Building project..."
npm run build

echo "🔁 Creating _redirects for SPA routing..."
echo "/* /index.html 200" > dist/_redirects

echo "✅ Build complete!"
