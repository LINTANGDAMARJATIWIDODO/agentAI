/**
 * Vercel Serverless Function Entry Point for NEXUS AI ENTERPRISE
 */
const requestHandler = require('../server.js');

module.exports = (req, res) => {
  return requestHandler(req, res);
};
