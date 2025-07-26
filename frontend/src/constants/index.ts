// API Endpoints
export const API_ENDPOINTS = {
  CHAT: '/api/chat',
  DASHBOARD: '/api/dashboard',
  PORTFOLIO: '/api/portfolio',
  GOALS: '/api/goals',
  CREDIT: '/api/credit',
  TAXES: '/api/taxes',
  DEBT: '/api/debt',
  SIPS: '/api/sips',
  SUBSCRIPTIONS: '/api/subscriptions',
  RISK: '/api/risk',
  LIQUIDITY: '/api/liquidity',
  PLANNER: '/api/planner',
} as const;

// Dashboard Routes
export const DASHBOARD_ROUTES = {
  OVERVIEW: '/dashboard',
  PORTFOLIO: '/dashboard/portfolio',
  GOALS: '/dashboard/goals',
  CREDIT: '/dashboard/credit',
  TAXES: '/dashboard/taxes',
  DEBT: '/dashboard/debt',
  SIPS: '/dashboard/sips',
  SUBSCRIPTIONS: '/dashboard/subscriptions',
  RISK: '/dashboard/risk',
  LIQUIDITY: '/dashboard/liquidity',
  PLANNER: '/dashboard/planner',
} as const;

// Navigation Items
export const NAVIGATION_ITEMS = [
  { name: 'Overview', href: DASHBOARD_ROUTES.OVERVIEW, icon: 'Home' },
  { name: 'Portfolio', href: DASHBOARD_ROUTES.PORTFOLIO, icon: 'TrendingUp' },
  { name: 'Goals', href: DASHBOARD_ROUTES.GOALS, icon: 'Target' },
  { name: 'Credit', href: DASHBOARD_ROUTES.CREDIT, icon: 'CreditCard' },
  { name: 'Taxes', href: DASHBOARD_ROUTES.TAXES, icon: 'Calculator' },
  { name: 'Debt', href: DASHBOARD_ROUTES.DEBT, icon: 'DollarSign' },
  { name: 'SIPs', href: DASHBOARD_ROUTES.SIPS, icon: 'BarChart3' },
  { name: 'Subscriptions', href: DASHBOARD_ROUTES.SUBSCRIPTIONS, icon: 'Settings' },
  { name: 'Risk Manager', href: DASHBOARD_ROUTES.RISK, icon: 'Shield' },
  { name: 'Liquidity', href: DASHBOARD_ROUTES.LIQUIDITY, icon: 'PiggyBank' },
  { name: 'Planner', href: DASHBOARD_ROUTES.PLANNER, icon: 'Calendar' },
] as const;

// Quick Suggestions for Chat
export const CHAT_SUGGESTIONS = [
  "What's my current portfolio risk level?",
  "Show me investment opportunities",
  "Analyze my spending patterns",
  "Help me optimize my taxes",
  "Create a retirement plan",
  "Review my debt payoff strategy"
] as const;

// Colors
export const COLORS = {
  PRIMARY: '#3B82F6',
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  DANGER: '#EF4444',
  PURPLE: '#8B5CF6',
  CYAN: '#06B6D4',
  GRAY: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827',
  }
} as const;

// Breakpoints
export const BREAKPOINTS = {
  MOBILE: 768,
  TABLET: 1024,
  DESKTOP: 1280,
} as const;

// Animation Durations
export const ANIMATION_DURATIONS = {
  FAST: 150,
  NORMAL: 300,
  SLOW: 500,
} as const;

// Z-Index Values
export const Z_INDEX = {
  DROPDOWN: 10,
  STICKY: 20,
  FIXED: 30,
  MODAL: 40,
  TOOLTIP: 50,
  OVERLAY: 60,
} as const;