from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --------------------------------------------------------------------------
# TEMPLATE HTML PRINCIPAL
# --------------------------------------------------------------------------
TREATMENT_PLAN_TEMPLATE = '''
<!DOCTYPE html>
<html dir="{{ text_direction }}" lang="{{ lang }}">
<head>
<meta charset="UTF-8">
<title>{{ page_title }}</title>

<style>
/* ====================== ADMIN RESET ====================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: {{ font_family }};
    background: white;
    color: #000;
    padding: 35px;
    font-size: 14pt;
    line-height: 1.7;
}

/* ====================== ADMIN HEADER ====================== */
.header {
    border: 2px solid #000;
    padding: 20px;
    margin-bottom: 35px;
    text-align: center;
}

.header h1 {
    font-size: 22pt;
    font-weight: bold;
    margin-bottom: 5px;
}

.date {
    font-size: 12pt;
    font-style: italic;
}

/* ====================== SECTIONS ====================== */
.section {
    border: 1px solid #000;
    padding: 20px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 18pt;
    font-weight: bold;
    margin-bottom: 15px;
    text-align: {{ text_align }};
    padding-bottom: 5px;
    border-bottom: 2px solid #000;
}

/* ====================== INFO GRID ====================== */
.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px 20px;
}

.info-label {
    font-weight: bold;
    font-size: 14pt;
    text-align: {{ text_align }};
}

.info-value {
    border: 1px solid #777;
    padding: 8px;
    font-size: 14pt;
    text-align: {{ text_align }};
}

/* ====================== GROUP TABLES ====================== */
.group {
    margin-bottom: 25px;
}

.group-title {
    font-weight: bold;
    font-size: 16pt;
    padding: 10px;
    background: #e5e5e5;
    border: 1px solid #000;
    text-align: {{ text_align }};
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 13pt;
}

th, td {
    border: 1px solid #000;
    padding: 10px;
    text-align: {{ text_align }};
}

/* ====================== SOLUTIONS ====================== */
.solution-block {
    border: 1px solid #000;
    padding: 15px;
    margin-bottom: 25px;
    background: #f7f7f7;
}

.solution-block-title {
    font-weight: bold;
    font-size: 16pt;
    margin-bottom: 12px;
    border-bottom: 1px solid #000;
    padding-bottom: 6px;
}

/* solution items */
.solution-point {
    margin-bottom: 10px;
    display: flex;
    flex-direction: {{ flex_direction }};
}

.point-number {
    font-weight: bold;
    margin-{{ bullet_margin_side }}: 10px;
}

/* ====================== FOOTER ====================== */
.footer {
    text-align: center;
    font-size: 11pt;
    margin-top: 40px;
    padding-top: 15px;
    color: #444;
    border-top: 1px solid #000;
}

/* ====================== PRINT ====================== */
@media print {
    @page { size: A4 portrait; margin: 15mm; }
    .print-button { display: none !important; }
    body { padding: 0; }
    .section { page-break-inside: avoid; }
}
</style>
</head>
<body>

<button class="print-button" onclick="window.print()" 
style="padding:8px 15px; margin-bottom:20px; font-size:12pt;">
    {{ print_button_text }}
</button>

<div class="header">
    <h1>{{ main_title }}</h1>
    <div class="date">{{ report_date_label }} : {{ date }}</div>
</div>

<div class="section">
    <h2 class="section-title">{{ basic_info_title }}</h2>
    <div class="info-grid">
        {% for label, value in info_items %}
            <div class="info-label">{{ label }}</div>
            <div class="info-value">{{ value }}</div>
        {% endfor %}
    </div>
</div>

<div class="section">
    <h2 class="section-title">{{ classification_title }}</h2>

    {% for key, group_title in group_titles.items() %}
        <div class="group">
            <div class="group-title">{{ group_title }}</div>

            <table>
                <thead>
                    <tr>
                        <th>{{ student_name_label }}</th>
                        <th>{{ group_label }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups[key] %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>{{ group_title }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endfor %}
</div>

<div class="section">
    <h2 class="section-title">{{ analysis_title }}</h2>

    {% for block_title, items in solution_blocks.items() %}
    <div class="solution-block">
        <div class="solution-block-title">{{ block_title }}</div>

        {% if items %}
            {% for item in items %}
            <div class="solution-point">
                <span class="point-number">{{ loop.index }}.</span>
                <span>{{ item }}</span>
            </div>
            {% endfor %}
        {% else %}
            <p>{{ no_items_text }}</p>
        {% endif %}
    </div>
    {% endfor %}
</div>

<div class="footer">
    {{ footer_text }} – © {{ date[:4] }}
</div>

</body>
</html>

'''

# --------------------------------------------------------------------------
# UTILITAIRES
# --------------------------------------------------------------------------

def clean_text(text):
    """Nettoie un bloc de texte et le transforme en liste sans doublons."""
    if not text:
        return []

    unwanted = ['ـ', '●', '★']
    for u in unwanted:
        text = text.replace(u, '')

    return [line.strip() for line in text.split('\n') if line.strip()]


