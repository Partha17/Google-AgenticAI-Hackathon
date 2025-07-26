# Financial Dashboard - React Frontend

This document outlines the plan to replicate the enhanced Python-based financial dashboard in React. The new frontend will be a standalone application that communicates with the existing backend services, providing a more modern, interactive, and performant user experience.

## Tech Stack

- **Framework:** React (Next.js for server-side rendering and routing)
- **Styling:** Tailwind CSS for a utility-first approach to styling, with a modern design system
- **State Management:** Redux Toolkit for predictable state management, especially for handling complex data from multiple sources
- **Data Fetching:** React Query for efficient data fetching, caching, and synchronization with the backend
- **Charting:** Recharts for creating beautiful, interactive charts and graphs
- **Authentication:** NextAuth.js for seamless integration with Google Authentication

## Project Structure

The frontend will be organized into a clear, modular structure to ensure scalability and maintainability:

```
/dashboard/frontend
|-- /components       # Reusable UI components (buttons, cards, etc.)
|   |-- /Prompt       # Prompt component for user queries
|-- /features         # Feature-based modules (e.g., portfolio, risk-assessment)
|   |-- /portfolio
|   |   |-- Portfolio.js
|   |   |-- portfolioSlice.js
|-- /hooks            # Custom hooks for shared logic
|-- /lib              # Helper functions and utilities
|-- /pages            # Next.js pages for routing
|   |-- /api          # API routes for backend communication
|-- /public           # Static assets (images, fonts, etc.)
|-- /store            # Redux store configuration
|-- /styles           # Global styles and Tailwind CSS configuration
|-- /constants        # Shared constants (API endpoints, etc.)
```

## Component Breakdown

The dashboard will be broken down into the following key components:

- **Layout:** A main layout component that includes the sidebar, header, and content area.
- **Sidebar:** A navigation component with links to different sections of the dashboard.
- **Header:** A header component with user information, authentication status, and global actions.
- **Dashboard:** A central component that aggregates data from multiple sources and displays it in a unified view.
- **Charts:** A set of reusable chart components for displaying financial data (e.g., portfolio treemap, risk gauge).
- **Cards:** A collection of card components for displaying key metrics and insights.
- **Prompt:** A ChatGPT-like interface for users to submit queries and receive AI-powered responses.

## API Configuration

All API endpoints will be defined in a central configuration file (`/constants/api.js`) to ensure that they can be easily updated without changing the application code. This will make it simple to switch between different backend environments (e.g., development, staging, production).

## Development Plan

1. **Setup:** Initialize a new Next.js project with Tailwind CSS, Redux Toolkit, and other dependencies.
2. **Authentication:** Implement Google Authentication using NextAuth.js to secure the dashboard.
3. **API Layer:** Create a centralized API configuration and a set of helper functions for making requests to the backend.
4. **Prompt Component:** Build a reusable prompt component with a flexible interface for user queries.
5. **Dashboard:** Build the main dashboard layout and components, replicating the enhanced dashboard's design.
6. **Charting:** Develop a set of interactive chart components to visualize financial data.
7. **Deployment:** Deploy the React frontend to a modern hosting platform like Vercel or Netlify.

This plan provides a clear roadmap for creating a modern, performant, and scalable frontend for the financial dashboard, leveraging the best of the React ecosystem.
