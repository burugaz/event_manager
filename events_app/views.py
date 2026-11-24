import os
from django.http import HttpResponse
from homepage.views import page
from storage import load_events

def event_list(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "events.json")
    events_dict = load_events(json_path)

    events = list(events_dict.values()) if isinstance(events_dict, dict) else events_dict
    events_sorted = sorted(events, key=lambda e: e.date if hasattr(e, 'date') else e.get('date', ''))

    rows = "".join([
        f"<tr><td>{e.id if hasattr(e, 'id') else e.get('id')}</td>"
        f"<td>{e.title if hasattr(e, 'title') else e.get('title')}</td>"
        f"<td>{(e.date if hasattr(e, 'date') else e.get('date')).strftime('%d.%m.%Y') if hasattr(e.date if hasattr(e, 'date') else e.get('date'), 'strftime') else str(e.date if hasattr(e, 'date') else e.get('date'))}</td>"
        f"<td>{e.capacity if hasattr(e, 'capacity') else e.get('capacity')}</td>"
        f"<td><a href='/events/{e.id if hasattr(e, 'id') else e.get('id')}/' class='btn btn-sm btn-primary'>Подробнее</a></td></tr>"
        for e in events_sorted
    ])

    content = f"""
    <h1>Список мероприятий</h1>
    <p class="text-muted">Всего мероприятий: {len(events_sorted)}</p>
    <table class="table table-striped table-hover">
        <thead class="table-dark"><tr><th>ID</th><th>Название</th><th>Дата</th><th>Вместимость</th><th>Действия</th></tr></thead>
        <tbody>{rows if rows else '<tr><td colspan="5" class="text-center">Мероприятий нет</td></tr>'}</tbody>
    </table>
    <a href="/" class="btn btn-secondary">← На главную</a>
    """
    return page("Мероприятия – Event Manager", content)

def event_detail(request, event_id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_dict = load_events(os.path.join(base_dir, "data", "events.json"))

    event = events_dict.get(event_id) if isinstance(events_dict, dict) else next((e for e in events_dict if (e.id if hasattr(e, 'id') else e.get('id')) == event_id), None)

    if event is None:
        return page("404 – Не найдено", "<h1 class='text-danger'>Мероприятие не найдено</h1><a href='/events/' class='btn btn-secondary'>← Назад</a>", status=404)

    title = event.title if hasattr(event, 'title') else event.get('title')
    event_date = event.date if hasattr(event, 'date') else event.get('date')
    capacity = event.capacity if hasattr(event, 'capacity') else event.get('capacity')
    date_str = event_date.strftime('%d.%m.%Y') if hasattr(event_date, 'strftime') else str(event_date)

    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">{title}</h1>
            <p class="card-text"><strong>ID:</strong> {event_id}</p>
            <p class="card-text"><strong>Дата:</strong> {date_str}</p>
            <p class="card-text"><strong>Вместимость:</strong> {capacity} человек</p>
        </div>
    </div>
    <a href="/events/" class="btn btn-secondary mt-3">← К списку мероприятий</a>
    """
    return page(title, content)