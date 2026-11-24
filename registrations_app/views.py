import os
from django.http import HttpResponse
from homepage.views import page
from storage import load_events, load_registrations

def registration_list(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_dict = load_events(os.path.join(base_dir, "data", "events.json"))
    registrations = load_registrations(os.path.join(base_dir, "data", "registrations.json"), events_dict)

    registrations_sorted = sorted(registrations, key=lambda r: r.event.date if hasattr(r.event, 'date') else str(r.event.get('date', '')))

    rows = "".join([
        f"<tr><td>{r.id if hasattr(r, 'id') else r.get('id')}</td>"
        f"<td>{r.employee_name if hasattr(r, 'employee_name') else r.get('employee_name')}</td>"
        f"<td>{r.event.title if hasattr(r.event, 'title') else r.event.get('title')}</td>"
        f"<td>{(r.event.date if hasattr(r.event, 'date') else r.event.get('date')).strftime('%d.%m.%Y') if hasattr(r.event.date if hasattr(r.event, 'date') else r.event.get('date'), 'strftime') else str(r.event.date if hasattr(r.event, 'date') else r.event.get('date'))}</td>"
        f"<td><a href='/registrations/{r.id if hasattr(r, 'id') else r.get('id')}/' class='btn btn-sm btn-primary'>Подробнее</a></td></tr>"
        for r in registrations_sorted
    ])

    content = f"""
    <h1>Список регистраций</h1>
    <p class="text-muted">Всего регистраций: {len(registrations_sorted)}</p>
    <table class="table table-striped table-hover">
        <thead class="table-dark"><tr><th>ID</th><th>Сотрудник</th><th>Мероприятие</th><th>Дата</th><th>Действия</th></tr></thead>
        <tbody>{rows if rows else '<tr><td colspan="5" class="text-center">Регистраций нет</td></tr>'}</tbody>
    </table>
    <a href="/" class="btn btn-secondary">← На главную</a>
    """
    return page("Регистрации – Event Manager", content)

def registration_detail(request, registration_id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    events_dict = load_events(os.path.join(base_dir, "data", "events.json"))
    registrations = load_registrations(os.path.join(base_dir, "data", "registrations.json"), events_dict)

    registration = next((r for r in registrations if (r.id if hasattr(r, 'id') else r.get('id')) == registration_id), None)

    if registration is None:
        return page("404 – Не найдено", "<h1 class='text-danger'>Регистрация не найдена</h1><a href='/registrations/' class='btn btn-secondary'>← Назад</a>", status=404)

    emp_name = registration.employee_name if hasattr(registration, 'employee_name') else registration.get('employee_name')
    ev_title = registration.event.title if hasattr(registration.event, 'title') else registration.event.get('title')
    ev_date = registration.event.date if hasattr(registration.event, 'date') else registration.event.get('date')
    ev_cap = registration.event.capacity if hasattr(registration.event, 'capacity') else registration.event.get('capacity')
    date_str = ev_date.strftime('%d.%m.%Y') if hasattr(ev_date, 'strftime') else str(ev_date)

    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">Регистрация сотрудника</h1>
            <p class="card-text"><strong>ID:</strong> {registration_id}</p>
            <p class="card-text"><strong>Сотрудник:</strong> {emp_name}</p>
            <p class="card-text"><strong>Мероприятие:</strong> {ev_title}</p>
            <p class="card-text"><strong>Дата:</strong> {date_str}</p>
            <p class="card-text"><strong>Вместимость:</strong> {ev_cap} чел.</p>
        </div>
    </div>
    <a href="/registrations/" class="btn btn-secondary mt-3">← К списку регистраций</a>
    """
    return page(f"Регистрация – {emp_name}", content)