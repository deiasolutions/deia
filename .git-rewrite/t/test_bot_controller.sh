#!/bin/bash
echo "🔥 FIRE DRILL: Bot Controller Production Test"
echo "=============================================="
echo ""

echo "1️⃣  Launch BOT-PROD-001..."
RESULT=$(curl -s -X POST http://127.0.0.1:8000/api/bot/launch -H "Content-Type: application/json" -d '{"bot_id":"BOT-PROD-001","adapter":"mock"}')
echo "   $RESULT"
sleep 2

echo ""
echo "2️⃣  Launch BOT-PROD-002..."
RESULT=$(curl -s -X POST http://127.0.0.1:8000/api/bot/launch -H "Content-Type: application/json" -d '{"bot_id":"BOT-PROD-002","adapter":"mock"}')
echo "   $RESULT"
sleep 2

echo ""
echo "3️⃣  List Active Bots..."
curl -s http://127.0.0.1:8000/api/bots | python -m json.tool
sleep 2

echo ""
echo "4️⃣  Get BOT-PROD-001 Status..."
curl -s http://127.0.0.1:8000/api/bot/BOT-PROD-001/status | python -m json.tool
sleep 2

echo ""
echo "5️⃣  Send Task to BOT-PROD-001..."
curl -s -X POST http://127.0.0.1:8000/api/bot/BOT-PROD-001/task -H "Content-Type: application/json" -d '{"command":"Deploy production update"}' | python -m json.tool
sleep 2

echo ""
echo "6️⃣  Send Task to BOT-PROD-002..."
curl -s -X POST http://127.0.0.1:8000/api/bot/BOT-PROD-002/task -H "Content-Type: application/json" -d '{"command":"Run system tests"}' | python -m json.tool
sleep 2

echo ""
echo "7️⃣  Stop BOT-PROD-002..."
curl -s -X POST http://127.0.0.1:8000/api/bot/stop/BOT-PROD-002
sleep 2

echo ""
echo "8️⃣  Final Bot List (should show only BOT-PROD-001)..."
curl -s http://127.0.0.1:8000/api/bots | python -m json.tool

echo ""
echo "✅ PRODUCTION TEST COMPLETE"
