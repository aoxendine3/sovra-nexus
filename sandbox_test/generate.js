const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const secret = "TEST_SECRET_KEY_12345";

function generate(expiresIn) {
  const payload = {
    origin: "sovra_sandbox",
    timestamp: Date.now(),
    nonce: crypto.randomBytes(16).toString('hex')
  };
  return jwt.sign(payload, secret, { algorithm: 'HS256', expiresIn });
}

console.log(JSON.stringify({
  valid: generate('5s'),
  expired: generate('-10s'), // Already expired
  replay: generate('5s')     // Will be sent twice
}));
