#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Math Worksheet Generator - Maths Worksheet (ttkbootstrap style)
Function: Generates an 18x5 math problems worksheet, supporting PDF export and printing.
"""

import tkinter as tk
from tkinter import filedialog
import random
import json
import os
import sys
import subprocess
import platform
from datetime import datetime
from typing import List, Tuple, Dict, Any

# ttkbootstrap UI library
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    print("Please install ttkbootstrap: pip install ttkbootstrap")
    sys.exit(1)

# PDF generation library
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm, inch
    from reportlab.lib.colors import black, gray, darkgray, lightgrey
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
except ImportError:
    print("Please install reportlab: pip install reportlab")
    sys.exit(1)


class MathWorksheetGenerator:
    """Math Worksheet Generator Application"""

    def __init__(self):
        """Initialize the application"""
        self.root = ttk.Window(
            title="Math Worksheet Generator",
            themename="cosmo",
            size=(720, 880),  # Modified size to 720pt x 880pt
            position=(100, 50)
        )

        # Multilingual support
        self.lang_dict = {
            'en': {
                'title': 'Math Worksheet Generator',
                'menu_save': 'Save',
                'menu_language': 'Language',
                'menu_about': 'About',
                'menu_export_pdf': 'Export PDF',
                'menu_print': 'Print',
                'tab_settings': '📝 Settings',
                'tab_preview': '👀 Preview',
                'card_title_label': '🎯 Worksheet Title (***Please use English***)',
                'card_problem_type': '🔢 Problem Type',
                'add': '➕ Addition',
                'sub': '➖ Subtraction',
                'mul': '✖️ Multiplication',
                'div': '➗ Division',
                'mixed': '🔀 Mixed',
                'parens': '() Order of Operations',
                'fill_blank': '__ Fill in the Blank',
                'card_ranges': '📊 Number Range',
                'range_to': 'to',
                'card_options': '⚙️ Other Options',
                'no_negative': '🚫 Avoid negative results (for subtraction)',
                'seed': '🎲 Fixed random seed:',
                'card_samples': '📋 Default Samples',
                'sample_a': 'Mixed Beginner',
                'sample_b': 'Times Tables 1-12',
                'sample_c': 'Exact Division',
                'sample_d': 'Order of Operations',
                'sample_e': 'Fill in the Blank',
                'card_actions': '🚀 Actions',
                'btn_generate': '🔄 Generate Problems',
                'btn_export': '💾 Export PDF',
                'btn_print': '🖨️ Print',
                'preview_title': '📄 Worksheet Preview',
                'status_default': 'Please click \'Generate Problems\' first.',
                'regenerate': '🔄 Regenerate & Preview',
                'copy_problems': '📋 Copy Problems',
                'save_text': '💾 Save as Text',
                'msg_complete_title': 'Generation Complete',
                'msg_complete_body': 'Successfully generated {} problems. You can now preview, export, or print.',
                'msg_error_title': 'Generation Error',
                'msg_error_body': 'An error occurred while generating problems: {}',
                'msg_warning_no_problems': 'Please generate problems first.',
                'msg_copy_success': 'Problems have been copied to the clipboard.',
                'msg_copy_fail': 'An error occurred during copying: {}',
                'msg_save_success': 'Text file saved to: {}',
                'msg_save_fail': 'An error occurred while saving: {}',
                'msg_export_success': 'PDF saved to: {}',
                'msg_export_fail': 'An error occurred while exporting the PDF: {}',
                'about_title': 'About',
                'about_content': 'Math Worksheet Generator\n\n© 2025\n\nAuthor: On Tang\nWebsite: on99.co.uk\n\nThis application is a simple tool for creating customizable math worksheets. It is designed to help students practice and improve their math skills.',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': 'The print program has been launched. Please select your printer from the dialog.',
                'msg_print_tip': 'The PDF file has been opened. Please use your PDF reader\'s print function.',
                'msg_print_success': 'The document has been sent to the default printer.',
                'msg_file_location': 'The PDF file has been generated at: {}'
            },
            'zh-tw': {
                'title': '數學練習題產生器',
                'menu_save': '檔案',
                'menu_language': '語言',
                'menu_about': '關於',
                'menu_export_pdf': '匯出為PDF',
                'menu_print': '列印',
                'tab_settings': '📝 設定',
                'tab_preview': '👀 預覽',
                'card_title_label': '🎯 工作表標題 (***請使用英文***)',
                'card_problem_type': '🔢 問題類型',
                'add': '➕ 加法',
                'sub': '➖ 減法',
                'mul': '✖️ 乘法',
                'div': '➗ 除法',
                'mixed': '🔀 混合',
                'parens': '() 運算順序',
                'fill_blank': '__ 填空',
                'card_ranges': '📊 數字範圍',
                'range_to': '至',
                'card_options': '⚙️ 其他選項',
                'no_negative': '🚫 避免負數答案 (用於減法)',
                'seed': '🎲 固定亂數種子:',
                'card_samples': '📋 範例',
                'sample_a': '混合初學者',
                'sample_b': '乘法表 1-12',
                'sample_c': '整數除法',
                'sample_d': '運算順序',
                'sample_e': '填空',
                'card_actions': '🚀 動作',
                'btn_generate': '🔄 生成題目',
                'btn_export': '💾 匯出為PDF',
                'btn_print': '🖨️ 列印',
                'preview_title': '📄 工作表預覽',
                'status_default': '請先點擊「生成題目」。',
                'regenerate': '🔄 重新生成並預覽',
                'copy_problems': '📋 複製題目',
                'save_text': '💾 儲存為文字',
                'msg_complete_title': '生成完成',
                'msg_complete_body': '已成功生成 {} 道題目。您現在可以預覽、匯出或列印。',
                'msg_error_title': '生成錯誤',
                'msg_error_body': '生成題目時發生錯誤：{}',
                'msg_warning_no_problems': '請先生成題目。',
                'msg_copy_success': '題目已複製到剪貼簿。',
                'msg_copy_fail': '複製時發生錯誤：{}',
                'msg_save_success': '文字檔已儲存至：{}',
                'msg_save_fail': '儲存時發生錯誤：{}',
                'msg_export_success': 'PDF 已儲存至：{}',
                'msg_export_fail': '匯出PDF時發生錯誤：{}',
                'about_title': '關於',
                'about_content': '數學練習題產生器\n\n© 2025\n\n作者: On Tang\n網站: on99.co.uk\n\n本應用程式是一款簡單的工具，用於建立可自訂的數學練習題。旨在幫助學生練習和提升他們的數學技能。',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': '已啟動列印程式。請從對話框中選擇您的印表機。',
                'msg_print_tip': 'PDF 文件已開啟。請使用您的 PDF 閱讀器之列印功能。',
                'msg_print_success': '文件已發送到預設印表機。',
                'msg_file_location': 'PDF 文件已生成於：{}'
            },
            'zh-cn': {
                'title': '数学练习题生成器',
                'menu_save': '文件',
                'menu_language': '语言',
                'menu_about': '关于',
                'menu_export_pdf': '导出为PDF',
                'menu_print': '打印',
                'tab_settings': '📝 设置',
                'tab_preview': '👀 预览',
                'card_title_label': '🎯 工作表标题 (***请使用英文***)',
                'card_problem_type': '🔢 问题类型',
                'add': '➕ 加法',
                'sub': '➖ 减法',
                'mul': '✖️ 乘法',
                'div': '➗ 除法',
                'mixed': '🔀 混合',
                'parens': '() 运算顺序',
                'fill_blank': '__ 填空',
                'card_ranges': '📊 数字范围',
                'range_to': '至',
                'card_options': '⚙️ 其他选项',
                'no_negative': '🚫 避免负数答案 (用于减法)',
                'seed': '🎲 固定随机种子:',
                'card_samples': '📋 示例',
                'sample_a': '混合初学者',
                'sample_b': '乘法表 1-12',
                'sample_c': '精确除法',
                'sample_d': '运算顺序',
                'sample_e': '填空',
                'card_actions': '🚀 操作',
                'btn_generate': '🔄 生成题目',
                'btn_export': '💾 导出为PDF',
                'btn_print': '🖨️ 打印',
                'preview_title': '📄 工作表预览',
                'status_default': '请先点击“生成题目”。',
                'regenerate': '🔄 重新生成并预览',
                'copy_problems': '📋 复制题目',
                'save_text': '💾 保存为文本',
                'msg_complete_title': '生成完成',
                'msg_complete_body': '已成功生成 {} 道题目。您现在可以预览、导出或打印。',
                'msg_error_title': '生成错误',
                'msg_error_body': '生成题目时发生错误：{}',
                'msg_warning_no_problems': '请先生成题目。',
                'msg_copy_success': '题目已复制到剪贴簿。',
                'msg_copy_fail': '复制时发生错误：{}',
                'msg_save_success': '文本文件已保存至：{}',
                'msg_save_fail': '保存时发生错误：{}',
                'msg_export_success': 'PDF 已保存至：{}',
                'msg_export_fail': '导出PDF时发生错误：{}',
                'about_title': '关于',
                'about_content': '数学练习题生成器\n\n© 2025\n\n作者: On Tang\n网站: on99.co.uk\n\n本应用程序是一款简单的工具，用于创建可自定义的数学练习题。旨在帮助学生练习和提升他们的数学技能。',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': '已启动打印程序。请从对话框中选择您的打印机。',
                'msg_print_tip': 'PDF 文件已打开。请使用您的 PDF 阅读器之打印功能。',
                'msg_print_success': '文件已发送到默认打印机。',
                'msg_file_location': 'PDF 文件已生成于：{}'
            },
            'ja': {
                'title': '数学ワークシートジェネレーター',
                'menu_save': '保存',
                'menu_language': '言語',
                'menu_about': 'について',
                'menu_export_pdf': 'PDFをエクスポート',
                'menu_print': '印刷',
                'tab_settings': '📝 設定',
                'tab_preview': '👀 プレビュー',
                'card_title_label': '🎯 ワークシートタイトル (***英語を使用してください***)',
                'card_problem_type': '🔢 問題の種類',
                'add': '➕ 足し算',
                'sub': '➖ 引き算',
                'mul': '✖️ 掛け算',
                'div': '➗ 割り算',
                'mixed': '🔀 混合',
                'parens': '() 演算の順序',
                'fill_blank': '__ 穴埋め',
                'card_ranges': '📊 数字の範囲',
                'range_to': 'から',
                'card_options': '⚙️ その他のオプション',
                'no_negative': '🚫 マイナスになる結果を避ける (引き算用)',
                'seed': '🎲 固定乱数シード:',
                'card_samples': '📋 デフォルトサンプル',
                'sample_a': '初心者向け混合',
                'sample_b': '九九表 1-12',
                'sample_c': '割り切り割り算',
                'sample_d': '演算の順序',
                'sample_e': '穴埋め',
                'card_actions': '🚀 アクション',
                'btn_generate': '🔄 問題を生成',
                'btn_export': '💾 PDFをエクスポート',
                'btn_print': '🖨️ 印刷',
                'preview_title': '📄 ワークシートプレビュー',
                'status_default': 'まず「問題を生成」をクリックしてください。',
                'regenerate': '🔄 再生成とプレビュー',
                'copy_problems': '📋 問題をコピー',
                'save_text': '💾 テキストで保存',
                'msg_complete_title': '生成完了',
                'msg_complete_body': '{}個の問題が正常に生成されました。プレビュー、エクスポート、印刷ができます。',
                'msg_error_title': '生成エラー',
                'msg_error_body': '問題の生成中にエラーが発生しました: {}',
                'msg_warning_no_problems': 'まず問題を生成してください。',
                'msg_copy_success': '問題がクリップボードにコピーされました。',
                'msg_copy_fail': 'コピー中にエラーが発生しました: {}',
                'msg_save_success': 'テキストファイルが保存されました: {}',
                'msg_save_fail': '保存中にエラーが発生しました: {}',
                'msg_export_success': 'PDFが保存されました: {}',
                'msg_export_fail': 'PDFのエクスポート中にエラーが発生しました: {}',
                'about_title': 'について',
                'about_content': '数学ワークシートジェネレーター\n\n© 2025\n\n著者: On Tang\nウェブサイト: on99.co.uk\n\nこのアプリケーションは、カスタマイズ可能な数学ワークシートを作成するためのシンプルなツールです。学生が数学のスキルを練習し、向上させるのに役立つように設計されています。',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': '印刷プログラムが起動しました。ダイアログからプリンタを選択してください。',
                'msg_print_tip': 'PDFファイルが開かれました。PDFリーダーの印刷機能を使用してください。',
                'msg_print_success': 'ドキュメントがデフォルトプリンタに送信されました。',
                'msg_file_location': 'PDFファイルは次の場所に生成されました: {}'
            },
            'ko': {
                'title': '수학 워크시트 생성기',
                'menu_save': '파일',
                'menu_language': '언어',
                'menu_about': '정보',
                'menu_export_pdf': 'PDF 내보내기',
                'menu_print': '인쇄',
                'tab_settings': '📝 설정',
                'tab_preview': '👀 미리보기',
                'card_title_label': '🎯 워크시트 제목 (***영어를 사용하세요***)',
                'card_problem_type': '🔢 문제 유형',
                'add': '➕ 덧셈',
                'sub': '➖ 뺄셈',
                'mul': '✖️ 곱셈',
                'div': '➗ 나눗셈',
                'mixed': '🔀 혼합',
                'parens': '() 연산 순서',
                'fill_blank': '__ 빈칸 채우기',
                'card_ranges': '📊 숫자 범위',
                'range_to': '에서',
                'card_options': '⚙️ 기타 옵션',
                'no_negative': '🚫 음수 결과 피하기 (뺄셈용)',
                'seed': '🎲 고정 랜덤 시드:',
                'card_samples': '📋 기본 샘플',
                'sample_a': '초급 혼합',
                'sample_b': '구구단 1-12',
                'sample_c': '나눗셈',
                'sample_d': '연산 순서',
                'sample_e': '빈칸 채우기',
                'card_actions': '🚀 작업',
                'btn_generate': '🔄 문제 생성',
                'btn_export': '💾 PDF 내보내기',
                'btn_print': '🖨️ 인쇄',
                'preview_title': '📄 워크시트 미리보기',
                'status_default': '먼저 \'문제 생성\'을 클릭하세요.',
                'regenerate': '🔄 다시 생성 및 미리보기',
                'copy_problems': '📋 문제 복사',
                'save_text': '💾 텍스트로 저장',
                'msg_complete_title': '생성 완료',
                'msg_complete_body': '{}개의 문제를 성공적으로 생성했습니다. 이제 미리보기, 내보내기, 인쇄를 할 수 있습니다.',
                'msg_error_title': '생성 오류',
                'msg_error_body': '문제 생성 중 오류가 발생했습니다: {}',
                'msg_warning_no_problems': '먼저 문제를 생성하세요.',
                'msg_copy_success': '문제가 클립보드에 복사되었습니다.',
                'msg_copy_fail': '복사 중 오류가 발생했습니다: {}',
                'msg_save_success': '텍스트 파일이 저장되었습니다: {}',
                'msg_save_fail': '저장 중 오류가 발생했습니다: {}',
                'msg_export_success': 'PDF가 저장되었습니다: {}',
                'msg_export_fail': 'PDF 내보내기 중 오류가 발생했습니다: {}',
                'about_title': '정보',
                'about_content': '수학 워크시트 생성기\n\n© 2025\n\nAuthor: On Tang\nWebsite: on99.co.uk\n\n이 응용 프로그램은 사용자 정의 가능한 수학 워크시트를 만드는 간단한 도구입니다. 학생들이 수학 기술을 연습하고 향상시키는 데 도움이 되도록 설계되었습니다.',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': '인쇄 프로그램이 시작되었습니다. 대화 상자에서 프린터를 선택하세요.',
                'msg_print_tip': 'PDF 파일이 열렸습니다. PDF 리더의 인쇄 기능을 사용하세요.',
                'msg_print_success': '문서가 기본 프린터로 전송되었습니다.',
                'msg_file_location': 'PDF 파일이 다음 위치에 생성되었습니다: {}'
            },
            'fr': {
                'title': 'Générateur de Fiches d\'Exercices de Mathématiques',
                'menu_save': 'Enregistrer',
                'menu_language': 'Langue',
                'menu_about': 'À propos',
                'menu_export_pdf': 'Exporter en PDF',
                'menu_print': 'Imprimer',
                'tab_settings': '📝 Paramètres',
                'tab_preview': '👀 Aperçu',
                'card_title_label': '🎯 Titre de la Fiche (***Veuillez utiliser l\'anglais***)',
                'card_problem_type': '🔢 Type de Problème',
                'add': '➕ Addition',
                'sub': '➖ Soustraction',
                'mul': '✖️ Multiplication',
                'div': '➗ Division',
                'mixed': '🔀 Mixte',
                'parens': '() Ordre des Opérations',
                'fill_blank': '__ Remplir le vide',
                'card_ranges': '📊 Plage de Nombres',
                'range_to': 'à',
                'card_options': '⚙️ Autres Options',
                'no_negative': '🚫 Éviter les résultats négatifs (pour la soustraction)',
                'seed': '🎲 Graine aléatoire fixe:',
                'card_samples': '📋 Exemples par Défaut',
                'sample_a': 'Mixte Débutant',
                'sample_b': 'Tables de Multiplication 1-12',
                'sample_c': 'Division Exacte',
                'sample_d': 'Ordre des Opérations',
                'sample_e': 'Remplir le vide',
                'card_actions': '🚀 Actions',
                'btn_generate': '🔄 Générer des Problèmes',
                'btn_export': '💾 Exporter en PDF',
                'btn_print': '🖨️ Imprimer',
                'preview_title': '📄 Aperçu de la Fiche',
                'status_default': 'Veuillez d\'abord cliquer sur \'Générer des Problèmes\'.',
                'regenerate': '🔄 Régénérer & Aperçu',
                'copy_problems': '📋 Copier les Problèmes',
                'save_text': '💾 Enregistrer en Texte',
                'msg_complete_title': 'Génération Complète',
                'msg_complete_body': 'Succès de la génération de {} problèmes. Vous pouvez maintenant les prévisualiser, les exporter ou les imprimer.',
                'msg_error_title': 'Erreur de Génération',
                'msg_error_body': 'Une erreur est survenue lors de la génération des problèmes: {}',
                'msg_warning_no_problems': 'Veuillez d\'abord générer des problèmes.',
                'msg_copy_success': 'Les problèmes ont été copiés dans le presse-papiers.',
                'msg_copy_fail': 'Une erreur est survenue lors de la copie: {}',
                'msg_save_success': 'Fichier texte enregistré dans : {}',
                'msg_save_fail': 'Une erreur est survenue lors de l\'enregistrement: {}',
                'msg_export_success': 'PDF enregistré dans : {}',
                'msg_export_fail': 'Une erreur est survenue lors de l\'exportation du PDF: {}',
                'about_title': 'À propos',
                'about_content': 'Générateur de Fiches d\'Exercices de Mathématiques\n\n© 2025\n\nAuthor: On Tang\nWebsite: on99.co.uk\n\nCette application est un outil simple pour créer des fiches d\'exercices de mathématiques personnalisables. Elle est conçue pour aider les étudiants à pratiquer et à améliorer leurs compétences en mathématiques.',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': 'Le programme d\'impression a été lancé. Veuillez sélectionner votre imprimante dans la boîte de dialogue.',
                'msg_print_tip': 'Le fichier PDF a été ouvert. Veuillez utiliser la fonction d\'impression de votre lecteur PDF.',
                'msg_print_success': 'Le document a été envoyé à l\'imprimante par défaut.',
                'msg_file_location': 'Le fichier PDF a été généré à l\'emplacement : {}'
            },
            'hi': {
                'title': 'गणित वर्कशीट जेनरेटर',
                'menu_save': 'सहेजें',
                'menu_language': 'भाषा',
                'menu_about': 'के बारे में',
                'menu_export_pdf': 'PDF के रूप में निर्यात करें',
                'menu_print': 'छापें',
                'tab_settings': '📝 सेटिंग्स',
                'tab_preview': '👀 पूर्वावलोकन',
                'card_title_label': '🎯 वर्कशीट शीर्षक (***कृपया अंग्रेजी का उपयोग करें***)',
                'card_problem_type': '🔢 समस्या का प्रकार',
                'add': '➕ जोड़',
                'sub': '➖ घटाव',
                'mul': '✖️ गुणा',
                'div': '➗ भाग',
                'mixed': '🔀 मिश्रित',
                'parens': '() संचालन का क्रम',
                'fill_blank': '__ रिक्त स्थान भरें',
                'card_ranges': '📊 संख्या सीमा',
                'range_to': 'से',
                'card_options': '⚙️ अन्य विकल्प',
                'no_negative': '🚫 नकारात्मक परिणामों से बचें (घटाव के लिए)',
                'seed': '🎲 स्थिर यादृच्छिक बीज:',
                'card_samples': '📋 डिफ़ॉल्ट नमूने',
                'sample_a': 'मिश्रित शुरुआती',
                'sample_b': 'गुणा तालिका 1-12',
                'sample_c': 'सटीक भाग',
                'sample_d': 'संचालन का क्रम',
                'sample_e': 'रिक्त स्थान भरें',
                'card_actions': '🚀 कार्य',
                'btn_generate': '🔄 समस्याएं उत्पन्न करें',
                'btn_export': '💾 PDF के रूप में निर्यात करें',
                'btn_print': '🖨️ छापें',
                'preview_title': '📄 वर्कशीट पूर्वावलोकन',
                'status_default': 'कृपया पहले \'समस्याएं उत्पन्न करें\' पर क्लिक करें।',
                'regenerate': '🔄 पुनः उत्पन्न करें और पूर्वावलोकन करें',
                'copy_problems': '📋 समस्याएं कॉपी करें',
                'save_text': '💾 टेक्स्ट के रूप में सहेजें',
                'msg_complete_title': 'पीढ़ी पूर्ण',
                'msg_complete_body': 'सफलतापूर्वक {} समस्याएं उत्पन्न हुईं। अब आप पूर्वावलोकन, निर्यात या प्रिंट कर सकते हैं।',
                'msg_error_title': 'पीढ़ी त्रुटि',
                'msg_error_body': 'समस्याएं उत्पन्न करते समय एक त्रुटि हुई: {}',
                'msg_warning_no_problems': 'कृपया पहले समस्याएं उत्पन्न करें।',
                'msg_copy_success': 'समस्याओं को क्लिपबोर्ड पर कॉपी किया गया है।',
                'msg_copy_fail': 'कॉपी करते समय एक त्रुटि हुई: {}',
                'msg_save_success': 'टेक्स्ट फ़ाइल यहां सहेजी गई: {}',
                'msg_save_fail': 'सहेजते समय एक त्रुटि हुई: {}',
                'msg_export_success': 'पीडीएफ यहां सहेजी गई: {}',
                'msg_export_fail': 'पीडीएफ निर्यात करते समय एक त्रुटि हुई: {}',
                'about_title': 'के बारे में',
                'about_content': 'गणित वर्कशीट जेनरेटर\n\n© 2025\n\nलेखक: On Tang\nवेबसाइट: on99.co.uk\n\nयह एप्लिकेशन अनुकूलन योग्य गणित वर्कशीट्स बनाने के लिए एक सरल उपकरण है। इसे छात्रों को उनके गणित कौशल का अभ्यास करने और सुधारने में मदद करने के लिए डिज़ाइन किया गया है।',
                'pdf_header': 'Maths Worksheet',
                'pdf_subtitle': 'Write the answers as fast as you can, but make sure they are correct!',
                'pdf_date': 'Date: ',
                'pdf_name': 'Name: ',
                'pdf_footer_left': 'Maths Worksheet',
                'pdf_copyright': 'Copyright © 2025. on99.co.uk',
                'msg_print_started': 'प्रिंट प्रोग्राम लॉन्च किया गया है। कृपया डायलॉग से अपना प्रिंटर चुनें।',
                'msg_print_tip': 'पीडीएफ फाइल खोली गई है। कृपया अपने पीडीएफ रीडर के प्रिंट फ़ंक्शन का उपयोग करें।',
                'msg_print_success': 'दस्तावेज़ डिफ़ॉल्ट प्रिंटर पर भेजा गया है।',
                'msg_file_location': 'पीडीएफ फाइल यहां उत्पन्न हुई है: {}'
            }
        }
        self.current_lang = 'en'
        self.trans = self.lang_dict[self.current_lang]

        self.root.title(self.trans['title'])

        # Problem configuration
        self.config = {
            'header': "Maths Worksheet",
            'mode': 'mixed',  # add, sub, mul, div, mixed, parens, fill_blank
            'add_range': (0, 50),
            'sub_range': (0, 50),
            'mul_range': (1, 12),
            'div_range': (1, 12),
            'no_negative': True,
            'seed': None,
            'shuffle': True
        }

        # Default samples
        self.samples = {
            'A': {
                'name_key': 'sample_a',
                'header': 'Maths Worksheet - Mixed Beginner',
                'mode': 'mixed',
                'add_range': (0, 50),
                'sub_range': (0, 50),
                'mul_range': (1, 10),
                'div_range': (1, 10),
                'no_negative': True
            },
            'B': {
                'name_key': 'sample_b',
                'header': 'Maths Worksheet - Times Tables',
                'mode': 'mul',
                'mul_range': (1, 12)
            },
            'C': {
                'name_key': 'sample_c',
                'header': 'Maths Worksheet - Division',
                'mode': 'div',
                'div_range': (1, 12)
            },
            'D': {
                'name_key': 'sample_d',
                'header': 'Maths Worksheet - Order of Operations',
                'mode': 'parens',
                'add_range': (1, 10),
                'sub_range': (1, 10),
                'mul_range': (1, 5),
                'div_range': (1, 5)
            },
            'E': {
                'name_key': 'sample_e',
                'header': 'Maths Worksheet - Missing Numbers',
                'mode': 'fill_blank',
                'add_range': (1, 20),
                'sub_range': (1, 20),
                'mul_range': (1, 10),
                'div_range': (1, 10)
            }
        }

        # Store generated problems
        self.current_problems = []

        self.setup_gui()

    def update_language(self, lang_code: str):
        """Update all UI elements to the selected language"""
        self.current_lang = lang_code
        self.trans = self.lang_dict[self.current_lang]
        self.root.title(self.trans['title'])
        self.setup_menu()
        self.setup_gui()

    def setup_menu(self):
        """Setup the main menu bar"""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Save menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label=self.trans['menu_save'], menu=file_menu)
        file_menu.add_command(label=self.trans['menu_export_pdf'], command=self.export_pdf)
        file_menu.add_command(label=self.trans['menu_print'], command=self.print_worksheet)

        # Language menu
        lang_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label=self.trans['menu_language'], menu=lang_menu)
        lang_menu.add_command(label='English', command=lambda: self.update_language('en'))
        lang_menu.add_command(label='繁體中文', command=lambda: self.update_language('zh-tw'))
        lang_menu.add_command(label='简体中文', command=lambda: self.update_language('zh-cn'))
        lang_menu.add_command(label='日本語', command=lambda: self.update_language('ja'))
        lang_menu.add_command(label='한국인', command=lambda: self.update_language('ko'))
        lang_menu.add_command(label='Français', command=lambda: self.update_language('fr'))
        lang_menu.add_command(label='हिन्दी', command=lambda: self.update_language('hi'))

        # About menu
        about_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label=self.trans['menu_about'], menu=about_menu)
        about_menu.add_command(label=self.trans['menu_about'], command=self.show_about)

    def show_about(self):
        """Display the about dialog with copyright info"""
        ttk.dialogs.Messagebox.show_info(
            title=self.trans['about_title'],
            message=self.trans['about_content'],
            parent=self.root
        )

    def setup_gui(self):
        """Setup the GUI interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.setup_menu()

        notebook = ttk.Notebook(self.root, bootstyle="primary")
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text=self.trans['tab_settings'])

        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text=self.trans['tab_preview'])

        self.setup_settings_tab(settings_frame)
        self.setup_preview_tab(preview_frame)

    def setup_settings_tab(self, parent):
        """Setup the "Settings" tab"""
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Title settings card
        title_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_title_label'], bootstyle="info", padding=15)
        title_card.pack(fill=X, padx=10, pady=5)

        self.header_var = tk.StringVar(value=self.config['header'])
        header_entry = ttk.Entry(title_card, textvariable=self.header_var, font=("Arial", 12), bootstyle="info")
        header_entry.pack(fill=X)

        # Problem type selection card
        mode_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_problem_type'], bootstyle="success",
                                   padding=15)
        mode_card.pack(fill=X, padx=10, pady=5)

        self.mode_var = tk.StringVar(value=self.config['mode'])

        modes_row1_frame = ttk.Frame(mode_card)
        modes_row1_frame.pack(fill=X)
        modes_row2_frame = ttk.Frame(mode_card)
        modes_row2_frame.pack(fill=X, pady=(5, 0))

        modes_row1 = [
            (self.trans['add'], 'add', 'success'),
            (self.trans['sub'], 'sub', 'warning'),
            (self.trans['mul'], 'mul', 'info'),
            (self.trans['div'], 'div', 'danger')
        ]
        modes_row2 = [
            (self.trans['mixed'], 'mixed', 'primary'),
            (self.trans['parens'], 'parens', 'dark'),
            (self.trans['fill_blank'], 'fill_blank', 'secondary')
        ]

        for text, value, style in modes_row1:
            btn = ttk.Radiobutton(
                modes_row1_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bootstyle=f"{style}-outline-toolbutton"
            )
            btn.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        for text, value, style in modes_row2:
            btn = ttk.Radiobutton(
                modes_row2_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bootstyle=f"{style}-outline-toolbutton"
            )
            btn.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        # Number range settings card
        ranges_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_ranges'], bootstyle="warning", padding=15)
        ranges_card.pack(fill=X, padx=10, pady=5)

        ranges_grid = ttk.Frame(ranges_card)
        ranges_grid.pack(fill=X)

        ttk.Label(ranges_grid, text=f"{self.trans['add']} {self.trans['card_ranges']}:",
                  font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=W, pady=3)
        self.add_min_var = tk.IntVar(value=self.config['add_range'][0])
        self.add_max_var = tk.IntVar(value=self.config['add_range'][1])
        add_frame = ttk.Frame(ranges_grid)
        add_frame.grid(row=0, column=1, sticky=W, padx=10)
        ttk.Spinbox(add_frame, from_=0, to=999, textvariable=self.add_min_var, width=8, bootstyle="success").pack(
            side=LEFT, padx=2)
        ttk.Label(add_frame, text=self.trans['range_to']).pack(side=LEFT, padx=5)
        ttk.Spinbox(add_frame, from_=0, to=999, textvariable=self.add_max_var, width=8, bootstyle="success").pack(
            side=LEFT, padx=2)

        ttk.Label(ranges_grid, text=f"{self.trans['sub']} {self.trans['card_ranges']}:",
                  font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=W, pady=3)
        self.sub_min_var = tk.IntVar(value=self.config['sub_range'][0])
        self.sub_max_var = tk.IntVar(value=self.config['sub_range'][1])
        sub_frame = ttk.Frame(ranges_grid)
        sub_frame.grid(row=1, column=1, sticky=W, padx=10)
        ttk.Spinbox(sub_frame, from_=0, to=999, textvariable=self.sub_min_var, width=8, bootstyle="warning").pack(
            side=LEFT, padx=2)
        ttk.Label(sub_frame, text=self.trans['range_to']).pack(side=LEFT, padx=5)
        ttk.Spinbox(sub_frame, from_=0, to=999, textvariable=self.sub_max_var, width=8, bootstyle="warning").pack(
            side=LEFT, padx=2)

        ttk.Label(ranges_grid, text=f"{self.trans['mul']} {self.trans['card_ranges']}:",
                  font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=W, pady=3)
        self.mul_min_var = tk.IntVar(value=self.config['mul_range'][0])
        self.mul_max_var = tk.IntVar(value=self.config['mul_range'][1])
        mul_frame = ttk.Frame(ranges_grid)
        mul_frame.grid(row=2, column=1, sticky=W, padx=10)
        ttk.Spinbox(mul_frame, from_=1, to=99, textvariable=self.mul_min_var, width=8, bootstyle="info").pack(side=LEFT,
                                                                                                              padx=2)
        ttk.Label(mul_frame, text=self.trans['range_to']).pack(side=LEFT, padx=5)
        ttk.Spinbox(mul_frame, from_=1, to=99, textvariable=self.mul_max_var, width=8, bootstyle="info").pack(side=LEFT,
                                                                                                              padx=2)

        ttk.Label(ranges_grid, text=f"{self.trans['div']} {self.trans['card_ranges']}:",
                  font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=W, pady=3)
        self.div_min_var = tk.IntVar(value=self.config['div_range'][0])
        self.div_max_var = tk.IntVar(value=self.config['div_range'][1])
        div_frame = ttk.Frame(ranges_grid)
        div_frame.grid(row=3, column=1, sticky=W, padx=10)
        ttk.Spinbox(div_frame, from_=1, to=99, textvariable=self.div_min_var, width=8, bootstyle="danger").pack(
            side=LEFT, padx=2)
        ttk.Label(div_frame, text=self.trans['range_to']).pack(side=LEFT, padx=5)
        ttk.Spinbox(div_frame, from_=1, to=99, textvariable=self.div_max_var, width=8, bootstyle="danger").pack(
            side=LEFT, padx=2)

        # Other options card
        options_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_options'], bootstyle="secondary",
                                      padding=15)
        options_card.pack(fill=X, padx=10, pady=5)

        self.no_negative_var = tk.BooleanVar(value=self.config['no_negative'])
        ttk.Checkbutton(
            options_card,
            text=self.trans['no_negative'],
            variable=self.no_negative_var,
            bootstyle="round-toggle"
        ).pack(anchor=W, pady=5)

        seed_frame = ttk.Frame(options_card)
        seed_frame.pack(fill=X, pady=5)
        ttk.Label(seed_frame, text=self.trans['seed'], font=("Arial", 10)).pack(side=LEFT)
        self.seed_var = tk.StringVar()
        ttk.Entry(seed_frame, textvariable=self.seed_var, width=20, bootstyle="secondary").pack(side=LEFT, padx=10)

        # Default samples card
        samples_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_samples'], bootstyle="primary",
                                      padding=15)
        samples_card.pack(fill=X, padx=10, pady=5)

        samples_row1_frame = ttk.Frame(samples_card)
        samples_row1_frame.pack(fill=X)
        samples_row2_frame = ttk.Frame(samples_card)
        samples_row2_frame.pack(fill=X, pady=(5, 0))

        samples_keys = list(self.samples.keys())
        sample_styles = ['success', 'info', 'warning', 'danger', 'primary']

        samples_row1_keys = ['A', 'B', 'C']
        for i, key in enumerate(samples_row1_keys):
            sample = self.samples[key]
            style = sample_styles[i % len(sample_styles)]
            btn = ttk.Button(
                samples_row1_frame,
                text=f"Sample {key}: {self.trans[sample['name_key']]}",
                command=lambda k=key: self.load_sample(k),
                bootstyle=f"{style}-outline",
                width=25
            )
            btn.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        samples_row2_keys = ['D', 'E']
        for i, key in enumerate(samples_row2_keys):
            sample = self.samples[key]
            style = sample_styles[(i + 3) % len(sample_styles)]
            btn = ttk.Button(
                samples_row2_frame,
                text=f"Sample {key}: {self.trans[sample['name_key']]}",
                command=lambda k=key: self.load_sample(k),
                bootstyle=f"{style}-outline",
                width=25
            )
            btn.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        # Action buttons card
        actions_card = ttk.Labelframe(scrollable_frame, text=self.trans['card_actions'], bootstyle="dark", padding=15)
        actions_card.pack(fill=X, padx=10, pady=10)

        buttons_frame = ttk.Frame(actions_card)
        buttons_frame.pack(fill=X)

        ttk.Button(
            buttons_frame,
            text=self.trans['btn_generate'],
            command=self.generate_problems_only,
            bootstyle="primary",
            width=20
        ).pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        ttk.Button(
            buttons_frame,
            text=self.trans['btn_export'],
            command=self.export_pdf,
            bootstyle="success",
            width=20
        ).pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        ttk.Button(
            buttons_frame,
            text=self.trans['btn_print'],
            command=self.print_worksheet,
            bootstyle="info",
            width=20
        ).pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        # Configure scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

    def setup_preview_tab(self, parent):
        """Setup the "Preview" tab"""
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=X, padx=10, pady=5)

        ttk.Label(
            title_frame,
            text=self.trans['preview_title'],
            font=("Arial", 16, "bold"),
            bootstyle="primary"
        ).pack(side=LEFT)

        self.status_var = tk.StringVar(value=self.trans['status_default'])
        status_label = ttk.Label(
            title_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            bootstyle="secondary"
        )
        status_label.pack(side=RIGHT)

        preview_container = ttk.Labelframe(parent, text="Preview Content", bootstyle="info", padding=10)
        preview_container.pack(fill=BOTH, expand=True, padx=10, pady=5)

        self.preview_text = tk.Text(
            preview_container,
            height=25,
            width=90,
            wrap=tk.NONE,
            font=("Consolas", 11),
            bg="#f8f9fa",
            fg="#343a40",
            selectbackground="#007bff",
            selectforeground="white"
        )

        scrollbar_y = ttk.Scrollbar(preview_container, orient="vertical", command=self.preview_text.yview)
        scrollbar_x = ttk.Scrollbar(preview_container, orient="horizontal", command=self.preview_text.xview)
        self.preview_text.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.preview_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        quick_actions = ttk.Frame(parent)
        quick_actions.pack(fill=X, padx=10, pady=5)

        ttk.Button(
            quick_actions,
            text=self.trans['regenerate'],
            command=self.generate_preview,
            bootstyle="outline-primary"
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            quick_actions,
            text=self.trans['copy_problems'],
            command=self.copy_problems,
            bootstyle="outline-info"
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            quick_actions,
            text=self.trans['save_text'],
            command=self.save_text,
            bootstyle="outline-success"
        ).pack(side=LEFT, padx=5)

    def load_sample(self, sample_key: str):
        """Load a default sample configuration"""
        sample = self.samples[sample_key]

        self.header_var.set(sample['header'])
        self.mode_var.set(sample['mode'])

        self.add_min_var.set(sample.get('add_range', self.config['add_range'])[0])
        self.add_max_var.set(sample.get('add_range', self.config['add_range'])[1])

        self.sub_min_var.set(sample.get('sub_range', self.config['sub_range'])[0])
        self.sub_max_var.set(sample.get('sub_range', self.config['sub_range'])[1])

        self.mul_min_var.set(sample.get('mul_range', self.config['mul_range'])[0])
        self.mul_max_var.set(sample.get('mul_range', self.config['mul_range'])[1])

        self.div_min_var.set(sample.get('div_range', self.config['div_range'])[0])
        self.div_max_var.set(sample.get('div_range', self.config['div_range'])[1])

        self.no_negative_var.set(sample.get('no_negative', self.config['no_negative']))

        ttk.dialogs.Messagebox.show_info(
            title="Success",
            message=f"Sample {sample_key}: {self.trans[sample['name_key']]} loaded successfully.",
            parent=self.root
        )

    def get_current_config(self) -> Dict[str, Any]:
        """Get the current UI configuration"""
        return {
            'header': self.header_var.get(),
            'mode': self.mode_var.get(),
            'add_range': (self.add_min_var.get(), self.add_max_var.get()),
            'sub_range': (self.sub_min_var.get(), self.sub_max_var.get()),
            'mul_range': (self.mul_min_var.get(), self.mul_max_var.get()),
            'div_range': (self.div_min_var.get(), self.div_max_var.get()),
            'no_negative': self.no_negative_var.get(),
            'seed': self.seed_var.get() if self.seed_var.get() else None
        }

    def generate_addition_problem(self, min_val: int, max_val: int) -> Tuple[str, int]:
        """Generate an addition problem"""
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        return f"{a} + {b} = ", a + b

    def generate_subtraction_problem(self, min_val: int, max_val: int, no_negative: bool) -> Tuple[str, int]:
        """Generate a subtraction problem"""
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

        if no_negative and a < b:
            a, b = b, a

        return f"{a} - {b} = ", a - b

    def generate_multiplication_problem(self, min_val: int, max_val: int) -> Tuple[str, int]:
        """Generate a multiplication problem"""
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        return f"{a} x {b} = ", a * b

    def generate_division_problem(self, min_val: int, max_val: int) -> Tuple[str, int]:
        """Generate an integer division problem"""
        quotient = random.randint(min_val, max_val)
        divisor = random.randint(min_val, max_val)
        dividend = quotient * divisor

        return f"{dividend} ÷ {divisor} = ", quotient

    def generate_parentheses_problem(self, config: Dict[str, Any]) -> Tuple[str, int]:
        """Generate an order of operations problem with parentheses"""
        ops = ['+', '-', 'x', '÷']
        op1 = random.choice(ops)
        op2 = random.choice(ops)

        if op1 == '+':
            a = random.randint(*config['add_range'])
            b = random.randint(*config['add_range'])
        elif op1 == '-':
            a = random.randint(*config['sub_range'])
            b = random.randint(*config['sub_range'])
            if config['no_negative'] and a < b:
                a, b = b, a
        elif op1 == 'x':
            a = random.randint(*config['mul_range'])
            b = random.randint(*config['mul_range'])
        else:
            quotient = random.randint(*config['div_range'])
            divisor = random.randint(*config['div_range'])
            a = quotient * divisor
            b = divisor

        c = random.choice([random.randint(*config['add_range']), random.randint(*config['mul_range'])])

        problem_text = ""
        answer = 0

        if random.choice([True, False]):
            paren_text = f"({a} {op1} {b})"
            if op1 == '+':
                paren_result = a + b
            elif op1 == '-':
                paren_result = a - b
            elif op1 == 'x':
                paren_result = a * b
            else:
                if b == 0: return self.generate_parentheses_problem(config)
                paren_result = a / b
                if paren_result != int(paren_result): return self.generate_parentheses_problem(config)
                paren_result = int(paren_result)

            if op2 == '+':
                problem_text = f"{paren_text} + {c} = "
                answer = paren_result + c
            elif op2 == '-':
                problem_text = f"{paren_text} - {c} = "
                answer = paren_result - c
            elif op2 == 'x':
                problem_text = f"{paren_text} x {c} = "
                answer = paren_result * c
            else:
                if c == 0: return self.generate_parentheses_problem(config)
                if paren_result % c != 0: return self.generate_parentheses_problem(config)
                problem_text = f"{paren_text} ÷ {c} = "
                answer = paren_result // c
        else:
            paren_text = f"({b} {op1} {c})"
            if op1 == '+':
                paren_result = b + c
            elif op1 == '-':
                paren_result = b - c
            elif op1 == 'x':
                paren_result = b * c
            else:
                if c == 0: return self.generate_parentheses_problem(config)
                paren_result = b / c
                if paren_result != int(paren_result): return self.generate_parentheses_problem(config)
                paren_result = int(paren_result)

            if op2 == '+':
                problem_text = f"{a} + {paren_text} = "
                answer = a + paren_result
            elif op2 == '-':
                if a < paren_result and config['no_negative']: return self.generate_parentheses_problem(config)
                problem_text = f"{a} - {paren_text} = "
                answer = a - paren_result
            elif op2 == 'x':
                problem_text = f"{a} x {paren_text} = "
                answer = a * paren_result
            else:
                if paren_result == 0: return self.generate_parentheses_problem(config)
                if a % paren_result != 0: return self.generate_parentheses_problem(config)
                problem_text = f"{a} ÷ {paren_text} = "
                answer = a // paren_result

        if problem_text == "" or answer is None:
            return self.generate_parentheses_problem(config)

        return problem_text, answer

    def generate_fill_blank_problem(self, config: Dict[str, Any]) -> Tuple[str, int]:
        """Generate a fill-in-the-blank problem"""
        op = random.choice(['+', '-', 'x', '÷'])

        if op == '+':
            a = random.randint(*config['add_range'])
            b = random.randint(*config['add_range'])
            result = a + b
            blank_pos = random.choice([0, 1])
            if blank_pos == 0:
                problem_text = f"__ + {b} = {result}"
                answer = a
            else:
                problem_text = f"{a} + __ = {result}"
                answer = b

        elif op == '-':
            a = random.randint(*config['sub_range'])
            b = random.randint(*config['sub_range'])
            if config['no_negative'] and a < b:
                a, b = b, a
            result = a - b
            blank_pos = random.choice([0, 1])
            if blank_pos == 0:
                problem_text = f"__ - {b} = {result}"
                answer = a
            else:
                problem_text = f"{a} - __ = {result}"
                answer = b

        elif op == 'x':
            a = random.randint(*config['mul_range'])
            b = random.randint(*config['mul_range'])
            result = a * b
            blank_pos = random.choice([0, 1])
            if blank_pos == 0:
                problem_text = f"__ x {b} = {result}"
                answer = a
            else:
                problem_text = f"{a} x __ = {result}"
                answer = b

        else:  # '÷'
            divisor = random.randint(*config['div_range'])
            quotient = random.randint(*config['div_range'])
            dividend = divisor * quotient

            blank_pos = random.choice([0, 1])
            if blank_pos == 0:
                problem_text = f"__ ÷ {divisor} = {quotient}"
                answer = dividend
            else:
                problem_text = f"{dividend} ÷ __ = {quotient}"
                answer = divisor

        return problem_text, answer

    def generate_problems(self, config: Dict[str, Any]) -> List[Tuple[str, int]]:
        """Generate 90 problems (18 x 5 = 90)"""
        if config['seed']:
            try:
                random.seed(int(config['seed']))
            except ValueError:
                random.seed(hash(config['seed']))

        problems = []
        mode = config['mode']
        total_problems = 18 * 5

        if mode == 'mixed':
            problems_per_type = total_problems // 4

            for _ in range(problems_per_type):
                problems.append(self.generate_addition_problem(*config['add_range']))

            for _ in range(problems_per_type):
                problems.append(self.generate_subtraction_problem(*config['sub_range'], config['no_negative']))

            for _ in range(problems_per_type):
                problems.append(self.generate_multiplication_problem(*config['mul_range']))

            for _ in range(problems_per_type):
                problems.append(self.generate_division_problem(*config['div_range']))

            while len(problems) < total_problems:
                problems.append(self.generate_addition_problem(*config['add_range']))

        elif mode == 'parens':
            for _ in range(total_problems):
                problems.append(self.generate_parentheses_problem(config))

        elif mode == 'fill_blank':
            for _ in range(total_problems):
                problems.append(self.generate_fill_blank_problem(config))

        else:
            for _ in range(total_problems):
                if mode == 'add':
                    problems.append(self.generate_addition_problem(*config['add_range']))
                elif mode == 'sub':
                    problems.append(self.generate_subtraction_problem(*config['sub_range'], config['no_negative']))
                elif mode == 'mul':
                    problems.append(self.generate_multiplication_problem(*config['mul_range']))
                elif mode == 'div':
                    problems.append(self.generate_division_problem(*config['div_range']))

        random.shuffle(problems)

        return problems

    def generate_problems_only(self):
        """Generate problems without showing the preview tab."""
        try:
            config = self.get_current_config()
            problems = self.generate_problems(config)
            self.current_problems = problems
            self.status_var.set(self.trans['msg_complete_body'].format(len(problems)))
            ttk.dialogs.Messagebox.show_info(
                title=self.trans['msg_complete_title'],
                message=self.trans['msg_complete_body'].format(len(problems)),
                parent=self.root
            )
        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title=self.trans['msg_error_title'],
                message=self.trans['msg_error_body'].format(str(e)),
                parent=self.root
            )

    def generate_preview(self):
        """Generate a preview"""
        try:
            config = self.get_current_config()
            problems = self.generate_problems(config)
            self.current_problems = problems

            self.preview_text.delete(1.0, tk.END)

            header = config['header']
            separator = "=" * 80

            self.preview_text.insert(tk.END, f"{separator}\n")
            self.preview_text.insert(tk.END, f"{header:^80}\n")
            self.preview_text.insert(tk.END, f"{separator}\n\n")

            self.preview_text.insert(tk.END, "Date: ________________    Name: ____________________________\n\n")

            self.preview_text.insert(tk.END,
                                     "Write the answers as fast as you can, but make sure they are correct!\n\n")

            rows = 18
            cols = 5

            for row in range(rows):
                row_text = ""
                for col in range(cols):
                    idx = row * cols + col
                    if idx < len(problems):
                        problem = problems[idx][0]
                        row_text += f"{problem:<16}"
                    else:
                        row_text += " " * 16
                self.preview_text.insert(tk.END, row_text + "\n")

            self.preview_text.insert(tk.END, f"\n{separator}\n")
            self.preview_text.insert(tk.END,
                                     f"Total problems: {len(problems)} | Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            self.status_var.set(f"✅ {len(problems)} problems generated.")

        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title=self.trans['msg_error_title'],
                message=f"An error occurred while generating the preview: {str(e)}",
                parent=self.root
            )

    def copy_problems(self):
        """Copy problems to clipboard"""
        if not self.current_problems:
            ttk.dialogs.Messagebox.show_warning(
                title=self.trans['msg_warning_no_problems'],
                message=self.trans['msg_warning_no_problems'],
                parent=self.root
            )
            return

        try:
            content = self.preview_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(content)

            ttk.dialogs.Messagebox.show_info(
                title=self.trans['msg_copy_success'],
                message=self.trans['msg_copy_success'],
                parent=self.root
            )
        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title=self.trans['msg_copy_fail'],
                message=f"{self.trans['msg_copy_fail']}: {str(e)}",
                parent=self.root
            )

    def save_text(self):
        """Save problems as a text file"""
        if not self.current_problems:
            ttk.dialogs.Messagebox.show_warning(
                title=self.trans['msg_warning_no_problems'],
                message=self.trans['msg_warning_no_problems'],
                parent=self.root
            )
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            header_clean = "".join(c for c in self.header_var.get() if c.isalnum() or c in (' ', '-', '_')).strip()
            default_filename = f"{header_clean}_{timestamp}.txt"

            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=default_filename
            )

            if filepath:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(self.preview_text.get(1.0, tk.END))

                ttk.dialogs.Messagebox.show_info(
                    title=self.trans['msg_save_success'],
                    message=self.trans['msg_save_success'].format(filepath),
                    parent=self.root
                )
        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title=self.trans['msg_save_fail'],
                message=f"{self.trans['msg_save_fail']}: {str(e)}",
                parent=self.root
            )

    def export_pdf(self):
        """Export as PDF"""
        if not self.current_problems:
            ttk.dialogs.Messagebox.show_warning(
                title=self.trans['msg_warning_no_problems'],
                message=self.trans['msg_warning_no_problems'],
                parent=self.root
            )
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            header_clean = "".join(c for c in self.header_var.get() if c.isalnum() or c in (' ', '-', '_')).strip()
            default_filename = f"{header_clean}_{timestamp}.pdf"

            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=default_filename
            )

            if not filepath:
                return

            self.create_pdf(filepath, self.current_problems, self.get_current_config())

            ttk.dialogs.Messagebox.show_info(
                title=self.trans['msg_export_success'],
                message=self.trans['msg_export_success'].format(filepath),
                parent=self.root
            )

        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title=self.trans['msg_export_fail'],
                message=f"{self.trans['msg_export_fail']}: {str(e)}",
                parent=self.root
            )

    def create_pdf(self, filepath: str, problems: List[Tuple[str, int]], config: Dict[str, Any]):
        """Create a precise A4 PDF file"""
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        margin = 10 * mm
        content_width = width - 2 * margin
        content_height = height - 2 * margin

        # Draw border
        c.setStrokeColorRGB(0.5, 0.5, 0.5)
        c.setLineWidth(1)
        pattern_size = 5 * mm

        for i in range(int(content_width / (pattern_size + 2))):
            x = margin + i * (pattern_size + 2)
            c.line(x, height - margin, x + pattern_size, height - margin)
            c.line(x, margin, x + pattern_size, margin)

        for i in range(int(content_height / (pattern_size + 2))):
            y = margin + i * (pattern_size + 2)
            c.line(margin, y, margin, y + pattern_size)
            c.line(width - margin, y, width - margin, y + pattern_size)

        header_height = 40 * mm
        title = config['header']

        c.setFont("Helvetica-Bold", 24)
        title_width = c.stringWidth(title, "Helvetica-Bold", 24)
        title_x = margin + (content_width - title_width) / 2
        title_y = height - margin - 40

        c.setFillColor(lightgrey)
        c.setStrokeColor(lightgrey)
        c.roundRect(title_x - 10, title_y - 8, title_width + 20, 35, 8, fill=1, stroke=0)

        c.setFillColor("black")
        c.drawString(title_x, title_y, title)

        c.setFont("Helvetica", 12)
        subtitle = "Write the answers as fast as you can, but make sure they are correct!"
        subtitle_width = c.stringWidth(subtitle, "Helvetica", 12)
        subtitle_x = margin + (content_width - subtitle_width) / 2
        c.drawString(subtitle_x, title_y - 30, subtitle)

        c.setFont("Helvetica", 11)
        info_y = title_y - 50

        c.drawString(margin + 20, info_y, "Date: ")
        c.setLineWidth(1)
        c.line(margin + 60, info_y - 2, margin + 160, info_y - 2)

        name_x = width - margin - 200
        c.drawString(name_x, info_y, "Name: ")
        c.line(name_x + 45, info_y - 2, width - margin - 20, info_y - 2)

        problems_start_y = info_y - 25
        problems_height = problems_start_y - margin - 25

        rows = 18
        cols = 5
        row_height = problems_height / rows
        col_width = content_width / cols

        c.setFont("Helvetica", 11)
        c.setFillColor(black)

        for row in range(rows):
            for col in range(cols):
                idx = row * cols + col
                if idx < len(problems):
                    problem_text = problems[idx][0]

                    x = margin + col * col_width + 8
                    y = problems_start_y - row * row_height - 15

                    c.drawString(x, y, problem_text)

        c.setStrokeColor(gray)
        c.setLineWidth(0.3)

        for col in range(1, cols):
            x = margin + col * col_width
            c.line(x, problems_start_y + 5, x, problems_start_y - problems_height)

        for row in range(6, rows, 6):
            y = problems_start_y - row * row_height + 2
            c.line(margin, y, margin + content_width, y)

        c.setFont("Helvetica", 8)
        c.setFillColor(darkgray)

        footer_y = margin / 2

        footer_left = self.trans['pdf_footer_left']
        c.drawString(margin, footer_y, footer_left)

        footer_right = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        footer_right_width = c.stringWidth(footer_right, "Helvetica", 8)
        c.drawString(width - margin - footer_right_width, footer_y, footer_right)

        copyright_text = self.trans['pdf_copyright']
        copyright_width = c.stringWidth(copyright_text, "Helvetica", 8)
        copyright_x = margin + (content_width - copyright_width) / 2

        c.drawString(copyright_x, footer_y, copyright_text)

        url = "https://on99.co.uk"
        url_rect = [copyright_x, footer_y - 2, copyright_x + copyright_width, footer_y + 10]
        c.linkURL(url, url_rect, relative=1)

        c.setFillColor(black)

        c.save()

    def print_worksheet(self):
        """Print the worksheet"""
        if not self.current_problems:
            ttk.dialogs.Messagebox.show_warning(
                title=self.trans['msg_warning_no_problems'],
                message=self.trans['msg_warning_no_problems'],
                parent=self.root
            )
            return

        try:
            temp_dir = os.path.join(os.path.expanduser("~"), "temp")
            os.makedirs(temp_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_pdf = os.path.join(temp_dir, f"speed_trials_print_{timestamp}.pdf")

            self.create_pdf(temp_pdf, self.current_problems, self.get_current_config())

            system = platform.system()

            if system == "Windows":
                try:
                    os.startfile(temp_pdf, "print")
                    ttk.dialogs.Messagebox.show_info(
                        title="Print Started",
                        message=self.trans['msg_print_started'],
                        parent=self.root
                    )
                except Exception:
                    os.startfile(temp_pdf)
                    ttk.dialogs.Messagebox.show_info(
                        title="Print Tip",
                        message=self.trans['msg_print_tip'],
                        parent=self.root
                    )

            elif system == "Darwin":
                try:
                    subprocess.run(["lpr", temp_pdf], check=True)
                    ttk.dialogs.Messagebox.show_info(
                        title="Print Successful",
                        message=self.trans['msg_print_success'],
                        parent=self.root
                    )
                except subprocess.CalledProcessError:
                    subprocess.run(["open", temp_pdf])
                    ttk.dialogs.Messagebox.show_info(
                        title="Print Tip",
                        message=self.trans['msg_print_tip'],
                        parent=self.root
                    )

            else:
                try:
                    subprocess.run(["lpr", temp_pdf], check=True)
                    ttk.dialogs.Messagebox.show_info(
                        title="Print Successful",
                        message=self.trans['msg_print_success'],
                        parent=self.root
                    )
                except subprocess.CalledProcessError:
                    try:
                        subprocess.run(["xdg-open", temp_pdf])
                        ttk.dialogs.Messagebox.show_info(
                            title="Print Tip",
                            message=self.trans['msg_print_tip'],
                            parent=self.root
                        )
                    except subprocess.CalledProcessError:
                        ttk.dialogs.Messagebox.show_info(
                            title="File Location",
                            message=self.trans['msg_file_location'].format(temp_pdf),
                            parent=self.root
                        )

        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                title="Print Error",
                message=f"An error occurred while printing: {str(e)}",
                parent=self.root
            )

    def run(self):
        """Run the application"""
        self.root.place_window_center()
        self.root.mainloop()


def main():
    """Main function"""
    try:
        app = MathWorksheetGenerator()
        app.run()
    except Exception as e:
        print(f"Program startup failed: {str(e)}")
        print("Please ensure the required dependencies are installed: pip install ttkbootstrap reportlab")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()