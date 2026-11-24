from django.http import HttpResponse

def page(title: str, content: str, status: int = 200) -> HttpResponse:
    """Временная функция для формирования HTML-каркаса (ПР5)."""
    bootstrap_css = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap_css}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Event Manager</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/events/">Мероприятия</a>
                <a class="nav-link" href="/registrations/">Регистрации</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""
    return HttpResponse(html, status=status)

def index(request):
    content = """
    <h1 class="display-4">Добро пожаловать в Event Manager</h1>
    <p class="lead">Система организации и учёта корпоративных мероприятий.</p>
    <a href="/events/" class="btn btn-primary me-2">Список мероприятий</a>
    <a href="/registrations/" class="btn btn-secondary">Список регистраций</a>
    """
    return page("Главная – Event Manager", content)

def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return page("404 – страница не найдена", content, status=404)