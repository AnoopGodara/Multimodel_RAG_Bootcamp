#!/bin/bash
# Quick test runner - skips Gemini API calls for speed

echo "==============================================="
echo "STARTING FAST TEST (No Gemini API Calls)"
echo "==============================================="
echo ""

# Activate venv if available
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi

# Set fast test mode (skips Gemini API)
export FAST_TEST_MODE=true
echo "✓ Fast test mode: ENABLED (Gemini calls will be mocked)"
echo ""

# Start the server in background
echo "[STEP 1/2] Starting FastAPI server..."
python main.py > /tmp/server.log 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"
sleep 3

# Run tests
echo ""
echo "[STEP 2/2] Running fast test suite..."
python test_fast.py
TEST_RESULT=$?

# Cleanup
echo ""
echo "Stopping server (PID: $SERVER_PID)..."
kill $SERVER_PID 2>/dev/null || true
sleep 1

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ ALL TESTS PASSED!"
else
    echo "✗ Some tests failed. Check output above."
fi

exit $TEST_RESULT
