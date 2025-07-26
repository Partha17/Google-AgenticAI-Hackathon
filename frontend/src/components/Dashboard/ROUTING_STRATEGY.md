# 🗂️ FinGenie Routing Strategy

## 📍 Route Structure

### **Main Dashboard Routes:**
```
/dashboard                    # Overview dashboard
├── /dashboard/overview       # Net worth & financial summary
├── /dashboard/portfolio      # Portfolio analysis & allocation
├── /dashboard/goals          # Goal tracking & planning
├── /dashboard/credit         # Credit score & loans
├── /dashboard/taxes          # Tax optimization
├── /dashboard/debt           # Debt payoff strategies
├── /dashboard/sips           # SIP analysis & optimization
├── /dashboard/subscriptions  # Subscription management
├── /dashboard/risk           # Risk assessment
├── /dashboard/liquidity      # Emergency fund & cash flow
└── /dashboard/planner        # Master financial planner
```

## 🎯 Component Organization

### **Dashboard Cards (Main Page):**
1. **Net Worth Card** → `/dashboard/overview`
2. **Portfolio Card** → `/dashboard/portfolio`
3. **Goals Card** → `/dashboard/goals`
4. **Credit Card** → `/dashboard/credit`
5. **Taxes Card** → `/dashboard/taxes`
6. **Debt Card** → `/dashboard/debt`
7. **SIPs Card** → `/dashboard/sips`
8. **Subscriptions Card** → `/dashboard/subscriptions`

### **Advanced Features (Separate Pages):**
- **Risk Manager** → `/dashboard/risk`
- **Liquidity Agent** → `/dashboard/liquidity`
- **Router Agent** → `/dashboard/planner`

## 🎨 UI Strategy

### **Main Dashboard:**
- **Grid layout** with 8 main cards
- **Quick metrics** on each card
- **Click to expand** functionality
- **Recent activity** sidebar

### **Individual Pages:**
- **Full-screen** detailed analysis
- **Multiple charts** and visualizations
- **Action buttons** for each feature
- **Breadcrumb navigation**

## 🔧 Implementation Priority

### **Phase 1 (Core):**
1. `/dashboard` - Main overview
2. `/dashboard/overview` - Net worth
3. `/dashboard/portfolio` - Portfolio analysis
4. `/dashboard/goals` - Goal tracking

### **Phase 2 (Financial Tools):**
1. `/dashboard/credit` - Credit management
2. `/dashboard/taxes` - Tax optimization
3. `/dashboard/debt` - Debt payoff
4. `/dashboard/sips` - SIP analysis

### **Phase 3 (Advanced):**
1. `/dashboard/subscriptions` - Subscription manager
2. `/dashboard/risk` - Risk assessment
3. `/dashboard/liquidity` - Cash flow
4. `/dashboard/planner` - Master planner