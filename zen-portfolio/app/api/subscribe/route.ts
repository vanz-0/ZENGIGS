import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { email } = await request.json();

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 });
    }

    const apiKey = process.env.RESEND_API_KEY;

    if (!apiKey) {
      console.error('Missing RESEND_API_KEY in environment variables');
      return NextResponse.json({ error: 'Server configuration error' }, { status: 500 });
    }

    // Send the freebie email via Resend
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        from: 'ZENGIGS <onboarding@resend.dev>',
        to: [email],
        subject: '🚀 Your Free Growth Strategy Guide from ZENGIGS',
        html: `
          <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #0a0a0f; color: #e0e0e0; padding: 40px; border-radius: 16px;">
            <div style="text-align: center; margin-bottom: 32px;">
              <h1 style="font-size: 28px; margin: 0; color: #ffffff;">
                ZENGIGS<span style="color: #a855f7;">.</span>
              </h1>
              <p style="color: #888; font-size: 13px; margin-top: 4px;">Tech-Powered Virtual Assistant</p>
            </div>

            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 12px; padding: 32px; margin-bottom: 24px;">
              <h2 style="color: #a855f7; font-size: 22px; margin: 0 0 16px 0;">Welcome to the Growth Playbook 🎉</h2>
              <p style="line-height: 1.7; color: #ccc; margin: 0 0 20px 0;">
                Thanks for joining! You've just unlocked our proven strategies that have helped businesses 
                book 20+ sales appointments in 60 days, slash operational costs, and automate their most 
                time-consuming workflows.
              </p>
              <p style="line-height: 1.7; color: #ccc; margin: 0 0 24px 0;">
                Here's what you'll get in the coming days:
              </p>
              <ul style="color: #ccc; line-height: 2; padding-left: 20px; margin: 0 0 24px 0;">
                <li><strong style="color: #fff;">Day 1:</strong> The Cold Outreach Framework (guaranteed replies)</li>
                <li><strong style="color: #fff;">Day 3:</strong> AI Automation Blueprint (save 20+ hrs/week)</li>
                <li><strong style="color: #fff;">Day 5:</strong> CRM Pipeline Mastery (never lose a deal again)</li>
                <li><strong style="color: #fff;">Day 7:</strong> The Full Growth Stack (everything tied together)</li>
              </ul>
            </div>

            <div style="text-align: center; margin-bottom: 32px;">
              <a href="https://zengigs.com" 
                 style="display: inline-block; background: #a855f7; color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 10px; font-weight: bold; font-size: 15px;">
                Visit ZENGIGS →
              </a>
            </div>

            <div style="border-top: 1px solid #222; padding-top: 20px; text-align: center; color: #666; font-size: 12px;">
              <p>© ${new Date().getFullYear()} ZENGIGS. All rights reserved.</p>
              <p>You're receiving this because you signed up at zengigs.com</p>
            </div>
          </div>
        `,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Resend API Error:', errorData);
      return NextResponse.json({ error: 'Failed to send email. Please try again later.' }, { status: response.status });
    }

    return NextResponse.json({ message: 'Check your inbox! Your free guide is on the way 🚀' }, { status: 200 });

  } catch (error) {
    console.error('Subscription error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
