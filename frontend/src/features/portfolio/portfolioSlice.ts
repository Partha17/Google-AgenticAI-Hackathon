// frontend/src/features/portfolio/portfolioSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PortfolioState {
  // Define your state properties here
}

const initialState: PortfolioState = {
  // Initialize your state here
};

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    // Define your reducers here
  },
});

export const { /* export your actions here */ } = portfolioSlice.actions;

export default portfolioSlice.reducer;
