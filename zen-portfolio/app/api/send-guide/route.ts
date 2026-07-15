import { NextRequest, NextResponse } from 'next/server';

const FREEBIE_PDF_URL = 'https://zengigs.com/guides/0-to-100-selling-pdfs.pdf';
const FREEBIE_FILENAME = '0-to-100-Selling-PDFs.pdf';

export async function POST(req: NextRequest) {
  const { email } = await req.json();
  if (!email || typeof email !== 'string' || !email.includes('@')) {
    return NextResponse.json({ error: 'Valid email required' }, { status: 400 });
  }

  const brevoApiKey = process.env.BREVO_API_KEY;
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!brevoApiKey) {
    return NextResponse.json({ error: 'Brevo API key not configured' }, { status: 500 });
  }

  // 1. Store lead in Supabase (try anon key, fallback to service role)
  let leadStored = false;
  for (const key of [supabaseServiceKey, supabaseAnonKey].filter(Boolean)) {
    try {
      const res = await fetch(`${supabaseUrl}/rest/v1/leads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': key!,
          'Authorization': `Bearer ${key}`,
          'Prefer': 'resolution=ignore-duplicates',
        },
        body: JSON.stringify({ email, source: 'freebie_guide', status: 'new' }),
      });
      if (res.ok) {
        leadStored = true;
        break;
      }
    } catch (_) {
      // try next key
    }
  }
  console.log(leadStored ? `Lead stored: ${email}` : `Lead storage skipped for: ${email}`);

  // 2. Send email via Brevo with PDF attachment
  try {
    const response = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': brevoApiKey,
      },
      body: JSON.stringify({
        sender: { name: 'ZENGIGS', email: 'evans@zengigs.com' },
        to: [{ email }],
        subject: 'Your Free Guide: 0 to 100 — Selling PDFs',
        htmlContent: `
          <div style="font-family:Arial,sans-serif;max-width:560px;margin:0 auto;padding:24px;background:#111318;color:#fff;border-radius:12px">
            <h1 style="color:#e8b931;font-size:28px;margin:0 0 8px">Your free guide is here 👋</h1>
            <p style="color:#c9ced8;font-size:15px;line-height:1.6">
              You just downloaded a PDF that teaches you how to sell PDFs.
              The proof is in your hands — 10 stages, 0 to 100, zero fluff.
            </p>
            <p style="color:#c9ced8;font-size:13px">The guide is attached below. If you want the full series on Affiliate Marketing,
            Content Creation, Earning with AI, and Web Dev with AI — 
            <a href="https://zengigs.com/hub/services" style="color:#e8b931">grab the bundle here →</a>
            </p>
            <hr style="border-color:#333;margin:20px 0">
            <p style="color:#666;font-size:11px">ZENGIGS — Tech-Powered Virtual Assistant</p>
          </div>`,
        attachment: [
          { name: FREEBIE_FILENAME, url: FREEBIE_PDF_URL },
        ],
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      console.error('Brevo send failed:', err);
      return NextResponse.json({ error: 'Email delivery failed' }, { status: 502 });
    }

    return NextResponse.json({ success: true, lead_saved: leadStored });
  } catch (err) {
    console.error('Send guide error:', err);
    return NextResponse.json({ error: 'Internal error' }, { status: 500 });
  }
}