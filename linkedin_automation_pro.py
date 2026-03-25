"""
LinkedIn Automation - Desktop Application
Local application with direct LinkedIn connection

Features:
- Advanced content generation following strict LinkedIn rules
- Human-like behavior simulation
- Smart scheduling with variability
- Direct LinkedIn connection via Selenium
- Professional GUI with Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import json
import os
import sys
from datetime import datetime, timedelta
import random
import time
import sqlite3
import logging

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import modules
try:
    from modules.database import Database
    from modules.advanced_content_generator import AdvancedContentGenerator
    from modules.image_handler import ImageHandler
    from modules.scheduler import SmartScheduler
    from modules.linkedin_automation import LinkedInAutomation
except ImportError as e:
    print(f"Warning: {e}")
    # Create stub classes
    class Database:
        def __init__(self): pass
        def get_stats(self): return {'total': 0, 'published': 0, 'scheduled': 0, 'generated': 0}
        def save_post(self, *args): return 1
        def get_posts(self, status=None): return []
        def get_recent_posts(self, limit=5): return []
        def update_post_status(self, *args): pass
        def delete_post(self, *args): pass


class LinkedInAutomationApp:
    """Main Application - Advanced LinkedIn Automation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 LinkedIn Automation Pro - Sistema Inteligente")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set icon
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
        
        # Colors
        self.LINKEDIN_BLUE = '#0077B5'
        self.LINKEDIN_DARK = '#004182'
        self.SUCCESS = '#28a745'
        self.WARNING = '#ffc107'
        self.DANGER = '#dc3545'
        self.GOLD = '#ffc107'
        
        # Initialize modules
        self.db = Database()
        self.content_gen = AdvancedContentGenerator()
        self.image_handler = ImageHandler()
        self.scheduler = SmartScheduler()
        self.automation = None
        
        # State
        self.is_logged_in = False
        self.current_content = None
        self.current_image = None
        
        # Create UI
        self.setup_styles()
        self.create_ui()
        
        # Load data
        self.update_dashboard()
        self.load_settings()
        
        logger.info("LinkedIn Automation Pro started")
    
    def setup_styles(self):
        """Configure UI styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom styles
        self.style.configure('LinkedIn.TButton', 
                           background=self.LINKEDIN_BLUE,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(15, 8))
        
        self.style.configure('LinkedIn.TFrame', background='#f8f9fa')
        self.style.configure('Card.TFrame', background='white')
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 18, 'bold'),
                           foreground=self.LINKEDIN_BLUE)
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12),
                           foreground='#666')
        self.style.configure('Stat.TLabel',
                           font=('Segoe UI', 24, 'bold'),
                           foreground=self.LINKEDIN_BLUE)
        self.style.configure('StatLabel.TLabel',
                           font=('Segoe UI', 10),
                           foreground='#666')
    
    def create_ui(self):
        """Create main UI"""
        # Main container
        main = ttk.Frame(self.root, style='LinkedIn.TFrame')
        main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main)
        
        # Notebook
        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_content_tab()
        self.create_posts_tab()
        self.create_schedule_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
        # Status bar
        self.create_status_bar(main)
    
    def create_header(self, parent):
        """Create header"""
        header = ttk.Frame(parent)
        header.pack(fill='x')
        
        # Title
        title_frame = ttk.Frame(header)
        title_frame.pack(side='left')
        
        ttk.Label(title_frame, text="LinkedIn Automation Pro", 
                 font=('Segoe UI', 20, 'bold'),
                 foreground=self.LINKEDIN_BLUE).pack(anchor='w')
        ttk.Label(title_frame, text="Sistema Inteligente de Publicación",
                 font=('Segoe UI', 10),
                 foreground='#666').pack(anchor='w')
        
        # Connection status
        conn_frame = ttk.Frame(header)
        conn_frame.pack(side='right')
        
        self.conn_status = ttk.Label(conn_frame, 
                                      text="● Desconectado",
                                      font=('Segoe UI', 11),
                                      foreground=self.DANGER)
        self.conn_status.pack(side='right', padx=10)
        
        ttk.Button(conn_frame, text="🌐 Conectar LinkedIn",
                  command=self.connect_linkedin,
                  style='LinkedIn.TButton').pack(side='right', padx=5)
    
    def create_dashboard_tab(self):
        """Create Dashboard tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")
        
        # Stats row
        stats_frame = ttk.Frame(tab)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.stats = {}
        stats_config = [
            ('total', '📝', 'Total Posts'),
            ('published', '✅', 'Publicados'),
            ('scheduled', '📅', 'Programados'),
            ('generated', '✨', 'Generados'),
            ('this_week', '📊', 'Esta Semana')
        ]
        
        for i, (key, icon, label) in enumerate(stats_config):
            card = ttk.Frame(stats_frame, relief='solid', borderwidth=1)
            card.grid(row=0, column=i, padx=8, pady=5, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            ttk.Label(card, text=icon, font=('Segoe UI', 28)).pack(pady=(10, 0))
            self.stats[key] = ttk.Label(card, text="0", style='Stat.TLabel')
            self.stats[key].pack()
            ttk.Label(card, text=label, style='StatLabel.TLabel').pack(pady=(0, 10))
        
        # Quick actions
        actions_frame = ttk.LabelFrame(tab, text="⚡ Acciones Rápidas", padding=15)
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack(fill='x')
        
        buttons = [
            ("✨ Generar Nuevo Post", self.quick_generate, self.LINKEDIN_BLUE),
            ("📤 Publicar Ahora", self.quick_publish, self.SUCCESS),
            ("📅 Ejecutar Scheduler", self.run_scheduler, self.WARNING),
            ("📊 Actualizar Datos", self.update_dashboard, '#666'),
            ("🧠 Ver Estadísticas IA", self.show_ai_stats, '#9c27b0')
        ]
        
        for i, (text, cmd, color) in enumerate(buttons):
            btn = ttk.Button(actions_grid, text=text, command=cmd)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky='ew')
            actions_grid.columnconfigure(i, weight=1)
        
        # Recent posts
        recent_frame = ttk.LabelFrame(tab, text="📋 Posts Recientes", padding=10)
        recent_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.recent_text = scrolledtext.ScrolledText(
            recent_frame, height=12, wrap=tk.WORD,
            font=('Consolas', 10), bg='#f8f9fa'
        )
        self.recent_text.pack(fill='both', expand=True)
    
    def create_content_tab(self):
        """Create Content Generation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✨ Generar Contenido")
        
        # Split view
        pane = ttk.PanedWindow(tab, orient='horizontal')
        pane.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left = ttk.LabelFrame(pane, text="⚙️ Configuración de Generación", padding=15)
        pane.add(left, weight=1)
        
        # Theme
        ttk.Label(left, text="Tema:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        self.theme_var = tk.StringVar(value="auto")
        themes = ["Auto (IA Decide)", "Desarrollo Software", "Experiencias Personales",
                  "Aprendizaje Profesional", "Errores y Lecciones"]
        ttk.Combobox(left, textvariable=self.theme_var, values=themes,
                    width=28, state='readonly').pack(pady=(0, 15), fill='x')
        
        # Word count
        ttk.Label(left, text="Longitud (palabras):", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        words_frame = ttk.Frame(left)
        words_frame.pack(fill='x', pady=(0, 15))
        
        self.min_words = tk.IntVar(value=80)
        self.max_words = tk.IntVar(value=180)
        
        ttk.Spinbox(words_frame, from_=50, to=300, width=6,
                    textvariable=self.min_words).pack(side='left')
        ttk.Label(words_frame, text=" a ").pack(side='left')
        ttk.Spinbox(words_frame, from_=50, to=300, width=6,
                    textvariable=self.max_words).pack(side='left')
        
        # Options
        ttk.Label(left, text="Opciones:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        self.opt_image = tk.BooleanVar(value=True)
        self.opt_hashtags = tk.BooleanVar(value=True)
        self.opt_imperfections = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(left, text="Agregar imagen relevante",
                       variable=self.opt_image).pack(anchor='w')
        ttk.Checkbutton(left, text="Generar hashtags automáticos",
                       variable=self.opt_hashtags).pack(anchor='w')
        ttk.Checkbutton(left, text="Incluir imperfecciones humanas",
                       variable=self.opt_imperfections).pack(anchor='w')
        
        # Generate button
        ttk.Button(left, text="✨ Generar Contenido IA",
                  command=self.generate_content,
                  style='LinkedIn.TButton').pack(pady=20, fill='x')
        
        # Stats
        stats_frame = ttk.LabelFrame(left, text="📊 Estadísticas IA", padding=10)
        stats_frame.pack(fill='x', pady=10)
        
        self.ai_stats_text = tk.Text(stats_frame, height=6, width=30,
                                     font=('Consolas', 9), bg='#f8f9fa')
        self.ai_stats_text.pack(fill='x')
        
        # Right panel - Preview
        right = ttk.LabelFrame(pane, text="👁️ Vista Previa del Contenido", padding=15)
        pane.add(right, weight=2)
        
        # Content preview with tags
        preview_header = ttk.Frame(right)
        preview_header.pack(fill='x', pady=(0, 10))
        
        self.preview_tone = ttk.Label(preview_header, text="TONO",
                                      background=self.LINKEDIN_BLUE,
                                      foreground='white',
                                      padding=(10, 5))
        self.preview_tone.pack(side='left', padx=2)
        
        self.preview_style = ttk.Label(preview_header, text="ESTILO",
                                       background='#6c757d',
                                       foreground='white',
                                       padding=(10, 5))
        self.preview_style.pack(side='left', padx=2)
        
        self.preview_words = ttk.Label(preview_header, text="0 palabras",
                                       foreground='#666')
        self.preview_words.pack(side='left', padx=10)
        
        self.preview_topic = ttk.Label(preview_header, text="TEMA",
                                       background=self.GOLD,
                                       foreground='black',
                                       padding=(10, 5))
        self.preview_topic.pack(side='left', padx=2)
        
        # Content text
        self.preview_content = scrolledtext.ScrolledText(
            right, height=18, wrap=tk.WORD,
            font=('Segoe UI', 12), bg='white',
            padx=15, pady=15
        )
        self.preview_content.pack(fill='both', expand=True, pady=(0, 10))
        
        # Image preview
        self.image_frame = ttk.LabelFrame(right, text="🖼️ Imagen", padding=5)
        self.image_frame.pack(fill='x')
        
        self.image_label = ttk.Label(self.image_frame, 
                                     text="La imagen aparecerá aquí",
                                     background='#e9ecef',
                                     anchor='center')
        self.image_label.pack(fill='x', ipady=30)
        
        # Hashtags
        self.hashtags_label = ttk.Label(right, text="",
                                        foreground=self.LINKEDIN_BLUE,
                                        font=('Segoe UI', 11, 'bold'))
        self.hashtags_label.pack(pady=10)
        
        # Action buttons
        actions = ttk.Frame(right)
        actions.pack(fill='x')
        
        ttk.Button(actions, text="💾 Guardar",
                  command=self.save_content,
                  style='LinkedIn.TButton').pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(actions, text="📅 Programar",
                  command=self.schedule_content,
                  style='LinkedIn.TButton').pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(actions, text="📤 Publicar",
                  command=self.publish_content,
                  style='LinkedIn.TButton').pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(actions, text="🔄 Regenerar",
                  command=self.generate_content).pack(side='left', padx=5, fill='x', expand=True)
    
    def create_posts_tab(self):
        """Create Posts tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Posts")
        
        # Header
        header = ttk.Frame(tab)
        header.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header, text="Gestión de Posts", style='Title.TLabel').pack(side='left')
        
        # Filter
        filter_frame = ttk.Frame(header)
        filter_frame.pack(side='right')
        
        ttk.Label(filter_frame, text="Filtrar:").pack(side='left')
        self.status_filter = tk.StringVar(value="ALL")
        ttk.Combobox(filter_frame, textvariable=self.status_filter,
                    values=["ALL", "GENERATED", "SCHEDULED", "PUBLISHED", "FAILED"],
                    width=12, state='readonly').pack(side='left', padx=5)
        ttk.Button(filter_frame, text="🔄", command=self.load_posts).pack(side='left')
        
        # Posts list
        columns = ('id', 'content', 'tone', 'style', 'status', 'date')
        self.posts_tree = ttk.Treeview(tab, columns=columns, show='headings', height=20)
        
        self.posts_tree.heading('id', text='ID')
        self.posts_tree.heading('content', text='Contenido')
        self.posts_tree.heading('tone', text='Tono')
        self.posts_tree.heading('style', text='Estilo')
        self.posts_tree.heading('status', text='Estado')
        self.posts_tree.heading('date', text='Fecha')
        
        self.posts_tree.column('id', width=50)
        self.posts_tree.column('content', width=400)
        self.posts_tree.column('tone', width=100)
        self.posts_tree.column('style', width=120)
        self.posts_tree.column('status', width=100)
        self.posts_tree.column('date', width=150)
        
        self.posts_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Actions
        actions = ttk.Frame(tab)
        actions.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(actions, text="📤 Publicar Seleccionado",
                  command=self.publish_selected).pack(side='left', padx=5)
        ttk.Button(actions, text="📅 Programar",
                  command=self.schedule_selected).pack(side='left', padx=5)
        ttk.Button(actions, text="✏️ Editar",
                  command=self.edit_selected).pack(side='left', padx=5)
        ttk.Button(actions, text="🗑️ Eliminar",
                  command=self.delete_selected).pack(side='left', padx=5)
    
    def create_schedule_tab(self):
        """Create Schedule tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📅 Programación")
        
        # Settings
        settings = ttk.LabelFrame(tab, text="⚙️ Configuración de Programación", padding=15)
        settings.pack(fill='x', padx=20, pady=10)
        
        grid = ttk.Frame(settings)
        grid.pack(fill='x')
        
        # Posts per week
        ttk.Label(grid, text="Posts por semana:").grid(row=0, column=0, sticky='w', pady=5)
        freq = ttk.Frame(grid)
        freq.grid(row=0, column=1, padx=10)
        
        self.min_posts = tk.IntVar(value=3)
        self.max_posts = tk.IntVar(value=5)
        ttk.Spinbox(freq, from_=1, to=7, width=5, textvariable=self.min_posts).pack(side='left')
        ttk.Label(freq, text=" a ").pack(side='left')
        ttk.Spinbox(freq, from_=1, to=7, width=5, textvariable=self.max_posts).pack(side='left')
        
        # Time preferences
        ttk.Label(grid, text="Horarios preferidos:").grid(row=1, column=0, sticky='w', pady=5)
        times = ttk.Frame(grid)
        times.grid(row=1, column=1, padx=10, sticky='w')
        
        self.morning = tk.BooleanVar(value=True)
        self.afternoon = tk.BooleanVar(value=True)
        self.evening = tk.BooleanVar(value=True)
        ttk.Checkbutton(times, text="Mañana (7-10)", variable=self.morning).pack(side='left', padx=5)
        ttk.Checkbutton(times, text="Tarde (12-15)", variable=self.afternoon).pack(side='left', padx=5)
        ttk.Checkbutton(times, text="Noche (17-20)", variable=self.evening).pack(side='left', padx=5)
        
        # Weekend
        ttk.Label(grid, text="Fines de semana:").grid(row=2, column=0, sticky='w', pady=5)
        self.weekend = tk.BooleanVar(value=False)
        ttk.Checkbutton(grid, text="Incluir (20% probabilidad)",
                       variable=self.weekend).grid(row=2, column=1, padx=10, sticky='w')
        
        ttk.Button(grid, text="💾 Guardar Configuración",
                  command=self.save_schedule_settings,
                  style='LinkedIn.TButton').grid(row=3, column=0, columnspan=2, pady=15)
        
        # Scheduled posts
        scheduled = ttk.LabelFrame(tab, text="📅 Posts Programados", padding=15)
        scheduled.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('id', 'content', 'scheduled', 'status')
        self.scheduled_tree = ttk.Treeview(scheduled, columns=columns, show='headings', height=12)
        
        self.scheduled_tree.heading('id', text='ID')
        self.scheduled_tree.heading('content', text='Contenido')
        self.scheduled_tree.heading('scheduled', text='Programado para')
        self.scheduled_tree.heading('status', text='Estado')
        
        self.scheduled_tree.column('id', width=50)
        self.scheduled_tree.column('content', width=400)
        self.scheduled_tree.column('scheduled', width=200)
        self.scheduled_tree.column('status', width=100)
        
        self.scheduled_tree.pack(fill='both', expand=True, pady=10)
        
        # Actions
        sched_actions = ttk.Frame(scheduled)
        sched_actions.pack(fill='x')
        
        ttk.Button(sched_actions, text="▶️ Ejecutar Scheduler",
                  command=self.run_scheduler,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(sched_actions, text="⏸️ Pausar",
                  command=self.pause_scheduler).pack(side='left', padx=5)
    
    def create_settings_tab(self):
        """Create Settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Configuración")
        
        # Scrollable frame
        canvas = tk.Canvas(tab, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind("<Configure>", 
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # LinkedIn credentials
        cred = ttk.LabelFrame(scrollable, text="🔐 Credenciales de LinkedIn", padding=15)
        cred.pack(fill='x', pady=10)
        
        ttk.Label(cred, text="Email/Usuario:").grid(row=0, column=0, sticky='w', pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(cred, textvariable=self.email_var, width=45).grid(row=0, column=1, padx=10)
        
        ttk.Label(cred, text="Contraseña:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(cred, textvariable=self.password_var, show="•", width=45).grid(row=1, column=1, padx=10)
        
        conn_btns = ttk.Frame(cred)
        conn_btns.grid(row=2, column=0, columnspan=2, pady=15)
        ttk.Button(conn_btns, text="🔗 Probar Conexión",
                  command=self.test_connection,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(conn_btns, text="🌐 Abrir LinkedIn",
                  command=self.open_linkedin).pack(side='left', padx=5)
        
        # Profile
        profile = ttk.LabelFrame(scrollable, text="👤 Configuración de Perfil", padding=15)
        profile.pack(fill='x', pady=10)
        
        ttk.Label(profile, text="Nombre del Perfil:").grid(row=0, column=0, sticky='w', pady=5)
        self.profile_name = tk.StringVar(value="Software Engineer")
        ttk.Entry(profile, textvariable=self.profile_name, width=45).grid(row=0, column=1, padx=10)
        
        ttk.Label(profile, text="Industria:").grid(row=1, column=0, sticky='w', pady=5)
        self.industry = tk.StringVar(value="technology")
        ttk.Combobox(profile, textvariable=self.industry,
                    values=["technology", "finance", "healthcare", "education", "marketing"],
                    width=42).grid(row=1, column=1, padx=10)
        
        ttk.Label(profile, text="Temas Principales:").grid(row=2, column=0, sticky='w', pady=5)
        self.topics = tk.StringVar(value="Software Development, Career Growth, Tech Trends")
        ttk.Entry(profile, textvariable=self.topics, width=45).grid(row=2, column=1, padx=10)
        
        # Automation
        auto = ttk.LabelFrame(scrollable, text="🤖 Configuración de Automatización", padding=15)
        auto.pack(fill='x', pady=10)
        
        self.auto_post = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto, text="Publicación automática habilitada",
                       variable=self.auto_post).pack(anchor='w', pady=5)
        
        ttk.Label(auto, text="Nivel de simulación humana:").pack(anchor='w', pady=5)
        self.behavior = tk.StringVar(value="high")
        ttk.Radiobutton(auto, text="Alto (más humano, más lento)",
                       variable=self.behavior, value="high").pack(anchor='w')
        ttk.Radiobutton(auto, text="Medio (balanceado)",
                       variable=self.behavior, value="medium").pack(anchor='w')
        ttk.Radiobutton(auto, text="Bajo (más rápido)",
                       variable=self.behavior, value="low").pack(anchor='w')
        
        # Delay settings
        delay_frame = ttk.Frame(auto)
        delay_frame.pack(fill='x', pady=10)
        
        ttk.Label(delay_frame, text="Delay entre acciones (seg):").pack(side='left')
        self.min_delay = tk.IntVar(value=2)
        self.max_delay = tk.IntVar(value=15)
        ttk.Spinbox(delay_frame, from_=1, to=30, width=5,
                    textvariable=self.min_delay).pack(side='left', padx=5)
        ttk.Label(delay_frame, text="a").pack(side='left')
        ttk.Spinbox(delay_frame, from_=1, to=60, width=5,
                    textvariable=self.max_delay).pack(side='left', padx=5)
        
        # Save button
        ttk.Button(scrollable, text="💾 Guardar Configuración",
                  command=self.save_settings,
                  style='LinkedIn.TButton').pack(pady=20)
    
    def create_logs_tab(self):
        """Create Logs tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📋 Logs")
        
        # Header
        header = ttk.Frame(tab)
        header.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header, text="Logs del Sistema", style='Title.TLabel').pack(side='left')
        
        # Controls
        controls = ttk.Frame(header)
        controls.pack(side='right')
        
        ttk.Button(controls, text="🔄 Actualizar",
                  command=self.refresh_logs).pack(side='left', padx=5)
        ttk.Button(controls, text="🗑️ Limpiar",
                  command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(controls, text="💾 Exportar",
                  command=self.export_logs).pack(side='left', padx=5)
        
        # Log viewer
        self.log_text = scrolledtext.ScrolledText(
            tab, wrap=tk.WORD, font=('Consolas', 10),
            bg='#1e1e1e', fg='#00ff00',
            insertbackground='white'
        )
        self.log_text.pack(fill='both', expand=True, padx=20, pady=10)
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status = ttk.Frame(parent)
        status.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(status, text="Listo - Sistema inicializado")
        self.status_label.pack(side='left', padx=10)
        
        self.post_count_label = ttk.Label(status, text="Posts generados: 0")
        self.post_count_label.pack(side='right', padx=10)
    
    # ========== Core Functions ==========
    
    def update_dashboard(self):
        """Update dashboard statistics"""
        try:
            stats = self.db.get_stats()
            
            self.stats['total'].config(text=str(stats.get('total', 0)))
            self.stats['published'].config(text=str(stats.get('published', 0)))
            self.stats['scheduled'].config(text=str(stats.get('scheduled', 0)))
            self.stats['generated'].config(text=str(stats.get('generated', 0)))
            
            # Posts this week
            this_week = stats.get('published_this_week', 0)
            self.stats['this_week'].config(text=str(this_week))
            
            # Update recent posts
            recent = self.db.get_recent_posts(5)
            self.recent_text.delete(1.0, tk.END)
            
            if recent:
                for post in recent:
                    self.recent_text.insert(tk.END, 
                        f"[{post.get('status', 'N/A')}] {post.get('created_at', '')}\n")
                    content_preview = post.get('content', '')[:100]
                    self.recent_text.insert(tk.END, f"{content_preview}...\n\n")
            else:
                self.recent_text.insert(tk.END, "No hay posts recientes.\n")
                self.recent_text.insert(tk.END, "\nGenera tu primer contenido desde la pestaña 'Generar Contenido'")
            
            self.update_status("Dashboard actualizado")
            
        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")
            self.update_status(f"Error: {str(e)}")
    
    def generate_content(self):
        """Generate new content using AI"""
        self.update_status("Generando contenido con IA...")
        
        def generate():
            try:
                # Get generation settings
                theme = self.theme_var.get()
                min_words = self.min_words.get()
                max_words = self.max_words.get()
                
                # Generate content
                content = self.content_gen.generate(
                    theme=theme,
                    min_words=min_words,
                    max_words=max_words
                )
                
                # Get image if enabled
                image_url = None
                if self.opt_image.get():
                    image_url = self.image_handler.search_image(
                        content.get('image_query', 'technology')
                    )
                
                # Update UI
                self.root.after(0, lambda: self.update_preview(content, image_url))
                self.root.after(0, lambda: self.update_status(
                    f"Contenido generado: {content.get('tone', 'N/A')} - {content.get('word_count', 0)} palabras"))
                self.log("INFO", f"Contenido generado: Tono={content.get('tone')}, Estilo={content.get('style')}, {content.get('word_count')} palabras")
                
                # Update AI stats
                self.root.after(0, lambda: self.update_ai_stats())
                
            except Exception as e:
                logger.error(f"Error generating content: {e}")
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.log("ERROR", f"Error generando contenido: {str(e)}")
        
        threading.Thread(target=generate, daemon=True).start()
    
    def update_preview(self, content, image_url=None):
        """Update content preview"""
        self.preview_content.delete(1.0, tk.END)
        self.preview_content.insert(tk.END, content.get('post', ''))
        
        # Update tags
        self.preview_tone.config(text=content.get('tone', 'N/A'))
        self.preview_style.config(text=content.get('style', 'N/A'))
        self.preview_words.config(text=f"{content.get('word_count', 0)} palabras")
        self.preview_topic.config(text=content.get('topic', '').replace('_', ' ').title())
        
        # Update hashtags
        if content.get('hashtags'):
            hashtags_text = ' '.join([f"#{h}" for h in content['hashtags']])
            self.hashtags_label.config(text=hashtags_text)
        
        # Update image preview
        if image_url:
            self.image_label.config(text=f"✓ Imagen: {content.get('image_query', 'N/A')}")
            self.current_image = image_url
        else:
            self.image_label.config(text="Sin imagen")
            self.current_image = None
        
        # Store current content
        self.current_content = content
        
        self.load_posts()
    
    def update_ai_stats(self):
        """Update AI statistics display"""
        try:
            stats = self.content_gen.get_statistics()
            
            stats_text = f"""Total generados: {stats.get('total_generated', 0)}
Promedio palabras: {stats.get('average_word_count', 0):.0f}
Tono más usado: {stats.get('most_used_tone', 'N/A')}
Estilo más usado: {stats.get('most_used_style', 'N/A')}
Última generación: {datetime.now().strftime('%H:%M:%S')}"""
            
            self.ai_stats_text.delete(1.0, tk.END)
            self.ai_stats_text.insert(tk.END, stats_text)
            
        except Exception as e:
            logger.error(f"Error updating AI stats: {e}")
    
    def save_content(self):
        """Save current content"""
        if not self.current_content:
            messagebox.showwarning("Aviso", "No hay contenido para guardar")
            return
        
        try:
            post_id = self.db.save_post(self.current_content, self.current_image)
            self.update_dashboard()
            self.update_status(f"Contenido guardado (ID: {post_id})")
            self.log("INFO", f"Post guardado: ID {post_id}")
            messagebox.showinfo("Éxito", f"Post guardado con ID: {post_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def publish_content(self):
        """Publish current content"""
        if not self.is_logged_in:
            messagebox.showwarning("Aviso", "Conecta a LinkedIn primero")
            return
        
        if not self.current_content:
            messagebox.showwarning("Aviso", "No hay contenido para publicar")
            return
        
        self.update_status("Publicando en LinkedIn...")
        
        def publish():
            try:
                success = self.automation.publish_post(
                    self.current_content['post'],
                    self.current_image
                )
                
                if success:
                    self.root.after(0, lambda: self.update_status(
                        "✅ Publicado exitosamente en LinkedIn"))
                    self.root.after(0, self.update_dashboard)
                    self.log("INFO", "Post publicado en LinkedIn exitosamente")
                    self.root.after(0, lambda: messagebox.showinfo("Éxito", 
                        "Post publicado en LinkedIn!"))
                else:
                    self.root.after(0, lambda: self.update_status(
                        "❌ Error al publicar"))
                    self.log("ERROR", "Error al publicar en LinkedIn")
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.log("ERROR", f"Error publicando: {str(e)}")
        
        threading.Thread(target=publish, daemon=True).start()
    
    def schedule_content(self):
        """Schedule current content"""
        if not self.current_content:
            messagebox.showwarning("Aviso", "No hay contenido para programar")
            return
        
        # Schedule dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("📅 Programar Post")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Seleccionar fecha y hora de publicación:",
                 font=('Segoe UI', 12)).pack(pady=15)
        
        # Date
        date_frame = ttk.Frame(dialog)
        date_frame.pack(pady=10)
        ttk.Label(date_frame, text="Fecha:").pack(side='left')
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=date_var, width=15).pack(side='left', padx=10)
        
        # Time
        time_frame = ttk.Frame(dialog)
        time_frame.pack(pady=10)
        ttk.Label(time_frame, text="Hora:").pack(side='left')
        time_var = tk.StringVar(value="12:00")
        ttk.Entry(time_frame, textvariable=time_var, width=10).pack(side='left', padx=10)
        
        def do_schedule():
            try:
                scheduled_time = f"{date_var.get()} {time_var.get()}"
                post_id = self.db.save_post(
                    self.current_content, 
                    self.current_image,
                    status='SCHEDULED',
                    scheduled_time=scheduled_time
                )
                self.update_dashboard()
                self.load_scheduled_posts()
                self.update_status(f"Post programado para {scheduled_time}")
                self.log("INFO", f"Post {post_id} programado para {scheduled_time}")
                dialog.destroy()
                messagebox.showinfo("Éxito", f"Post programado para {scheduled_time}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="📅 Programar",
                  command=do_schedule,
                  style='LinkedIn.TButton').pack(pady=20)
    
    def quick_generate(self):
        """Quick generate from dashboard"""
        self.notebook.select(1)
        self.generate_content()
    
    def quick_publish(self):
        """Quick publish from dashboard"""
        if self.current_content:
            self.publish_content()
        else:
            messagebox.showinfo("Info", "Primero genera contenido")
    
    def connect_linkedin(self):
        """Connect to LinkedIn"""
        self.update_status("Conectando a LinkedIn...")
        self.log("INFO", "Iniciando conexión con LinkedIn...")
        
        def connect():
            try:
                self.automation = LinkedInAutomation(
                    self.email_var.get(),
                    self.password_var.get()
                )
                
                if self.automation.login():
                    self.is_logged_in = True
                    self.root.after(0, lambda: self.conn_status.config(
                        text="● Conectado", foreground=self.SUCCESS))
                    self.root.after(0, lambda: self.update_status(
                        "✅ LinkedIn conectado exitosamente"))
                    self.log("INFO", "LinkedIn conectado exitosamente")
                else:
                    self.root.after(0, lambda: self.update_status(
                        "⚠️ Error al conectar"))
                    self.log("ERROR", "Error al conectar con LinkedIn")
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.log("ERROR", f"Error de conexión: {str(e)}")
        
        threading.Thread(target=connect, daemon=True).start()
    
    def test_connection(self):
        """Test LinkedIn connection"""
        self.connect_linkedin()
    
    def open_linkedin(self):
        """Open LinkedIn in browser"""
        if self.automation:
            self.automation.open_browser()
        else:
            import webbrowser
            webbrowser.open("https://www.linkedin.com")
    
    def run_scheduler(self):
        """Run the scheduler"""
        self.update_status("Ejecutando scheduler...")
        self.log("INFO", "Scheduler iniciado")
        
        def run():
            try:
                due_posts = self.scheduler.get_due_posts()
                
                for post in due_posts:
                    if self.is_logged_in:
                        success = self.automation.publish_post(
                            post.get('content', ''),
                            post.get('image_url')
                        )
                        if success:
                            self.db.update_post_status(post['id'], 'PUBLISHED')
                            self.log("INFO", f"Post {post['id']} publicado automáticamente")
                    
                    time.sleep(random.uniform(1, 3))
                
                self.root.after(0, lambda: self.update_status(
                    f"✅ Scheduler completado: {len(due_posts)} posts procesados"))
                self.root.after(0, self.update_dashboard)
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error: {str(e)}"))
                self.log("ERROR", f"Error en scheduler: {str(e)}")
        
        threading.Thread(target=run, daemon=True).start()
    
    def pause_scheduler(self):
        """Pause scheduler"""
        self.log("INFO", "Scheduler pausado")
        self.update_status("Scheduler pausado")
    
    def load_posts(self):
        """Load posts into treeview"""
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
        
        status = self.status_filter.get()
        if status == "ALL":
            status = None
        
        posts = self.db.get_posts(status)
        
        for post in posts:
            content_preview = post.get('content', '')[:80] + "..." if len(post.get('content', '')) > 80 else post.get('content', '')
            self.posts_tree.insert('', 'end', values=(
                post.get('id', ''),
                content_preview,
                post.get('tone', 'N/A'),
                post.get('style', 'N/A'),
                post.get('status', 'N/A'),
                post.get('created_at', '')
            ))
    
    def load_scheduled_posts(self):
        """Load scheduled posts"""
        for item in self.scheduled_tree.get_children():
            self.scheduled_tree.delete(item)
        
        posts = self.db.get_posts('SCHEDULED')
        
        for post in posts:
            content_preview = post.get('content', '')[:80] + "..." if len(post.get('content', '')) > 80 else post.get('content', '')
            self.scheduled_tree.insert('', 'end', values=(
                post.get('id', ''),
                content_preview,
                post.get('scheduled_time', 'N/A'),
                post.get('status', 'N/A')
            ))
    
    def save_settings(self):
        """Save settings"""
        settings = {
            'email': self.email_var.get(),
            'password': self.password_var.get(),
            'profile_name': self.profile_name.get(),
            'industry': self.industry.get(),
            'topics': self.topics.get(),
            'auto_post': self.auto_post.get(),
            'behavior': self.behavior.get(),
            'min_delay': self.min_delay.get(),
            'max_delay': self.max_delay.get(),
            'min_posts': self.min_posts.get(),
            'max_posts': self.max_posts.get()
        }
        
        os.makedirs('data', exist_ok=True)
        with open('data/settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
        
        self.update_status("Configuración guardada")
        self.log("INFO", "Configuración guardada")
        messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
    
    def load_settings(self):
        """Load settings"""
        try:
            if os.path.exists('data/settings.json'):
                with open('data/settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.email_var.set(settings.get('email', ''))
                self.password_var.set(settings.get('password', ''))
                self.profile_name.set(settings.get('profile_name', 'Software Engineer'))
                self.industry.set(settings.get('industry', 'technology'))
                self.topics.set(settings.get('topics', ''))
                self.auto_post.set(settings.get('auto_post', True))
                self.behavior.set(settings.get('behavior', 'high'))
                self.min_delay.set(settings.get('min_delay', 2))
                self.max_delay.set(settings.get('max_delay', 15))
                self.min_posts.set(settings.get('min_posts', 3))
                self.max_posts.set(settings.get('max_posts', 5))
                
                self.log("INFO", "Configuración cargada")
        except Exception as e:
            self.log("ERROR", f"Error cargando configuración: {str(e)}")
    
    def save_schedule_settings(self):
        """Save schedule settings"""
        self.save_settings()
        messagebox.showinfo("Éxito", "Configuración de programación guardada")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
    
    def log(self, level, message):
        """Add log entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Log to file
        if level == "INFO":
            logger.info(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
    
    def refresh_logs(self):
        """Refresh logs"""
        try:
            with open('logs/app.log', 'r', encoding='utf-8') as f:
                logs = f.read()
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, logs[-5000:])  # Last 5000 chars
        except FileNotFoundError:
            self.log("INFO", "No se encontró archivo de logs")
    
    def clear_logs(self):
        """Clear logs display"""
        self.log_text.delete(1.0, tk.END)
        self.log("INFO", "Logs limpiados")
    
    def export_logs(self):
        """Export logs"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log("INFO", f"Logs exportados a {filename}")
    
    def show_ai_stats(self):
        """Show AI statistics"""
        stats = self.content_gen.get_statistics()
        
        stats_text = f"""📊 Estadísticas del Generador IA

Total de posts generados: {stats.get('total_generated', 0)}
Promedio de palabras: {stats.get('average_word_count', 0):.0f}
Tono más usado: {stats.get('most_used_tone', 'N/A')}
Estilo más usado: {stats.get('most_used_style', 'N/A')}

📝 El sistema sigue estas reglas:
- Tono humano y natural
- Imperfecciones leves ocasionales
- Estilo variable (directo vs storytelling)
- Longitud: 80-180 palabras
- Hook + Desarrollo + Cierre con pregunta
- Temas: Desarrollo, Experiencias, Aprendizaje, Errores"""
        
        messagebox.showinfo("Estadísticas IA", stats_text)
    
    # Placeholder methods
    def publish_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            item = self.posts_tree.item(selection[0])
            self.log("INFO", f"Publicando post ID: {item['values'][0]}")
            self.update_status(f"Publicando post {item['values'][0]}...")
    
    def schedule_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            self.schedule_content()
    
    def edit_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            item = self.posts_tree.item(selection[0])
            messagebox.showinfo("Info", f"Editando post ID: {item['values'][0]}")
    
    def delete_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            item = self.posts_tree.item(selection[0])
            if messagebox.askyesno("Confirmar", "¿Eliminar este post?"):
                self.db.delete_post(item['values'][0])
                self.load_posts()
                self.update_dashboard()


def main():
    """Main entry point"""
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('assets', exist_ok=True)
    
    root = tk.Tk()
    
    # Set icon
    try:
        root.iconbitmap('assets/icon.ico')
    except:
        pass
    
    app = LinkedInAutomationApp(root)
    
    def on_closing():
        if messagebox.askokcancel("Salir", 
            "¿Estás seguro de que quieres salir?\n\n"
            "LinkedIn Automation se cerrará."):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()