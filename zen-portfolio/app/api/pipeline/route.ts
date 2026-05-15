import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { action, query, location, mode } = body;

    if (!action) {
      return NextResponse.json({ error: 'Action is required' }, { status: 400 });
    }

    // Determine the root of the ZENGIGS project (one level up from zen-portfolio)
    const rootDir = path.resolve(process.cwd(), '..');
    const scriptPath = path.join(rootDir, 'execution', 'pipeline_orchestrator.py');
    
    // Command arguments
    const args = ['--action', action];
    if (query) args.push('--query', query);
    if (location) args.push('--location', location);
    if (mode) args.push('--mode', mode);

    console.log(`Executing: python ${scriptPath} ${args.join(' ')}`);

    // We run this asynchronously. We don't want to block the request for minutes.
    const pythonProcess = spawn('python', [scriptPath, ...args], {
      cwd: rootDir,
      env: { ...process.env }
    });

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    // For a real production app, we would use a task queue or WebSockets.
    // Here, we'll return a 202 Accepted and let the user know it's running.
    return NextResponse.json({ 
      message: 'Pipeline started successfully', 
      script: 'pipeline_orchestrator.py',
      params: { action, query, location, mode }
    }, { status: 202 });

  } catch (error: any) {
    console.error('Pipeline Trigger Error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