def unify_solutions(data):
    """Fusionne toutes les solutions/problèmes en éliminant les doublons."""
    solutions = set()
    problems = set()

    blocks = (
        data['solutions'].get('default', {}),
        *data['solutions'].get('userProposals', []),
        *data['solutions'].get('globalProposals', [])
    )

    for block in blocks:
        for item in clean_text(block.get('solution', '')):
            solutions.add(item)
        for item in clean_text(block.get('probleme', '')):
            problems.add(item)

    return {
        'solution': sorted(solutions),
        'probleme': sorted(problems)
    }


def get_language_context(data):
    """Renvoie les paramètres linguistiques adaptés selon la matière."""
    french_subjects = {
        "expression orale et récitation", "lecture", "production écrite",
        "écriture", "dictée", "langue", "langue française", "français"
    }

    matiere = data.get('matiereName', '').lower()

    is_fr = any(key in matiere for key in french_subjects)

    if is_fr:
        return {
            'lang': 'fr',
            'text_direction': 'ltr',
            'text_align': 'left',
            'border_side': 'left',
            'section_after_position': 'left',
            'flex_direction': 'row',
            'bullet_margin_side': 'right',
            'print_button_side': 'right',
            'font_family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",

            # Textes
            'page_title': "Plan de traitement et origine de l'erreur",
            'main_title': "Rapport du Plan de Traitement et Origine de l'Erreur",
            'print_button_text': "Imprimer le rapport",
            'report_date_label': "Date du rapport",
            'basic_info_title': "Informations de base",
            'classification_title': "Classification des apprenants",
            'analysis_title': "Analyse des erreurs et propositions",
            'solutions_title': "Solutions proposées",
            'problems_title': "Analyse des erreurs",
            'group_titles': {
                'treatment': "Groupe de traitement",
                'support': "Groupe de soutien",
                'excellence': "Groupe d'excellence"
            },
            'student_name_label': "Nom de l'élève",
            'group_label': "Groupe",
            'no_items_text': "Aucune donnée disponible",
            'footer_text': "Rapport généré automatiquement"
        }

    # Arabic
    return {
        'lang': 'ar',
        'text_direction': 'rtl',
        'text_align': 'right',
        'border_side': 'right',
        'section_after_position': 'right',
        'flex_direction': 'row-reverse',
        'bullet_margin_side': 'left',
        'print_button_side': 'left',
        'font_family': "'Amiri', 'Traditional Arabic', serif",

        # Textes
        'page_title': "خطة العلاج وأصل الخطأ",
        'main_title': "تقرير خطة العلاج وأصل الخطأ",
        'print_button_text': "طباعة التقرير",
        'report_date_label': "تاريخ التقرير",
        'basic_info_title': "المعلومات الأساسية",
        'classification_title': "تصنيف المتعلمين",
        'analysis_title': "تحليل الأخطاء واقتراح العلاج",
        'solutions_title': "الحلول المقترحة",
        'problems_title': "تحليل الأخطاء",
        'group_titles': {
            'treatment': "مجموعة العلاج",
            'support': "مجموعة الدعم",
            'excellence': "مجموعة التميز"
        },
        'student_name_label': "اسم التلميذ(ة)",
        'group_label': "المجموعة",
        'no_items_text': "لا توجد بيانات متاحة",
        'footer_text': "تم إنشاء التقرير آلياً"
    }


# --------------------------------------------------------------------------
# ROUTES
# --------------------------------------------------------------------------
@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():
    """Génère le rapport HTML complet."""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    data = request.get_json()

    required = ['schoolName', 'profName', 'className', 'matiereName', 'baremeName', 'groups', 'solutions']
    if any(key not in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    # Fusion des solutions
    solutions_unified = unify_solutions(data)

    # Contexte linguistique
    lang_ctx = get_language_context(data)

    # Infos affichées dans le tableau des informations
    info_items = [
        (lang_ctx['school_label'], data['schoolName']),
        (lang_ctx['teacher_label'], data['profName']),
        (lang_ctx['class_label'], data['className']),
        (lang_ctx['subject_label'], data['matiereName']),
        (lang_ctx['criteria_label'], data['baremeName'])
    ]

    if data.get('sousBaremeName'):
        info_items.append((lang_ctx['sub_criteria_label'], data['sousBaremeName']))

    context = {
        **lang_ctx,
        'date': datetime.now().strftime('%Y/%m/%d à %H:%M'),
        'info_items': info_items,
        'groups': {
            'treatment': [{'name': n} for n in data['groups'].get('treatment', [])],
            'support': [{'name': n} for n in data['groups'].get('support', [])],
            'excellence': [{'name': n} for n in data['groups'].get('excellence', [])]
        },
        'solution_blocks': {
            lang_ctx['solutions_title']: solutions_unified['solution'],
            lang_ctx['problems_title']: solutions_unified['probleme']
        }
    }

    html = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == "__main__":
    app.run(debug=True)
