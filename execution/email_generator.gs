/**
 * ZENGIGS — Upwork Proposal Generator
 * Google Apps Script for Google Sheets
 *
 * HOW TO USE:
 * 1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1XhyQcGW4IDs5kzH7thoMRpPr_alEkxDEACV1A9KRtVE
 * 2. Go to Extensions → Apps Script
 * 3. Paste this entire script and click Save
 * 4. Refresh your Sheet — a new "ZENGIGS Tools" menu will appear
 * 5. Click "ZENGIGS Tools" → "Generate Proposals for Upwork Jobs"
 *
 * WHAT IT DOES:
 * - Reads every row in the "Upwork" sheet
 * - For each job, generates a personalized, human-sounding proposal
 * - Writes proposals to a new "Proposals" sheet, ready to copy-paste into Upwork
 */

// ─── CONFIG ──────────────────────────────────────────────────────────────────
const UPWORK_SHEET_NAME = "Upwork";
const PROPOSALS_SHEET_NAME = "Proposals";
const GMAPS_SHEET_NAME = "GMaps Leads";

// Your ZENGIGS services — what you can offer
const YOUR_SERVICES = `
ZENGIGS is a video editing & content production studio specializing in:
- Short-form social media content (TikToks, Reels, YouTube Shorts)
- Long-form YouTube video editing with jump cuts, captions, and motion graphics
- AI-powered auto-captioning and subtitle generation
- Color grading & audio enhancement
- Animated lower-thirds, intros, and outros
- Batch content repurposing (turn 1 long video into 10+ social clips)
- Content strategy for YouTube channels and social platforms
`;

// ─── MENU ─────────────────────────────────────────────────────────────────────
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🎬 ZENGIGS Tools')
    .addItem('Generate Proposals for Upwork Jobs', 'generateUpworkProposals')
    .addItem('Push GMaps Leads to Sheet', 'createGMapsSheet')
    .addItem('📊 Dashboard Summary', 'showDashboard')
    .addToUi();
}

// ─── UPWORK PROPOSAL GENERATOR ────────────────────────────────────────────────
function generateUpworkProposals() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  // Get Upwork sheet
  const upworkSheet = ss.getSheetByName(UPWORK_SHEET_NAME);
  if (!upworkSheet) {
    ui.alert('❌ No "Upwork" sheet found. Please push your Upwork data first.');
    return;
  }

  const data = upworkSheet.getDataRange().getValues();
  if (data.length < 2) {
    ui.alert('❌ No job data found in the Upwork sheet.');
    return;
  }

  // Get or create Proposals sheet
  let proposalsSheet = ss.getSheetByName(PROPOSALS_SHEET_NAME);
  if (proposalsSheet) {
    proposalsSheet.clear();
  } else {
    proposalsSheet = ss.insertSheet(PROPOSALS_SHEET_NAME);
  }

  // Headers
  const headers = [
    'Job Title', 'Job URL', 'Client Country', 'Budget',
    'Category', 'Skills Required', 'Proposal (Copy-Paste Ready)',
    'Subject Line', 'Status', 'Notes'
  ];
  proposalsSheet.appendRow(headers);

  // Style the header row
  const headerRange = proposalsSheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#1a1a2e');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setFontSize(11);

  // Parse header row from Upwork sheet
  const upworkHeaders = data[0];
  const colIndex = {};
  upworkHeaders.forEach((h, i) => { colIndex[h] = i; });

  let processed = 0;
  let skipped = 0;

  // Process each job
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const title = row[colIndex['Title']] || '';
    const url = row[colIndex['URL']] || '';
    const budget = row[colIndex['Budget']] || 'Not specified';
    const category = row[colIndex['Category']] || '';
    const skills = row[colIndex['Skills']] || '';
    const country = row[colIndex['Client Country']] || '';
    const totalSpent = row[colIndex['Client Total Spent']] || '0';
    const experienceLevel = row[colIndex['Experience Level']] || '';

    if (!title || !url) {
      skipped++;
      continue;
    }

    // Generate the proposal
    const proposal = buildProposal(title, category, skills, budget, country, experienceLevel, totalSpent);
    const subject = buildSubjectLine(title, category);

    proposalsSheet.appendRow([
      title,
      url,
      country,
      budget,
      category,
      skills,
      proposal,
      subject,
      'Ready',
      ''
    ]);
    processed++;
  }

  // Auto-resize columns
  proposalsSheet.autoResizeColumns(1, headers.length);
  proposalsSheet.setColumnWidth(7, 600); // Proposal column — wider
  proposalsSheet.setColumnWidth(8, 300); // Subject line

  // Freeze header row
  proposalsSheet.setFrozenRows(1);

  // Wrap text in proposal column
  proposalsSheet.getRange(2, 7, processed, 1).setWrap(true);

  ui.alert(`✅ Done! Generated ${processed} proposals.\n${skipped > 0 ? skipped + ' rows skipped (missing data).' : ''}\n\nCheck the "${PROPOSALS_SHEET_NAME}" tab!`);
}

