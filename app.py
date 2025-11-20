from flask import Flask, request, jsonify, make_response, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Configuration CORS simple pour le développement

TREATMENT_PLAN_TEMPLATE = '''
<!DOCTYPE html>
<html dir="{{ text_direction }}" lang="{{ lang }}">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
    <style>
        /* Reset amélioré */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: {{ font_family }};
            line-height: 1.8;
            color: #333;
            background-color: #f9f9f9;
            padding: 20px;
            font-size: 16pt;
        }
        
        /* En-tête amélioré */
        .header {
            text-align: center;
            margin: 0 auto 30px;
            padding: 20px;
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 1000px;
        }
        
        .header h1 {
            font-size: 28pt;
            margin-bottom: 10px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }
        
        .header .date {
            font-size: 14pt;
            opacity: 0.9;
        }
        
        /* Sections améliorées */
        .section {
            background: white;
            margin: 0 auto 30px;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            max-width: 1000px;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 22pt;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
            position: relative;
            text-align: {{ text_align }};
        }
        
        .section-title::after {
            content: "";
            position: absolute;
            {{ section_after_position }}: 0;
            bottom: -2px;
            width: 150px;
            height: 3px;
            background: #3498db;
        }
        
        /* Grille d'informations améliorée */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .info-item {
            margin-bottom: 15px;
        }
        
        .info-label {
            font-weight: bold;
            color: #555;
            font-size: 14pt;
            margin-bottom: 5px;
            text-align: {{ text_align }};
        }
        
        .info-value {
            padding: 10px;
            background: #f8f8f8;
            border-radius: 6px;
            border-{{ border_side }}: 3px solid #3498db;
            font-size: 15pt;
            text-align: {{ text_align }};
        }
        
        /* Groupes d'élèves améliorés */
        .groups-container {
            margin-top: 30px;
        }
        
        .group {
            margin-bottom: 30px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }
        
        .group-title {
            font-size: 18pt;
            padding: 15px;
            margin: 0;
            text-align: {{ text_align }};
        }
        
        .group.treatment .group-title {
            background-color: #e74c3c;
            color: white;
        }
        
        .group.support .group-title {
            background-color: #f39c12;
            color: white;
        }
        
        .group.excellence .group-title {
            background-color: #2ecc71;
            color: white;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14pt;
        }
        
        th {
            background-color: #f5f5f5;
            padding: 12px 15px;
            text-align: {{ text_align }};
            font-weight: bold;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            text-align: {{ text_align }};
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* Blocs de solutions améliorés */
        .solution-block {
            background: #f8f9fa;
            margin-bottom: 25px;
            padding: 20px;
            border-radius: 8px;
            border-{{ border_side }}: 4px solid #9b59b6;
        }
        
        .solution-block-title {
            font-size: 18pt;
            color: #9b59b6;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            text-align: {{ text_align }};
            flex-direction: {{ flex_direction }};
        }
        
        .solution-block-title::before {
            content: "";
            display: inline-block;
            width: 12px;
            height: 12px;
            background-color: #9b59b6;
            border-radius: 50%;
            margin-{{ bullet_margin_side }}: 10px;
        }
        
        .solution-point {
            margin-bottom: 12px;
            display: flex;
            align-items: flex-start;
            padding: 8px 0;
            flex-direction: {{ flex_direction }};
        }
        
        .bullet {
            color: #9b59b6;
            font-weight: bold;
            margin-{{ bullet_margin_side }}: 10px;
            margin-{{ bullet_opposite_side }}: 8px;
            font-size: 16pt;
        }
        
        .point-number {
            color: #e74c3c;
            font-weight: bold;
            margin-{{ bullet_margin_side }}: 10px;
            margin-{{ bullet_opposite_side }}: 8px;
            font-size: 16pt;
        }
        
        .point-content {
            flex: 1;
            font-size: 15pt;
            text-align: {{ text_align }};
        }
        
        /* Pied de page amélioré */
        .footer {
            text-align: center;
            margin: 40px auto 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #777;
            font-size: 12pt;
            max-width: 1000px;
        }
        
        /* Bouton d'impression amélioré */
        .print-button {
            position: fixed;
            top: 20px;
            {{ print_button_side }}: 20px;
            padding: 12px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            z-index: 1000;
            font-size: 14pt;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
        }
        
        .print-button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Styles d'impression améliorés */
        @media print {
            /* Suppression complète des marges et en-têtes/pieds de page */
            @page {
                size: A4;
                margin: 0 !important;
                padding: 0 !important;
                @top-left { content: none !important; }
                @top-center { content: none !important; }
                @top-right { content: none !important; }
                @bottom-left { content: none !important; }
                @bottom-center { content: none !important; }
                @bottom-right { content: none !important; }
            }
            
            /* Styles du body - aucune marge externe */
            body {
                margin: 0 !important;
                padding: 0 !important;
                width: 100% !important;
                background-color: #f9f9f9 !important;
                font-size: 16pt !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            
            /* Conteneur principal */
            body > *:not(.print-button) {
                margin: 0 !important;
                padding: 20px !important;
                width: 100% !important;
                box-sizing: border-box !important;
            }
            
            /* Masquer le bouton d'impression et les liens blob */
            .print-button,
            a[href^="blob:"] {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
            }
            
            /* Conserver tous les styles visuels */
            .header {
                background: linear-gradient(135deg, #2c3e50, #3498db) !important;
                color: white !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
                padding: 20px !important;
                margin: 0 !important;
            }
            
            .section {
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
                background: white !important;
                padding: 25px !important;
                margin: 0 !important;
                page-break-inside: avoid !important;
            }
            
            /* Styles des groupes */
            .group.treatment .group-title {
                background-color: #e74c3c !important;
                color: white !important;
            }
            
            .group.support .group-title {
                background-color: #f39c12 !important;
                color: white !important;
            }
            
            .group.excellence .group-title {
                background-color: #2ecc71 !important;
                color: white !important;
            }
            
            /* Blocs de solutions */
            .solution-block {
                background: #f8f9fa !important;
                border-{{ border_side }}: 4px solid #9b59b6 !important;
            }
            
            .solution-block-title {
                color: #9b59b6 !important;
            }
            
            /* Styles des tableaux */
            th {
                background-color: #f5f5f5 !important;
            }
            
            tr:nth-child(even) {
                background-color: #f9f9f9 !important;
            }
            
            /* Gestion des sauts de page */
            .page-break {
                page-break-before: always !important;
            }
        }
    </style>
</head>
<body>
    <!-- Bouton d'impression (masqué lors de l'impression) -->
    <button class="print-button no-print" onclick="window.print()">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
            <path d="M5 1a2 2 0 0 0-2 2v1h10V3a2 2 0 0 0-2-2H5zm6 8H5a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1z"/>
            <path d="M0 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-1v-2a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2H2a2 2 0 0 1-2-2V7zm2.5 1a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>
        </svg>
        {{ print_button_text }}
    </button>

    <div class="header">
        <h1>{{ main_title }}</h1>
        <div class="date">{{ report_date_label }}: {{ date }}</div>
    </div>
    
    <div class="section">
        <h2 class="section-title">{{ basic_info_title }}</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">{{ school_label }}:</div>
                <div class="info-value">{{ schoolName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{{ teacher_label }}:</div>
                <div class="info-value">{{ profName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{{ class_label }}:</div>
                <div class="info-value">{{ className }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{{ subject_label }}:</div>
                <div class="info-value">{{ matiereName }}</div>
            </div>
            <div class="info-item">
                <div class="info-label">{{ criteria_label }}:</div>
                <div class="info-value">{{ baremeName }}</div>
            </div>
            {% if sousBaremeName %}
            <div class="info-item">
                <div class="info-label">{{ sub_criteria_label }}:</div>
                <div class="info-value">{{ sousBaremeName }}</div>
            </div>
            {% endif %}
        </div>
    </div>
    
    <div class="section groups-container">
        <h2 class="section-title">{{ classification_title }}</h2>
        
        <div class="group treatment">
            <h3 class="group-title">{{ treatment_group_title }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{{ student_name_label }}</th>
                        <th>{{ group_label }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.treatment %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>{{ treatment_group_title }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="group support">
            <h3 class="group-title">{{ support_group_title }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{{ student_name_label }}</th>
                        <th>{{ group_label }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.support %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>{{ support_group_title }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="group excellence">
            <h3 class="group-title">{{ excellence_group_title }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{{ student_name_label }}</th>
                        <th>{{ group_label }}</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in groups.excellence %}
                    <tr>
                        <td>{{ student.name }}</td>
                        <td>{{ excellence_group_title }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="section">
        <h2 class="section-title">{{ analysis_title }}</h2>
        
        <div class="solution-block">
            <h3 class="solution-block-title">{{ solutions_title }}</h3>
            {% for item in solutions_unified.solution %}
            <div class="solution-point">
                <span class="point-number">{{ loop.index }}.</span>
                <span class="point-content">{{ item }}</span>
            </div>
            {% else %}
            <p>{{ no_solutions_text }}</p>
            {% endfor %}
        </div>

        <div class="solution-block">
            <h3 class="solution-block-title">{{ problems_title }}</h3>
            {% for item in solutions_unified.probleme %}
            <div class="solution-point">
                <span class="point-number">{{ loop.index }}.</span>
                <span class="point-content">{{ item }}</span>
            </div>
            {% else %}
            <p>{{ no_problems_text }}</p>
            {% endfor %}
        </div>
    </div>
    
    <div class="footer">
        <p>{{ footer_text }} © {{ date[:4] }}</p>
    </div>

    <script>
        window.onload = function() {
            // Option d'impression automatique
            // setTimeout(window.print, 1000);
        };
    </script>
    
</body>
</html>
'''

