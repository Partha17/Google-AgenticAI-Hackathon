// frontend/src/pages/api/prompt.ts
import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { prompt } = req.body;
    // Process the prompt here
    res.status(200).json({ response: `You entered: ${prompt}` });
  } else {
    res.status(405).json({ message: 'Method Not Allowed' });
  }
}
