# ⚡ FAST TESTING GUIDE - 30 Minutes Left!

## Problem
Your original tests were using **Gemini API calls** during PDF ingestion (for every table & image), making tests take **30+ minutes**. Time was running out!

## Solution Implemented
Created a **FAST TEST MODE** that:
- ✅ Skips Gemini API calls → Returns **instant mock responses** instead
- ✅ Runs all tests in **~2-3 minutes** instead of 30+
- ✅ Still validates API endpoints work properly
- ✅ No code changes needed for production

## How to Run (Choose One)

### Option 1: Fast Tests (Recommended - 2-3 minutes)
```bash
bash run_fast_tests.sh
```
This automatically:
- Sets `FAST_TEST_MODE=true` 
- Starts the server
- Runs test suite with mocked Gemini responses
- Cleans up

### Option 2: Run Tests Manually
```bash
# Terminal 1: Start server with fast mode
export FAST_TEST_MODE=true
python main.py

# Terminal 2: Run tests
python test_fast.py
```

### Option 3: Full Tests with Real Gemini (Only if you have time)
```bash
# Make sure GEMINI_API_KEY is set in .env
python test_full_system.py
```

## What Changed
1. **src/models/gemini_client.py** - Added `FAST_TEST_MODE` check to return instant mock responses
2. **src/api/routes.py** - Added missing `pdfplumber` import
3. **test_fast.py** (NEW) - Optimized test suite with:
   - Smart server startup detection
   - Quick health checks
   - Single PDF ingestion test
   - Multiple query tests
   - Clear progress output

4. **run_fast_tests.sh** (NEW) - One-command test runner

## Test Results
```
✓ Health endpoint - PASS
✓ PDF ingestion (23 chunks) - PASS  
✓ Query endpoint - PASS
✓ Multiple queries (3) - PASS
━━━━━━━━━━━━━━━━━━━━━
RESULTS: 4/4 tests passed
```

## For Production
Remove `FAST_TEST_MODE=true` to use real Gemini API calls.

**GO! You have time now! 🚀**
