import base64
import json
import mimetypes

from django.conf import settings

AI_PROMPT = """Ты анализируешь рукописный чертёж комнаты или квартиры с указанными размерами.
Твоя задача — максимально точно прочитать цифры и извлечь размеры каждого помещения.

Правила:
- Читай цифры очень внимательно: 3, 4, 5, 6, 7, 8, 9 легко спутать в рукописи — смотри на форму каждой цифры.
- Если размеры указаны в сантиметрах (например, 510 или 424) — переведи в метры (510 см = 5.10 м, 424 см = 4.24 м).
- Если размеры указаны в метрах с точкой (например, 5.10 или 4.24) — оставь как есть.
- Если на чертеже несколько помещений — извлеки все.
- Если на чертеже одно помещение — верни массив из одного элемента.
- Если не удаётся распознать размеры — верни пустой массив.

Верни ТОЛЬКО валидный JSON без лишнего текста, пояснений или markdown:
{"rooms": [{"name": "Комната 1", "width": 5.10, "length": 4.24}, ...]}"""


def detect_fabric_size(width: float, length: float) -> str:
    """Определяет ширину полотна по меньшей стороне комнаты."""
    short_side = min(float(width), float(length))
    if short_side <= 3.6:
        return 'short'
    elif short_side <= 5.0:
        return 'wide'
    else:
        return 'the widest'


def _get_media_type(image_file) -> str:
    """Определяет MIME-тип изображения."""
    name = getattr(image_file, 'name', '')
    mime, _ = mimetypes.guess_type(name)
    if mime in ('image/jpeg', 'image/png', 'image/gif', 'image/webp'):
        return mime
    return 'image/jpeg'


def _clean_json(text: str) -> str:
    """Убирает markdown-обёртку вокруг JSON если модель её добавила."""
    import re
    # Убираем ```json ... ``` или ``` ... ```
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    # Если ответ пустой — возвращаем заглушку
    if not text:
        return '{"rooms": []}'
    return text


def recognize_with_claude(image_bytes: bytes, media_type: str) -> list:
    """Распознаёт комнаты через Claude 3.5 Sonnet."""
    import anthropic

    api_key = settings.ANTHROPIC_API_KEY
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY не задан в настройках.")

    client = anthropic.Anthropic(api_key=api_key)
    b64 = base64.standard_b64encode(image_bytes).decode('utf-8')

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": b64,
                    }
                },
                {
                    "type": "text",
                    "text": AI_PROMPT,
                }
            ]
        }]
    )

    text = message.content[0].text.strip()
    text = _clean_json(text)
    data = json.loads(text)
    return data.get("rooms", [])


def recognize_with_gpt4o(image_bytes: bytes, media_type: str) -> list:
    """Распознаёт комнаты через GPT-4o."""
    from openai import OpenAI

    api_key = settings.OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY не задан в настройках.")

    client = OpenAI(api_key=api_key)
    b64 = base64.b64encode(image_bytes).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": AI_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{media_type};base64,{b64}"}
                }
            ]
        }]
    )

    text = response.choices[0].message.content.strip()
    text = _clean_json(text)
    data = json.loads(text)
    return data.get("rooms", [])


def recognize_rooms(image_file, provider: str) -> list:
    """
    Основная функция распознавания.
    provider: 'claude' или 'gpt4o'
    Возвращает список словарей:
    [{'name': 'Комната 1', 'width': 4.2, 'length': 3.1, 'fabric_size': 'wide', 'ceiling_type': 'white mat'}, ...]
    """
    image_bytes = image_file.read()
    media_type = _get_media_type(image_file)

    if provider == 'claude':
        rooms = recognize_with_claude(image_bytes, media_type)
    elif provider == 'gpt4o':
        rooms = recognize_with_gpt4o(image_bytes, media_type)
    else:
        raise ValueError(f"Неизвестный провайдер: {provider}")

    result = []
    for i, room in enumerate(rooms):
        try:
            width = float(room.get('width', 0))
            length = float(room.get('length', 0))
        except (TypeError, ValueError):
            continue

        if width <= 0 or length <= 0:
            continue

        result.append({
            'name': room.get('name', f'Комната {i + 1}'),
            'width': round(width, 2),
            'length': round(length, 2),
            'fabric_size': detect_fabric_size(width, length),
            'ceiling_type': 'white mat',
        })

    return result
