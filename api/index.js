/**
 * Vercel Serverless Function Catch-All Entry Point
 */
const requestHandler = require('../server.js');

module.exports = (req, res) => {
  // Normalize req.url in Vercel environment if needed
  const realUrl = req.headers['x-forwarded-url'] || req.headers['x-matched-path'] || req.url;
  if (realUrl && realUrl.startsWith('/api')) {
    req.url = realUrl;
  }
  return requestHandler(req, res);
};