def unify_solutions(data):
    """Élimine les doublons et nettoie les solutions"""
    def clean_text(text):
        if not text:
            return []
        text = text.replace('ـ', '').replace('●', '').replace('★', '').strip()
        return [line.strip() for line in text.split('\n') if line.strip()]
    
    # Utilisation d'un set pour éliminer les doublons
    solutions = set()
    problemes = set()

    # Traitement des données par défaut
    default = data['solutions'].get('default', {})
    for item in clean_text(default.get('solution', '')):
        solutions.add(item)
    for item in clean_text(default.get('probleme', '')):
        problemes.add(item)

    # Traitement des propositions utilisateur
    for prop in data['solutions'].get('userProposals', []):
        if 'solution' in prop:
            for item in clean_text(prop['solution']):
                solutions.add(item)
        if 'probleme' in prop:
            for item in clean_text(prop['probleme']):
                problemes.add(item)

    # Traitement des propositions globales
    for prop in data['solutions'].get('globalProposals', []):
        if 'solution' in prop:
            for item in clean_text(prop['solution']):
                solutions.add(item)
        if 'probleme' in prop:
            for item in clean_text(prop['probleme']):
                problemes.add(item)

    return {
        'solution': [s for s in solutions if s],
        'probleme': [p for p in problemes if p]
    }

