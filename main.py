import requests
import time

# --- إعدادات ألماني V5.1 ---
TOKEN = "8685967489:AAHa41vlBqA8iP7Xmm4Hasv1ttiUsk60Vrg"
CHAT_ID = "8376468924"
SYMBOL = "BTCUSDT"
TIMEFRAME = "15m"

def get_data():
    # سحب الأسعار من بينانس (Binance)
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={TIMEFRAME}&limit=100"
    res = requests.get(url).json()
    return res

def calculate_rsi(data, period=5):
    # حساب RSI-5 يدويًا بدقة ألماني
    closes = [float(shm[4]) for shm in data]
    diffs = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in diffs]
    losses = [-d if d < 0 else 0 for d in diffs]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0: return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1+rs))

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(url)

print("🚀 رادار ألماني V5.1 قيد التشغيل...")

last_candle_time = None

while True:
    try:
        data = get_data()
        current_candle_time = data[-1][0]
        
        # التأكد من إغلاق الشمعة
        if last_candle_time != current_candle_time:
            rsi_val = calculate_rsi(data)
            price = data[-1][4]
            
            if rsi_val > 50:
                message = f"🚀 إشارة ألماني (BTC)\n\n📈 النوع: إغلاق فوق RSI 50\n⏱ الفريم: 15 دقيقة\n🔢 قيمة RSI: {rsi_val:.2f}\n💰 السعر الحالي: {price}\n⚠️ تحذير: راقب توتر السوق!"
                send_alert(message)
                print(f"✅ تم إرسال التنبيه: RSI {rsi_val:.2f}")
            
            last_candle_time = current_candle_time
            
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(30) # فحص كل 30 ثانية
