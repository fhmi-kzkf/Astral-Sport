"""
Gemini AI Concierge service — handles communication with Google Gemini API.
Includes mock fallback when API key is not configured.
"""

import json
from django.conf import settings

# Try to import google generativeai
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


# System prompt for the AI concierge
SYSTEM_PROMPT = """Kamu adalah "Astral", asisten AI untuk Astral Sport — platform penyewaan sepeda premium.

Panduan:
1. Bantu pelanggan memilih sepeda yang tepat berdasarkan:
   - Jenis rute (aspal, off-road, atau campuran)
   - Durasi sewa yang diinginkan
   - Level pengalaman bersepeda
   - Budget yang tersedia

2. Bisa menjawab FAQ teknis tentang sepeda (ukuran frame, jenis rem, gear system, dll)

3. Berikan estimasi kalori terbakar dan penghematan emisi CO2

4. Selalu ramah, profesional, dan ringkas. Gunakan emoji secukupnya.

5. Jika ditanya hal di luar topik sepeda/olahraga, arahkan kembali ke topik utama dengan sopan.

6. Rekomendasikan untuk menghubungi via WhatsApp untuk proses booking.

Katalog Sepeda:
- Road Bike: Untuk aspal, ringan (8-9kg), cocok kecepatan tinggi. Rp 50.000/jam.
- Mountain Bike: Untuk off-road, suspensi kuat, ban lebar. Rp 45.000/jam.
- Gravel Bike: Campuran aspal & tanah, serbaguna. Rp 55.000/jam.
- City Bike: Santai di kota, nyaman, keranjang depan. Rp 35.000/jam.
- E-Bike: Motor listrik assist, cocok pemula. Rp 75.000/jam.
- Folding Bike: Lipat, mudah dibawa, urban commute. Rp 40.000/jam.
"""


def get_ai_response(user_message, chat_history=None):
    """
    Get response from Gemini AI or mock fallback.

    Args:
        user_message: The user's message string
        chat_history: List of previous messages for context

    Returns:
        str: AI response text
    """
    api_key = settings.GOOGLE_API_KEY

    # Use real Gemini API if available
    if api_key and HAS_GENAI:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=SYSTEM_PROMPT
            )

            # Build conversation history
            history = []
            if chat_history:
                for msg in chat_history:
                    role = 'user' if msg['role'] == 'user' else 'model'
                    history.append({'role': role, 'parts': [msg['content']]})

            chat = model.start_chat(history=history)
            response = chat.send_message(user_message)
            return response.text

        except Exception as e:
            return f"Maaf, terjadi gangguan pada sistem AI. Silakan hubungi kami via WhatsApp untuk bantuan langsung. 🙏"

    # Mock fallback responses
    return _get_mock_response(user_message)


