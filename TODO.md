# AI Trading Performance Optimization - TODO Tracker

## Original Issues Fixed ✅ (from previous TODO)

## New Performance Plan (Confirmed: Optimize button is slow - GA + RL)

**Goal**: Reduce \"🚀 Optimize & Run AI Trading\" from 10-30s to <3s.

### Steps:

- [x] Step 1: Optimize src/genetic_algorithm.py ✅
  - Reduced population_size=20, generations=20
  - Added 20% data sampling for fitness
  - Vectorized price extraction

- [x] Step 2: Optimize ui/ai_dashboard.py ✅
  - Added @st.cache_data for GA, RL train, sim
  - RL episodes=25
  - Cached market overview data
  - Added computing state + button disable

- [ ] Step 3: utils/data_loader.py cache tweak

- [ ] Step 4: Test full pipeline
  - streamlit run streamlit_app.py
  - Time before/after Optimize button

**Current Progress**: Starting Step 1.
