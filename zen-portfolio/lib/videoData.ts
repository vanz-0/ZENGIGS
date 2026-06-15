export interface VideoEntry {
  id: string;          // filename without extension
  problem: string;     // Pain-point headline the viewer identifies with
  solution: string;    // One-line fix ZENGIGS delivers
  freeOffer: string;   // The free hook/offer pitched in the video
  category: VideoCategory;
}

export type VideoCategory =
  | "AI & Automation"
  | "CRM & Pipeline"
  | "Cold Outreach"
  | "Ads & Social"
  | "Web & App Dev"
  | "Data & Catalogs"
  | "Lead Generation";

export const videos: VideoEntry[] = [
  {
    id: "ECS_001",
    problem: "Struggling to get enough sales calls on the calendar?",
    solution: "We build systems that guarantee 20 booked appointments in 60 days.",
    freeOffer: "20 booked sales appointments in 60 days or you don't pay.",
    category: "Cold Outreach",
  },
  {
    id: "ECS_002",
    problem: "Website visitors bouncing before they ever speak to you?",
    solution: "We build live chat systems to capture leads in real-time.",
    freeOffer: "Free live chat system built for you. Only pay after your first 10 clients.",
    category: "Web & App Dev",
  },
  {
    id: "ECS_003",
    problem: "Sending out quotes but hearing crickets in return?",
    solution: "We build high-converting proposal templates that sell for you.",
    freeOffer: "Custom, high-converting proposal template built for you entirely for free.",
    category: "Cold Outreach",
  },
  {
    id: "ECS_004",
    problem: "Wondering why your competitors are ranking higher on Google?",
    solution: "We run a full SEO audit and fix hidden technical issues.",
    freeOffer: "Full SEO audit delivered to your inbox within 24 hours, completely free.",
    category: "Web & App Dev",
  },
  {
    id: "ECS_005",
    problem: "Pouring money into Google Ads with zero return?",
    solution: "We build Google Ads campaigns that guarantee qualified leads.",
    freeOffer: "50 qualified leads in 30 days or you don't pay a cent.",
    category: "Ads & Social",
  },
  {
    id: "ECS_006",
    problem: "Publishing blog posts that nobody actually reads?",
    solution: "We write SEO-optimized content that works for you 24/7.",
    freeOffer: "A completely free 500-word SEO blog post on any topic.",
    category: "Ads & Social",
  },
  {
    id: "ECS_007",
    problem: "Losing track of leads and watching deals slip through the cracks?",
    solution: "We build a world-class CRM customized to your industry.",
    freeOffer: "Custom CRM built for your industry at absolutely no cost.",
    category: "CRM & Pipeline",
  },
  {
    id: "ECS_008",
    problem: "Getting terrible open rates on your email campaigns?",
    solution: "We rewrite your emails to speak to pain points and convert better.",
    freeOffer: "We'll rewrite your last three email campaigns for free to boost conversions.",
    category: "Cold Outreach",
  },
  {
    id: "ECS_009",
    problem: "Posting on social media every day but not seeing any business growth?",
    solution: "We manage your social strategy to convert followers into customers.",
    freeOffer: "14 days of Instagram management completely free. No measurable growth = no invoice.",
    category: "Ads & Social",
  },
  {
    id: "ECS_010",
    problem: "Is your website acting like a leaky bucket for potential customers?",
    solution: "We redesign your site to communicate value in five seconds.",
    freeOffer: "Free homepage redesign mockup delivered in 72 hours. Only pay if you love it.",
    category: "Web & App Dev",
  },
  {
    id: "ECS_011",
    problem: "Dreading tax season because you always end up owing too much?",
    solution: "We organize your books to proactively save you money on deductions.",
    freeOffer: "One month of bookkeeping at no cost. We save you $2k in deductions, or it's free.",
    category: "AI & Automation",
  },
  {
    id: "ECS_012",
    problem: "Are your videos getting swiped past in the first five seconds?",
    solution: "We edit your raw footage into polished, attention-grabbing pieces.",
    freeOffer: "Send your latest raw video; we'll edit it ready-to-post, completely free.",
    category: "Ads & Social",
  },
  {
    id: "ECS_013",
    problem: "Finding it impossible to hire A-players for your open roles?",
    solution: "We pre-screen and filter candidates before they reach your desk.",
    freeOffer: "10 pre-screened candidates in 5 days. No fee unless you make a hire.",
    category: "AI & Automation",
  },
  {
    id: "ECS_014",
    problem: "Is your support inbox flooded with the exact same questions every day?",
    solution: "We build a custom AI chatbot that handles your top FAQs instantly.",
    freeOffer: "Custom AI chatbot for your top 20 FAQs. Don't pay unless it deflects 30% of tickets.",
    category: "AI & Automation",
  },
  {
    id: "ECS_015",
    problem: "Watching your sales team stumble on the goal line time after time?",
    solution: "We review sales calls and fix gaps in objection handling and structure.",
    freeOffer: "Full teardown of 3 sales calls with 5 specific fixes, completely free.",
    category: "CRM & Pipeline",
  },
  {
    id: "ECS_016",
    problem: "Are your paid ads getting expensive clicks but zero conversions?",
    solution: "We create tested ad variations that outperform your current creative.",
    freeOffer: "3 new creative variations for your best-performing ad, completely free.",
    category: "Ads & Social",
  },
  {
    id: "ECS_017",
    problem: "Struggling to fill seats for your seminars and webinars?",
    solution: "We refine your marketing hook and registration process to boost attendance.",
    freeOffer: "Free entry into our program to fulfill your 20 CME credit requirement.",
    category: "Ads & Social",
  },
  {
    id: "ECS_018",
    problem: "Trying to run a podcast but feeling overwhelmed by the technical work?",
    solution: "We handle professional audio production, SEO, and show notes.",
    freeOffer: "Full production (intro, outro, editing, show notes) for one episode at no cost.",
    category: "AI & Automation",
  },
  {
    id: "ECS_019",
    problem: "Are your sales reps wasting hours reaching out to dead email addresses?",
    solution: "We enrich your lead lists with verified contact information.",
    freeOffer: "Enrichment of your first 500 contacts with verified emails, phones, and LinkedIn, free.",
    category: "Lead Generation",
  },
  {
    id: "ECS_020",
    problem: "Is your landing page getting plenty of traffic but zero conversions?",
    solution: "We rewrite your headline and copy to drive immediate action.",
    freeOffer: "Free rewrite of your landing page headline and above-the-fold copy.",
    category: "Web & App Dev",
  },
  {
    id: "ECS_021",
    problem: "Are you spending hours every week on repetitive tasks?",
    solution: "We build automations connecting your tools to eliminate manual entry.",
    freeOffer: "One complete automation built at no cost. Must save you 5 hours/week.",
    category: "AI & Automation",
  },
  {
    id: "ECS_022",
    problem: "Do you feel like you're constantly losing deals to competitors?",
    solution: "We run a competitive analysis on pricing, positioning, and ad spend.",
    freeOffer: "Full competitive analysis of your top 5 competitors delivered in 48 hours, free.",
    category: "Data & Catalogs",
  },
  {
    id: "ECS_023",
    problem: "Have an amazing product but nobody actually knows who you are?",
    solution: "We pitch your story and secure features in relevant publications.",
    freeOffer: "Featured in 3 relevant publications in 60 days, or you don't pay.",
    category: "Cold Outreach",
  },
  {
    id: "ECS_024",
    problem: "Is your calendar empty because nobody wants to pick up the phone?",
    solution: "We cold call prospects on your behalf and book qualified meetings.",
    freeOffer: "We'll call 200 prospects and book qualified meetings. Only pay for shows.",
    category: "Cold Outreach",
  },
  {
    id: "ECS_025",
    problem: "Does your brand look amateurish compared to the premium prices you charge?",
    solution: "We build a full brand kit that builds trust with high-end clients.",
    freeOffer: "Full brand kit (logo, colors, typography, guidelines) built for free.",
    category: "Web & App Dev",
  },
  {
    id: "ECS_026",
    problem: "Are you still the best-kept secret in your industry?",
    solution: "We build your media authority by getting you featured in major publications.",
    freeOffer: "Featured in 3 relevant publications in 60 days, or you don't pay.",
    category: "Cold Outreach",
  },
];

export const categoryColors: Record<VideoCategory, string> = {
  "AI & Automation": "bg-purple-500/20 text-purple-300 border-purple-500/30",
  "CRM & Pipeline":  "bg-blue-500/20 text-blue-300 border-blue-500/30",
  "Cold Outreach":   "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
  "Ads & Social":    "bg-orange-500/20 text-orange-300 border-orange-500/30",
  "Web & App Dev":   "bg-green-500/20 text-green-300 border-green-500/30",
  "Data & Catalogs": "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  "Lead Generation": "bg-red-500/20 text-red-300 border-red-500/30",
};