// ─── PROPOSAL BUILDER ─────────────────────────────────────────────────────────
function buildProposal(title, category, skills, budget, country, experienceLevel, totalSpent) {
  const skillsList = skills ? skills.split(',').map(s => s.trim()).slice(0, 3) : [];

  // Determine which ZENGIGS service is most relevant
  let angle = '';
  let serviceHighlight = '';
  const titleLower = title.toLowerCase();
  const catLower = category.toLowerCase();
  const skillsLower = skills.toLowerCase();

  if (titleLower.includes('tiktok') || titleLower.includes('reel') || titleLower.includes('short') || skillsLower.includes('tiktok')) {
    angle = 'short-form social media';
    serviceHighlight = 'We specialize in TikToks, Reels, and YouTube Shorts — high-retention edits with captions, trending audio sync, and hooks that stop the scroll.';
  } else if (titleLower.includes('youtube') || catLower.includes('video') || skillsLower.includes('youtube')) {
    angle = 'YouTube content';
    serviceHighlight = 'We produce YouTube videos end-to-end: tight jump cuts, clean audio, color grading, animated lower-thirds, and chapter markers — all delivered on schedule.';
  } else if (titleLower.includes('caption') || skillsLower.includes('caption') || titleLower.includes('subtitle')) {
    angle = 'captioning & subtitles';
    serviceHighlight = 'Our AI-powered captioning workflow handles batch subtitle generation, accuracy review, and dynamic caption styling (word-by-word animations, custom fonts, brand colors).';
  } else if (titleLower.includes('motion') || skillsLower.includes('after effects') || skillsLower.includes('motion graphics')) {
    angle = 'motion graphics';
    serviceHighlight = 'We build custom motion graphics — animated intros, lower-thirds, logo reveals, and transitions — that make your brand look premium across every video.';
  } else if (titleLower.includes('ugc') || titleLower.includes('content creator')) {
    angle = 'content production';
    serviceHighlight = 'We handle the full post-production pipeline for UGC and branded content: editing, color, captions, and packaging into scroll-stopping short clips ready for Meta/TikTok ads.';
  } else if (catLower.includes('marketing') || skillsLower.includes('marketing')) {
    angle = 'video marketing';
    serviceHighlight = 'We turn raw footage into performance-driven video assets — ad creatives, social content, and long-form edits — built to convert, not just look good.';
  } else {
    angle = 'video editing & content production';
    serviceHighlight = 'We handle editing, color grading, captions, and motion graphics — delivering polished, publish-ready content on a reliable schedule.';
  }

  // Build opener based on client spend (warm vs cold signal)
  const spentNum = parseFloat(totalSpent) || 0;
  let opener = '';
  if (spentNum > 10000) {
    opener = `I can see you've worked with talented freelancers before and know what quality looks like — so I'll keep this direct.`;
  } else if (spentNum > 1000) {
    opener = `You've clearly invested in good content, and I respect that. Here's why we'd be a great fit for this project.`;
  } else {
    opener = `I came across your post and the project immediately caught my attention — it's exactly the kind of work we do best.`;
  }

  const proposal = `Hi,

${opener}

You're looking for ${angle} support, and this is our core focus at ZENGIGS. ${serviceHighlight}

${skillsList.length > 0 ? `I noticed you need skills in ${skillsList.join(', ')} — we work with these daily and have a streamlined workflow built around fast turnarounds without sacrificing quality.` : ''}

**What you can expect working with us:**
→ Clear communication from day one — no chasing for updates
→ First draft delivered within 48–72 hours (faster for urgent work)
→ Revisions until you're genuinely happy
→ Consistent quality, whether it's your 1st video or your 100th

We'd love to show you what we can do. If you want, share a sample of your raw footage or a reference edit — we can put together a quick test edit before you commit to anything.

Looking forward to talking,
Max
ZENGIGS Video Studio
—
Portfolio available on request`;

  return proposal;
}

