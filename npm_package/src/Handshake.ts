import jwt from 'jsonwebtoken';
import crypto from 'crypto';

/**
 * SOVRA Zero-Point Deep Lock (v18.0)
 * Enterprise Anti-Extraction Protocol
 */

export interface SovraPayload {
  origin: string;
  timestamp: number;
  nonce: string;
}

export function generateHandshake(): string {
  const secret = process.env.SOVRA_ZERO_POINT_SECRET;
  if (!secret) throw new Error("SOVRA_ZERO_POINT_SECRET is not defined in environment.");

  const payload: SovraPayload = {
    origin: "sovra_client",
    timestamp: Date.now(),
    nonce: crypto.randomBytes(16).toString('hex'), // Cryptographically secure nonce
  };

  // Sign with strict 5-second expiration
  return jwt.sign(payload, secret, { algorithm: 'HS256', expiresIn: '5s' });
}

export function validateHandshake(token: string): boolean {
  const secret = process.env.SOVRA_ZERO_POINT_SECRET;
  if (!secret) throw new Error("SOVRA_ZERO_POINT_SECRET is not defined in environment.");

  try {
    // Clock tolerance leeway of 2 seconds handled natively by verifying servers
    jwt.verify(token, secret, { algorithms: ['HS256'], clockTolerance: 2 });
    return true; 
  } catch (err) {
    return false; 
  }
}
