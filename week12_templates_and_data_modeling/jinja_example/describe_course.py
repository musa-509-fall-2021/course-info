from pathlib import Path
from jinja2 import Environment, FileSystemLoader

course1 = {
    'title': 'MUSA 509: Geospatial Cloud Computing',
    'is_virtual': False,
    'room': 'GSE 114 and virtually',
    'days': 'Monday and Wednesday',
    'instructor_name': 'Mjumbe Poe',
    'student_names': [
        'Carlos',
        'Sisun',
        'Marlana',
        'Olivia',
        'Ben',
        'Hui',
    ]
}

template_dir = Path(__file__).parent / 'templates'
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('index.html')
rendered = template.render(course=course1)

print(rendered)