def get_language_context(data):
    """Détermine le contexte linguistique basé sur la matière"""
    # Liste des matières considérées comme françaises
    french_subjects = [
        "expression orale et récitation", "lecture", "production écrite",
        "écriture", "dictée", "langue", "langue française", "français"
    ]
    
    matiere_name = data.get('matiereName', '').lower().strip()
    is_french = any(subject in matiere_name for subject in french_subjects)
    
    if is_french:
        return {
            # Configuration technique
            'lang': 'fr',
            'text_direction': 'ltr',
            'text_align': 'left',
            'border_side': 'left',
            'section_after_position': 'left',
            'flex_direction': 'row',
            'bullet_margin_side': 'right',
            'bullet_opposite_side': 'left',
            'print_button_side': 'right',
            'font_family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            
            # Textes en français
            'page_title': 'Plan de traitement et origine de l\'erreur',
            'main_title': 'Rapport du Plan de Traitement et Origine de l\'Erreur',
            'print_button_text': 'Imprimer le rapport',
            'report_date_label': 'Date du rapport',
            'basic_info_title': 'Informations de base',
            'school_label': 'Établissement scolaire',
            'teacher_label': 'Enseignant(e)',
            'class_label': 'Niveau scolaire',
            'subject_label': 'Matière',
            'criteria_label': 'Critère adopté',
            'sub_criteria_label': 'Sous-critère',
            'classification_title': 'Classification des apprenants par niveau d\'acquisition',
            'treatment_group_title': 'Groupe de traitement (difficultés importantes)',
            'support_group_title': 'Groupe de soutien (difficultés moyennes)',
            'excellence_group_title': 'Groupe d\'excellence (bonne acquisition)',
            'student_name_label': 'Nom de l\'élève',
            'group_label': 'Groupe',
            'analysis_title': 'Analyse des erreurs et propositions de traitement',
            'solutions_title': 'Solutions proposées',
            'problems_title': 'Analyse des erreurs',
            'no_solutions_text': 'Aucune solution disponible',
            'no_problems_text': 'Aucune analyse d\'erreur disponible',
            'footer_text': 'Rapport généré automatiquement - Tous droits réservés'
        }
    else:
        return {
            # Configuration technique
            'lang': 'ar',
            'text_direction': 'rtl',
            'text_align': 'right',
            'border_side': 'right',
            'section_after_position': 'right',
            'flex_direction': 'row-reverse',
            'bullet_margin_side': 'left',
            'bullet_opposite_side': 'right',
            'print_button_side': 'left',
            'font_family': "'Amiri', 'Traditional Arabic', sans-serif",
            
            # Textes en arabe
            'page_title': 'خطة العلاج وأصل الخطأ',
            'main_title': 'تقرير خطة العلاج وأصل الخطأ',
            'print_button_text': 'طباعة التقرير',
            'report_date_label': 'تاريخ التقرير',
            'basic_info_title': 'المعلومات الأساسية',
            'school_label': 'المؤسسة التعليمية',
            'teacher_label': 'الأستاذ(ة)',
            'class_label': 'المستوى الدراسي',
            'subject_label': 'المادة الدراسية',
            'criteria_label': 'المعيار المعتمد',
            'sub_criteria_label': 'المعيار الفرعي',
            'classification_title': 'تصنيف المتعلمين حسب مستوى التحصيل',
            'treatment_group_title': 'مجموعة العلاج (صعوبات كبيرة)',
            'support_group_title': 'مجموعة الدعم (صعوبات متوسطة)',
            'excellence_group_title': 'مجموعة التميز (تحصيل جيد)',
            'student_name_label': 'اسم التلميذ(ة)',
            'group_label': 'المجموعة',
            'analysis_title': 'تحليل الأخطاء واقتراحات العلاج',
            'solutions_title': 'الحلول المقترحة',
            'problems_title': 'تحليل الأخطاء',
            'no_solutions_text': 'لا توجد حلول متاحة',
            'no_problems_text': 'لا توجد تحليلات للأخطاء متاحة',
            'footer_text': 'تم إنشاء هذا التقرير آلياً - جميع الحقوق محفوظة'
        }

@app.route('/generate-treatment-plan', methods=['POST'])
def generate_treatment_plan():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        
        # Validation des champs requis
        required_fields = ['schoolName', 'profName', 'className', 
                         'matiereName', 'baremeName', 'groups', 'solutions']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # Unification des solutions
        solutions_unified = unify_solutions(data)

        # Obtenir le contexte linguistique
        language_context = get_language_context(data)

        # Contexte de base
        base_context = {
            'date': datetime.now().strftime('%Y/%m/%d à %H:%M'),
            'schoolName': data['schoolName'],
            'profName': data['profName'],
            'className': data['className'],
            'matiereName': data['matiereName'],
            'baremeName': data['baremeName'],
            'sousBaremeName': data.get('sousBaremeName', ''),
            'groups': {
                'treatment': [{'name': name} for name in data['groups'].get('treatment', [])],
                'support': [{'name': name} for name in data['groups'].get('support', [])],
                'excellence': [{'name': name} for name in data['groups'].get('excellence', [])]
            },
            'solutions_unified': solutions_unified
        }

        # Fusionner les contextes
        context = {**base_context, **language_context}

        html_content = render_template_string(TREATMENT_PLAN_TEMPLATE, **context)
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