def _get_mock_response(message):
    """Provide intelligent mock responses when Gemini API is not available."""
    message_lower = message.lower()

    if any(word in message_lower for word in ['halo', 'hai', 'hi', 'hello', 'hey']):
        return (
            "Halo! 👋 Selamat datang di Astral Sport!\n\n"
            "Saya Astral, asisten virtual yang siap membantu Anda memilih sepeda yang tepat. "
            "Anda bisa bertanya tentang:\n\n"
            "🚴 Rekomendasi sepeda berdasarkan rute\n"
            "💰 Info harga sewa\n"
            "📊 Estimasi kalori & CO2 saved\n"
            "🔧 Spesifikasi teknis sepeda\n\n"
            "Apa yang bisa saya bantu hari ini?"
        )

    if any(word in message_lower for word in ['road', 'aspal', 'jalan', 'kecepatan', 'cepat']):
        return (
            "🏎️ Untuk rute aspal, saya rekomendasikan **Road Bike** kami!\n\n"
            "**Spesifikasi:**\n"
            "• Berat: 8.5 kg (super ringan)\n"
            "• Frame: Carbon Fiber\n"
            "• Gear: Shimano 105 22-Speed\n"
            "• Ban: 700x25c (aero)\n\n"
            "**Harga:** Rp 50.000/jam | Rp 300.000/hari\n\n"
            "Cocok untuk: Cycling enthusiast yang mengejar kecepatan & performa. "
            "Mau langsung booking? Klik tombol 'Sewa Sekarang' di halaman katalog! 🚀"
        )

    if any(word in message_lower for word in ['mountain', 'gunung', 'offroad', 'off-road', 'tanah', 'trail']):
        return (
            "🏔️ Untuk off-road/trail, pilihan terbaik adalah **Mountain Bike** kami!\n\n"
            "**Spesifikasi:**\n"
            "• Berat: 12.5 kg\n"
            "• Frame: Aluminium Alloy\n"
            "• Suspensi: Front Fork 120mm travel\n"
            "• Ban: 29x2.25\" (grip maksimal)\n"
            "• Rem: Hydraulic Disc Brake\n\n"
            "**Harga:** Rp 45.000/jam | Rp 280.000/hari\n\n"
            "Siap menaklukkan medan apa pun! 💪"
        )

    if any(word in message_lower for word in ['harga', 'biaya', 'tarif', 'murah', 'mahal', 'price']):
        return (
            "💰 **Daftar Harga Sewa Sepeda:**\n\n"
            "| Tipe | Per Jam | Per Hari |\n"
            "|------|---------|----------|\n"
            "| City Bike | Rp 35.000 | Rp 200.000 |\n"
            "| Folding Bike | Rp 40.000 | Rp 240.000 |\n"
            "| Mountain Bike | Rp 45.000 | Rp 280.000 |\n"
            "| Road Bike | Rp 50.000 | Rp 300.000 |\n"
            "| Gravel Bike | Rp 55.000 | Rp 320.000 |\n"
            "| E-Bike | Rp 75.000 | Rp 450.000 |\n\n"
            "Semua harga sudah termasuk helm & bottle cage! 🎉"
        )

    if any(word in message_lower for word in ['kalori', 'calorie', 'bakar', 'olahraga', 'fitness']):
        return (
            "📊 **Estimasi Kalori Terbakar (per 10 km):**\n\n"
            "🚴 Road Bike: ~320 kkal\n"
            "🚵 Mountain Bike: ~450 kkal\n"
            "🚲 City Bike: ~280 kkal\n"
            "⚡ E-Bike: ~200 kkal\n\n"
            "Bersepeda 30 menit setara dengan membakar 1 piring nasi goreng! 🍛\n"
            "Plus, setiap 10 km bersepeda menghemat ~2.1 kg emisi CO2 vs berkendara mobil 🌿"
        )

    if any(word in message_lower for word in ['gravel', 'campuran', 'serbaguna', 'versatile']):
        return (
            "🌄 **Gravel Bike** adalah pilihan paling serbaguna!\n\n"
            "Bisa di aspal maupun tanah — sempurna untuk eksplorasi.\n\n"
            "**Spesifikasi:**\n"
            "• Berat: 9.8 kg\n"
            "• Frame: Chromoly Steel\n"
            "• Ban: 700x40c (lebar tapi tetap aero)\n"
            "• Gear: Shimano GRX 20-Speed\n\n"
            "**Harga:** Rp 55.000/jam | Rp 320.000/hari\n\n"
            "Best seller kami untuk weekend adventure! 🏆"
        )

    # Default response
    return (
        "Terima kasih atas pertanyaannya! 😊\n\n"
        "Saya bisa membantu Anda dengan:\n"
        "• 🚴 Rekomendasi sepeda (sebut jenis rute Anda)\n"
        "• 💰 Informasi harga sewa\n"
        "• 📊 Estimasi kalori & penghematan CO2\n"
        "• 🔧 Spesifikasi teknis sepeda\n\n"
        "Atau langsung hubungi tim kami via WhatsApp untuk booking cepat! 📱"
    )