// ─── SUBJECT LINE BUILDER ─────────────────────────────────────────────────────
function buildSubjectLine(title, category) {
  const titleLower = title.toLowerCase();

  if (titleLower.includes('tiktok') || titleLower.includes('reel') || titleLower.includes('short')) {
    return 'Fast, High-Retention Short-Form Edits — Let\'s Talk';
  } else if (titleLower.includes('youtube')) {
    return 'YouTube Editor Ready — Consistent Quality, Fast Turnaround';
  } else if (titleLower.includes('caption') || titleLower.includes('subtitle')) {
    return 'Batch Captioning Done Right — Accurate & On-Brand';
  } else if (titleLower.includes('motion') || titleLower.includes('animation')) {
    return 'Custom Motion Graphics That Make Your Brand Stand Out';
  } else if (titleLower.includes('ugc') || titleLower.includes('content creator')) {
    return 'UGC Editing Specialist — Ads-Ready in 48hrs';
  } else {
    return 'Video Editor for ' + title.substring(0, 40) + '... — Ready to Start';
  }
}

// ─── GMAPS LEADS SHEET CREATOR ────────────────────────────────────────────────
function createGMapsSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  let sheet = ss.getSheetByName(GMAPS_SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(GMAPS_SHEET_NAME);
    const headers = [
      'Business Name', 'Category', 'Phone', 'Email', 'Website',
      'Rating', 'Reviews', 'City', 'State', 'Google Maps URL',
      'Facebook', 'Instagram', 'LinkedIn', 'Email Status',
      'Outreach Sent?', 'Reply Received?', 'Notes'
    ];
    sheet.appendRow(headers);

    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground('#0f3460');
    headerRange.setFontColor('#ffffff');
    headerRange.setFontWeight('bold');
    headerRange.setFontSize(11);
    sheet.setFrozenRows(1);

    ui.alert('✅ "GMaps Leads" sheet created!\n\nRun the Google Maps pipeline from your terminal to populate it:\n\npython execution/gmaps_lead_pipeline.py --search "Video Editors in Austin TX" --limit 50 --sheet-url YOUR_SHEET_URL');
  } else {
    ui.alert('ℹ️ "GMaps Leads" sheet already exists.');
  }
}

// ─── DASHBOARD ────────────────────────────────────────────────────────────────
function showDashboard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  let summary = '📊 ZENGIGS Lead Dashboard\n\n';

  const sheets = [UPWORK_SHEET_NAME, PROPOSALS_SHEET_NAME, GMAPS_SHEET_NAME];
  sheets.forEach(name => {
    const sheet = ss.getSheetByName(name);
    if (sheet) {
      const rows = Math.max(0, sheet.getLastRow() - 1); // Subtract header
      summary += `✅ ${name}: ${rows} records\n`;
    } else {
      summary += `❌ ${name}: Not found\n`;
    }
  });

  summary += '\n💡 Use "Generate Proposals" to create copy-paste Upwork proposals from your scraped jobs.';
  ui.alert(summary);
}
