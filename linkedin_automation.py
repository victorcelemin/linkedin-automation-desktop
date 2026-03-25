"""
LinkedIn Automation - Aplicación Local de Escritorio
Conexión directa a LinkedIn con interfaz gráfica completa
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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import modules
try:
    from modules.linkedin_automation import LinkedInAutomation
    from modules.content_generator import ContentGenerator
    from modules.image_handler import ImageHandler
    from modules.scheduler import SmartScheduler
    from modules.database import Database
except ImportError as e:
    print(f"Warning: Some modules not found: {e}")


class LinkedInAutomationApp:
    """Main Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Automation - Sistema de Publicación Automática")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure style
        self.setup_style()
        
        # Initialize modules
        self.db = Database()
        self.automation = None
        self.content_gen = ContentGenerator()
        self.image_handler = ImageHandler()
        self.scheduler = SmartScheduler()
        
        # State
        self.is_logged_in = False
        self.browser_running = False
        
        # Create UI
        self.create_ui()
        
        # Load settings
        self.load_settings()
        
        # Update dashboard
        self.update_dashboard()
        
        logger.info("Application started")
    
    def setup_style(self):
        """Configure application style"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.LINKEDIN_BLUE = '#0077B5'
        self.LINKEDIN_DARK = '#004182'
        self.SUCCESS_GREEN = '#28a745'
        self.WARNING_YELLOW = '#ffc107'
        self.DANGER_RED = '#dc3545'
        
        # Configure styles
        self.style.configure('LinkedIn.TButton', 
                           background=self.LINKEDIN_BLUE,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))
        self.style.configure('LinkedIn.TFrame', background='#f8f9fa')
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 16, 'bold'),
                           foreground=self.LINKEDIN_BLUE)
        self.style.configure('Status.TLabel', 
                           font=('Segoe UI', 10))
    
    def create_ui(self):
        """Create main UI"""
        # Main container
        self.main_container = ttk.Frame(self.root, style='LinkedIn.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_content_tab()
        self.create_posts_tab()
        self.create_schedule_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_dashboard_tab(self):
        """Create Dashboard tab"""
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        
        # Title
        ttk.Label(self.dashboard_frame, 
                 text="Panel de Control",
                 style='Title.TLabel').pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.Frame(self.dashboard_frame)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Stats cards
        self.stats = {}
        stats_data = [
            ('total', 'Total Posts', '0', '📝'),
            ('published', 'Publicados', '0', '✅'),
            ('scheduled', 'Programados', '0', '📅'),
            ('generated', 'Generados', '0', '✨')
        ]
        
        for i, (key, label, value, icon) in enumerate(stats_data):
            card = ttk.Frame(stats_frame, relief='solid', borderwidth=1)
            card.grid(row=0, column=i, padx=10, pady=5, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            ttk.Label(card, text=icon, font=('Segoe UI', 24)).pack(pady=5)
            self.stats[key] = ttk.Label(card, text=value, 
                                        font=('Segoe UI', 20, 'bold'),
                                        foreground=self.LINKEDIN_BLUE)
            self.stats[key].pack()
            ttk.Label(card, text=label, font=('Segoe UI', 10)).pack(pady=(0, 10))
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(self.dashboard_frame, 
                                       text="Acciones Rápidas",
                                       padding=10)
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack(fill='x')
        
        ttk.Button(actions_grid, text="🚀 Generar Nuevo Post",
                  command=self.quick_generate,
                  style='LinkedIn.TButton').grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(actions_grid, text="🌐 Conectar LinkedIn",
                  command=self.connect_linkedin,
                  style='LinkedIn.TButton').grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_grid, text="▶️ Ejecutar Scheduler",
                  command=self.run_scheduler,
                  style='LinkedIn.TButton').grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(actions_grid, text="📊 Actualizar",
                  command=self.update_dashboard).grid(row=0, column=3, padx=5, pady=5)
        
        # Recent posts frame
        recent_frame = ttk.LabelFrame(self.dashboard_frame,
                                      text="Posts Recientes",
                                      padding=10)
        recent_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.recent_posts_text = scrolledtext.ScrolledText(
            recent_frame, height=10, wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.recent_posts_text.pack(fill='both', expand=True)
    
    def create_content_tab(self):
        """Create Content Generation tab"""
        self.content_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.content_frame, text="✨ Generar Contenido")
        
        # Title
        ttk.Label(self.content_frame,
                 text="Generador de Contenido con IA",
                 style='Title.TLabel').pack(pady=10)
        
        # Main content area
        content_area = ttk.Frame(self.content_frame)
        content_area.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Settings
        left_panel = ttk.LabelFrame(content_area, text="Configuración", padding=10)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Theme selection
        ttk.Label(left_panel, text="Tema:").pack(anchor='w')
        self.theme_var = tk.StringVar(value="auto")
        themes = ["Auto (IA Decide)", "Desarrollo Software", "Crecimiento Profesional",
                  "Tendencias Tech", "Liderazgo", "Experiencia Personal"]
        self.theme_combo = ttk.Combobox(left_panel, textvariable=self.theme_var,
                                        values=themes, width=25, state='readonly')
        self.theme_combo.pack(pady=(0, 10))
        
        # Word count
        ttk.Label(left_panel, text="Longitud (palabras):").pack(anchor='w')
        words_frame = ttk.Frame(left_panel)
        words_frame.pack(fill='x', pady=(0, 10))
        self.min_words = tk.IntVar(value=80)
        self.max_words = tk.IntVar(value=180)
        ttk.Spinbox(words_frame, from_=50, to=300, width=6,
                    textvariable=self.min_words).pack(side='left')
        ttk.Label(words_frame, text=" - ").pack(side='left')
        ttk.Spinbox(words_frame, from_=50, to=300, width=6,
                    textvariable=self.max_words).pack(side='left')
        
        # Options
        ttk.Label(left_panel, text="Opciones:").pack(anchor='w')
        self.add_image_var = tk.BooleanVar(value=True)
        self.add_hashtags_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_panel, text="Agregar imagen",
                       variable=self.add_image_var).pack(anchor='w')
        ttk.Checkbutton(left_panel, text="Agregar hashtags",
                       variable=self.add_hashtags_var).pack(anchor='w')
        
        # Generate button
        ttk.Button(left_panel, text="✨ Generar Contenido",
                  command=self.generate_content,
                  style='LinkedIn.TButton').pack(pady=20, fill='x')
        
        # Right panel - Preview
        right_panel = ttk.LabelFrame(content_area, text="Vista Previa", padding=10)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Content preview
        self.preview_text = scrolledtext.ScrolledText(
            right_panel, height=15, wrap=tk.WORD,
            font=('Segoe UI', 11)
        )
        self.preview_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Image preview placeholder
        self.image_frame = ttk.Frame(right_panel)
        self.image_frame.pack(fill='x', pady=5)
        self.image_label = ttk.Label(self.image_frame, 
                                     text="[Imagen aparecerá aquí]",
                                     relief='solid', anchor='center')
        self.image_label.pack(fill='x', ipady=40)
        
        # Hashtags
        self.hashtags_label = ttk.Label(right_panel, text="", 
                                        foreground=self.LINKEDIN_BLUE,
                                        font=('Segoe UI', 10, 'bold'))
        self.hashtags_label.pack(pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(right_panel)
        action_frame.pack(fill='x', pady=10)
        
        ttk.Button(action_frame, text="💾 Guardar",
                  command=self.save_content,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="📅 Programar",
                  command=self.schedule_content,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="📤 Publicar Ahora",
                  command=self.publish_now,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Regenerar",
                  command=self.generate_content).pack(side='left', padx=5)
    
    def create_posts_tab(self):
        """Create Posts management tab"""
        self.posts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.posts_frame, text="📝 Posts")
        
        # Title
        ttk.Label(self.posts_frame,
                 text="Gestión de Posts",
                 style='Title.TLabel').pack(pady=10)
        
        # Filter frame
        filter_frame = ttk.Frame(self.posts_frame)
        filter_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por estado:").pack(side='left')
        self.status_filter = tk.StringVar(value="ALL")
        statuses = ["ALL", "GENERATED", "SCHEDULED", "PUBLISHED", "FAILED"]
        ttk.Combobox(filter_frame, textvariable=self.status_filter,
                    values=statuses, width=15, state='readonly').pack(side='left', padx=10)
        ttk.Button(filter_frame, text="🔄 Actualizar",
                  command=self.load_posts).pack(side='left', padx=10)
        
        # Posts treeview
        columns = ('id', 'content', 'tone', 'status', 'date')
        self.posts_tree = ttk.Treeview(self.posts_frame, columns=columns,
                                       show='headings', height=15)
        
        self.posts_tree.heading('id', text='ID')
        self.posts_tree.heading('content', text='Contenido')
        self.posts_tree.heading('tone', text='Tono')
        self.posts_tree.heading('status', text='Estado')
        self.posts_tree.heading('date', text='Fecha')
        
        self.posts_tree.column('id', width=50)
        self.posts_tree.column('content', width=400)
        self.posts_tree.column('tone', width=100)
        self.posts_tree.column('status', width=100)
        self.posts_tree.column('date', width=150)
        
        self.posts_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Posts actions
        posts_actions = ttk.Frame(self.posts_frame)
        posts_actions.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(posts_actions, text="📤 Publicar Seleccionado",
                  command=self.publish_selected).pack(side='left', padx=5)
        ttk.Button(posts_actions, text="📅 Programar Seleccionado",
                  command=self.schedule_selected).pack(side='left', padx=5)
        ttk.Button(posts_actions, text="✏️ Editar",
                  command=self.edit_selected).pack(side='left', padx=5)
        ttk.Button(posts_actions, text="🗑️ Eliminar",
                  command=self.delete_selected).pack(side='left', padx=5)
    
    def create_schedule_tab(self):
        """Create Schedule tab"""
        self.schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_frame, text="📅 Programación")
        
        # Title
        ttk.Label(self.schedule_frame,
                 text="Programación Inteligente",
                 style='Title.TLabel').pack(pady=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.schedule_frame,
                                        text="Configuración de Publicación",
                                        padding=10)
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        settings_grid = ttk.Frame(settings_frame)
        settings_grid.pack(fill='x')
        
        # Posts per week
        ttk.Label(settings_grid, text="Posts por semana:").grid(row=0, column=0, sticky='w', pady=5)
        freq_frame = ttk.Frame(settings_grid)
        freq_frame.grid(row=0, column=1, padx=10, pady=5)
        
        self.min_posts = tk.IntVar(value=3)
        self.max_posts = tk.IntVar(value=5)
        ttk.Spinbox(freq_frame, from_=1, to=7, width=5,
                    textvariable=self.min_posts).pack(side='left')
        ttk.Label(freq_frame, text=" a ").pack(side='left')
        ttk.Spinbox(freq_frame, from_=1, to=7, width=5,
                    textvariable=self.max_posts).pack(side='left')
        
        # Preferred times
        ttk.Label(settings_grid, text="Horarios preferidos:").grid(row=1, column=0, sticky='w', pady=5)
        times_frame = ttk.Frame(settings_grid)
        times_frame.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        self.morning_var = tk.BooleanVar(value=True)
        self.afternoon_var = tk.BooleanVar(value=True)
        self.evening_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(times_frame, text="Mañana (7-10)",
                       variable=self.morning_var).pack(side='left', padx=5)
        ttk.Checkbutton(times_frame, text="Tarde (12-15)",
                       variable=self.afternoon_var).pack(side='left', padx=5)
        ttk.Checkbutton(times_frame, text="Noche (17-20)",
                       variable=self.evening_var).pack(side='left', padx=5)
        
        # Weekend posting
        ttk.Label(settings_grid, text="Publicar fines de semana:").grid(row=2, column=0, sticky='w', pady=5)
        self.weekend_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_grid, text="Sí (20% probabilidad)",
                       variable=self.weekend_var).grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Save settings button
        ttk.Button(settings_grid, text="💾 Guardar Configuración",
                  command=self.save_schedule_settings,
                  style='LinkedIn.TButton').grid(row=3, column=0, columnspan=2, pady=15)
        
        # Scheduled posts frame
        scheduled_frame = ttk.LabelFrame(self.schedule_frame,
                                         text="Posts Programados",
                                         padding=10)
        scheduled_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scheduled posts treeview
        sched_columns = ('id', 'content', 'scheduled_time', 'status')
        self.scheduled_tree = ttk.Treeview(scheduled_frame, columns=sched_columns,
                                           show='headings', height=10)
        
        self.scheduled_tree.heading('id', text='ID')
        self.scheduled_tree.heading('content', text='Contenido')
        self.scheduled_tree.heading('scheduled_time', text='Programado para')
        self.scheduled_tree.heading('status', text='Estado')
        
        self.scheduled_tree.column('id', width=50)
        self.scheduled_tree.column('content', width=400)
        self.scheduled_tree.column('scheduled_time', width=200)
        self.scheduled_tree.column('status', width=100)
        
        self.scheduled_tree.pack(fill='both', expand=True, pady=5)
        
        # Scheduler actions
        sched_actions = ttk.Frame(scheduled_frame)
        sched_actions.pack(fill='x', pady=10)
        
        ttk.Button(sched_actions, text="▶️ Ejecutar Scheduler",
                  command=self.run_scheduler,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(sched_actions, text="⏸️ Pausar",
                  command=self.pause_scheduler).pack(side='left', padx=5)
        ttk.Button(sched_actions, text="🗑️ Cancelar Seleccionado",
                  command=self.cancel_selected_schedule).pack(side='left', padx=5)
    
    def create_settings_tab(self):
        """Create Settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Configuración")
        
        # Title
        ttk.Label(self.settings_frame,
                 text="Configuración del Sistema",
                 style='Title.TLabel').pack(pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(self.settings_frame)
        scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # LinkedIn credentials
        cred_frame = ttk.LabelFrame(scrollable_frame, 
                                     text="Credenciales de LinkedIn",
                                     padding=15)
        cred_frame.pack(fill='x', pady=10)
        
        ttk.Label(cred_frame, text="Email/Usuario:").grid(row=0, column=0, sticky='w', pady=5)
        self.linkedin_email = tk.StringVar()
        ttk.Entry(cred_frame, textvariable=self.linkedin_email, width=40).grid(
            row=0, column=1, padx=10, pady=5)
        
        ttk.Label(cred_frame, text="Contraseña:").grid(row=1, column=0, sticky='w', pady=5)
        self.linkedin_password = tk.StringVar()
        ttk.Entry(cred_frame, textvariable=self.linkedin_password, 
                 show="*", width=40).grid(row=1, column=1, padx=10, pady=5)
        
        # Connection buttons
        conn_frame = ttk.Frame(cred_frame)
        conn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        ttk.Button(conn_frame, text="🔗 Probar Conexión",
                  command=self.test_connection,
                  style='LinkedIn.TButton').pack(side='left', padx=5)
        ttk.Button(conn_frame, text="🌐 Abrir LinkedIn",
                  command=self.open_linkedin).pack(side='left', padx=5)
        
        # Profile settings
        profile_frame = ttk.LabelFrame(scrollable_frame,
                                       text="Configuración de Perfil",
                                       padding=15)
        profile_frame.pack(fill='x', pady=10)
        
        ttk.Label(profile_frame, text="Nombre del Perfil:").grid(row=0, column=0, sticky='w', pady=5)
        self.profile_name = tk.StringVar(value="Software Engineer")
        ttk.Entry(profile_frame, textvariable=self.profile_name, width=40).grid(
            row=0, column=1, padx=10, pady=5)
        
        ttk.Label(profile_frame, text="Industria:").grid(row=1, column=0, sticky='w', pady=5)
        self.industry = tk.StringVar(value="technology")
        industries = ["technology", "finance", "healthcare", "education", "marketing"]
        ttk.Combobox(profile_frame, textvariable=self.industry,
                    values=industries, width=37).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(profile_frame, text="Temas Principales:").grid(row=2, column=0, sticky='w', pady=5)
        self.topics = tk.StringVar(value="Software Development, Career Growth, Tech Trends")
        ttk.Entry(profile_frame, textvariable=self.topics, width=40).grid(
            row=2, column=1, padx=10, pady=5)
        
        # Automation settings
        auto_frame = ttk.LabelFrame(scrollable_frame,
                                     text="Automatización",
                                     padding=15)
        auto_frame.pack(fill='x', pady=10)
        
        self.auto_post = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto_frame, text="Publicación automática habilitada",
                       variable=self.auto_post).pack(anchor='w', pady=5)
        
        ttk.Label(auto_frame, text="Nivel de comportamiento humano:").pack(anchor='w', pady=5)
        self.behavior_level = tk.StringVar(value="high")
        ttk.Radiobutton(auto_frame, text="Alto (más humano, más lento)",
                       variable=self.behavior_level, value="high").pack(anchor='w')
        ttk.Radiobutton(auto_frame, text="Medio (balanceado)",
                       variable=self.behavior_level, value="medium").pack(anchor='w')
        ttk.Radiobutton(auto_frame, text="Bajo (más rápido, menos humano)",
                       variable=self.behavior_level, value="low").pack(anchor='w')
        
        # Delay settings
        delay_frame = ttk.Frame(auto_frame)
        delay_frame.pack(fill='x', pady=10)
        
        ttk.Label(delay_frame, text="Delay entre acciones (segundos):").pack(side='left')
        self.min_delay = tk.IntVar(value=2)
        self.max_delay = tk.IntVar(value=15)
        ttk.Spinbox(delay_frame, from_=1, to=30, width=5,
                    textvariable=self.min_delay).pack(side='left', padx=5)
        ttk.Label(delay_frame, text="a").pack(side='left')
        ttk.Spinbox(delay_frame, from_=1, to=60, width=5,
                    textvariable=self.max_delay).pack(side='left', padx=5)
        
        # Save button
        ttk.Button(scrollable_frame, text="💾 Guardar Configuración",
                  command=self.save_settings,
                  style='LinkedIn.TButton').pack(pady=20)
    
    def create_logs_tab(self):
        """Create Logs tab"""
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="📋 Logs")
        
        # Title
        ttk.Label(self.logs_frame,
                 text="Logs del Sistema",
                 style='Title.TLabel').pack(pady=10)
        
        # Filter frame
        filter_frame = ttk.Frame(self.logs_frame)
        filter_frame.pack(fill='x', padx=20, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar:").pack(side='left')
        self.log_filter = tk.StringVar(value="ALL")
        ttk.Combobox(filter_frame, textvariable=self.log_filter,
                    values=["ALL", "INFO", "WARNING", "ERROR"],
                    width=15, state='readonly').pack(side='left', padx=10)
        ttk.Button(filter_frame, text="🔄 Actualizar",
                  command=self.refresh_logs).pack(side='left', padx=5)
        ttk.Button(filter_frame, text="🗑️ Limpiar",
                  command=self.clear_logs).pack(side='left', padx=5)
        ttk.Button(text="💾 Exportar", command=self.export_logs).pack(side='left', padx=5)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            self.logs_frame, wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#1e1e1e', fg='#00ff00',
            insertbackground='white'
        )
        self.logs_text.pack(fill='both', expand=True, padx=20, pady=10)
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.main_container)
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Listo", style='Status.TLabel')
        self.status_label.pack(side='left', padx=10)
        
        self.connection_status = ttk.Label(status_frame, text="🔴 Desconectado",
                                          style='Status.TLabel')
        self.connection_status.pack(side='right', padx=10)
    
    # ========== Core Functions ==========
    
    def update_dashboard(self):
        """Update dashboard statistics"""
        stats = self.db.get_stats()
        
        self.stats['total'].config(text=str(stats.get('total', 0)))
        self.stats['published'].config(text=str(stats.get('published', 0)))
        self.stats['scheduled'].config(text=str(stats.get('scheduled', 0)))
        self.stats['generated'].config(text=str(stats.get('generated', 0)))
        
        # Update recent posts
        recent = self.db.get_recent_posts(5)
        self.recent_posts_text.delete(1.0, tk.END)
        
        if recent:
            for post in recent:
                self.recent_posts_text.insert(tk.END, 
                    f"[{post['status']}] {post['created_at']}\n")
                self.recent_posts_text.insert(tk.END, 
                    f"{post['content'][:100]}...\n\n")
        else:
            self.recent_posts_text.insert(tk.END, "No hay posts recientes.")
        
        self.update_status("Dashboard actualizado")
    
    def connect_linkedin(self):
        """Connect to LinkedIn"""
        self.update_status("Conectando a LinkedIn...")
        
        def connect():
            try:
                self.automation = LinkedInAutomation(
                    self.linkedin_email.get(),
                    self.linkedin_password.get()
                )
                
                if self.automation.login():
                    self.is_logged_in = True
                    self.root.after(0, lambda: self.connection_status.config(
                        text="🟢 Conectado"))
                    self.root.after(0, lambda: self.update_status(
                        "LinkedIn conectado exitosamente"))
                    self.log("INFO", "LinkedIn conectado exitosamente")
                else:
                    self.root.after(0, lambda: self.update_status(
                        "Error al conectar con LinkedIn"))
                    self.log("ERROR", "Error al conectar con LinkedIn")
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"Error: {str(e)}"))
                self.log("ERROR", f"Error de conexión: {str(e)}")
        
        threading.Thread(target=connect, daemon=True).start()
    
    def generate_content(self):
        """Generate new content"""
        self.update_status("Generando contenido...")
        
        def generate():
            try:
                # Get settings
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
                if self.add_image_var.get():
                    image_url = self.image_handler.search_image(
                        content.get('image_query', 'technology')
                    )
                
                # Update UI
                self.root.after(0, lambda: self.update_preview(
                    content, image_url))
                self.root.after(0, lambda: self.update_status(
                    "Contenido generado exitosamente"))
                self.log("INFO", f"Contenido generado: {content.get('tone', 'N/A')}")
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"Error: {str(e)}"))
                self.log("ERROR", f"Error generando contenido: {str(e)}")
        
        threading.Thread(target=generate, daemon=True).start()
    
    def update_preview(self, content, image_url=None):
        """Update content preview"""
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, content.get('content', ''))
        
        if content.get('hashtags'):
            hashtags = ' '.join([f"#{h}" for h in content['hashtags']])
            self.hashtags_label.config(text=hashtags)
        
        if image_url:
            self.image_label.config(text=f"[Imagen: {image_url[:50]}...]")
        
        # Store current content
        self.current_content = content
        self.current_image = image_url
    
    def save_content(self):
        """Save current content"""
        if not hasattr(self, 'current_content'):
            messagebox.showwarning("Aviso", "No hay contenido para guardar")
            return
        
        self.db.save_post(self.current_content, self.current_image)
        self.update_dashboard()
        self.load_posts()
        self.update_status("Contenido guardado")
        self.log("INFO", "Contenido guardado en base de datos")
        messagebox.showinfo("Éxito", "Contenido guardado exitosamente")
    
    def publish_now(self):
        """Publish content immediately"""
        if not self.is_logged_in:
            messagebox.showwarning("Aviso", "Conecta a LinkedIn primero")
            return
        
        if not hasattr(self, 'current_content'):
            messagebox.showwarning("Aviso", "No hay contenido para publicar")
            return
        
        self.update_status("Publicando en LinkedIn...")
        
        def publish():
            try:
                success = self.automation.publish_post(
                    self.current_content['content'],
                    self.current_image
                )
                
                if success:
                    self.db.update_post_status(self.current_content.get('id'), 
                                              'PUBLISHED')
                    self.root.after(0, lambda: self.update_status(
                        "Publicado exitosamente"))
                    self.root.after(0, self.update_dashboard)
                    self.log("INFO", "Post publicado en LinkedIn")
                else:
                    self.root.after(0, lambda: self.update_status(
                        "Error al publicar"))
                    self.log("ERROR", "Error al publicar en LinkedIn")
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"Error: {str(e)}"))
                self.log("ERROR", f"Error publicando: {str(e)}")
        
        threading.Thread(target=publish, daemon=True).start()
    
    def schedule_content(self):
        """Schedule current content"""
        if not hasattr(self, 'current_content'):
            messagebox.showwarning("Aviso", "No hay contenido para programar")
            return
        
        # Show schedule dialog
        schedule_dialog = tk.Toplevel(self.root)
        schedule_dialog.title("Programar Post")
        schedule_dialog.geometry("300x200")
        
        ttk.Label(schedule_dialog, text="Seleccionar fecha y hora:").pack(pady=10)
        
        # Date entry
        date_frame = ttk.Frame(schedule_dialog)
        date_frame.pack(pady=5)
        ttk.Label(date_frame, text="Fecha:").pack(side='left')
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=date_var, width=15).pack(side='left', padx=5)
        
        # Time entry
        time_frame = ttk.Frame(schedule_dialog)
        time_frame.pack(pady=5)
        ttk.Label(time_frame, text="Hora:").pack(side='left')
        time_var = tk.StringVar(value="12:00")
        ttk.Entry(time_frame, textvariable=time_var, width=10).pack(side='left', padx=5)
        
        def do_schedule():
            try:
                scheduled_time = f"{date_var.get()} {time_var.get()}"
                self.db.save_post(self.current_content, self.current_image,
                                 status='SCHEDULED', scheduled_time=scheduled_time)
                self.update_dashboard()
                self.load_scheduled_posts()
                self.update_status(f"Programado para {scheduled_time}")
                self.log("INFO", f"Post programado para {scheduled_time}")
                schedule_dialog.destroy()
                messagebox.showinfo("Éxito", f"Post programado para {scheduled_time}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(schedule_dialog, text="Programar",
                  command=do_schedule,
                  style='LinkedIn.TButton').pack(pady=20)
    
    def load_posts(self):
        """Load posts into treeview"""
        # Clear existing items
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
        
        # Get filter
        status_filter = self.status_filter.get()
        if status_filter == "ALL":
            status_filter = None
        
        # Load posts
        posts = self.db.get_posts(status_filter)
        
        for post in posts:
            content_preview = post['content'][:80] + "..." if len(post['content']) > 80 else post['content']
            self.posts_tree.insert('', 'end', values=(
                post['id'],
                content_preview,
                post.get('tone', 'N/A'),
                post['status'],
                post['created_at']
            ))
    
    def load_scheduled_posts(self):
        """Load scheduled posts"""
        for item in self.scheduled_tree.get_children():
            self.scheduled_tree.delete(item)
        
        posts = self.db.get_posts('SCHEDULED')
        
        for post in posts:
            content_preview = post['content'][:80] + "..." if len(post['content']) > 80 else post['content']
            self.scheduled_tree.insert('', 'end', values=(
                post['id'],
                content_preview,
                post.get('scheduled_time', 'N/A'),
                post['status']
            ))
    
    def run_scheduler(self):
        """Run the smart scheduler"""
        self.update_status("Ejecutando scheduler...")
        self.log("INFO", "Scheduler iniciado")
        
        def run():
            try:
                due_posts = self.scheduler.get_due_posts()
                
                for post in due_posts:
                    if self.is_logged_in:
                        success = self.automation.publish_post(
                            post['content'],
                            post.get('image_url')
                        )
                        if success:
                            self.db.update_post_status(post['id'], 'PUBLISHED')
                            self.log("INFO", f"Post {post['id']} publicado automáticamente")
                    time.sleep(2)
                
                self.root.after(0, lambda: self.update_status(
                    f"Scheduler completado: {len(due_posts)} posts procesados"))
                self.root.after(0, self.update_dashboard)
                self.root.after(0, self.load_scheduled_posts)
                
            except Exception as e:
                self.root.after(0, lambda: self.update_status(
                    f"Error en scheduler: {str(e)}"))
                self.log("ERROR", f"Error en scheduler: {str(e)}")
        
        threading.Thread(target=run, daemon=True).start()
    
    def test_connection(self):
        """Test LinkedIn connection"""
        self.update_status("Probando conexión...")
        self.connect_linkedin()
    
    def open_linkedin(self):
        """Open LinkedIn in browser"""
        if self.automation:
            self.automation.open_browser()
    
    def save_settings(self):
        """Save all settings"""
        settings = {
            'linkedin_email': self.linkedin_email.get(),
            'linkedin_password': self.linkedin_password.get(),
            'profile_name': self.profile_name.get(),
            'industry': self.industry.get(),
            'topics': self.topics.get(),
            'auto_post': self.auto_post.get(),
            'behavior_level': self.behavior_level.get(),
            'min_delay': self.min_delay.get(),
            'max_delay': self.max_delay.get(),
            'min_posts': self.min_posts.get(),
            'max_posts': self.max_posts.get()
        }
        
        with open('data/settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
        
        self.update_status("Configuración guardada")
        self.log("INFO", "Configuración guardada")
        messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('data/settings.json'):
                with open('data/settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.linkedin_email.set(settings.get('linkedin_email', ''))
                self.linkedin_password.set(settings.get('linkedin_password', ''))
                self.profile_name.set(settings.get('profile_name', 'Software Engineer'))
                self.industry.set(settings.get('industry', 'technology'))
                self.topics.set(settings.get('topics', ''))
                self.auto_post.set(settings.get('auto_post', True))
                self.behavior_level.set(settings.get('behavior_level', 'high'))
                self.min_delay.set(settings.get('min_delay', 2))
                self.max_delay.set(settings.get('max_delay', 15))
                self.min_posts.set(settings.get('min_posts', 3))
                self.max_posts.set(settings.get('max_posts', 5))
                
                self.log("INFO", "Configuración cargada")
        except Exception as e:
            self.log("ERROR", f"Error cargando configuración: {str(e)}")
    
    def save_schedule_settings(self):
        """Save schedule settings"""
        settings = {
            'min_posts': self.min_posts.get(),
            'max_posts': self.max_posts.get(),
            'morning': self.morning_var.get(),
            'afternoon': self.afternoon_var.get(),
            'evening': self.evening_var.get(),
            'weekend': self.weekend_var.get()
        }
        
        with open('data/schedule_settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
        
        self.update_status("Configuración de programación guardada")
        self.log("INFO", "Configuración de programación guardada")
        messagebox.showinfo("Éxito", "Configuración guardada")
    
    def quick_generate(self):
        """Quick generate from dashboard"""
        self.notebook.select(1)  # Switch to content tab
        self.generate_content()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
    
    def log(self, level, message):
        """Add log entry"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        
        # Also log to file
        if level == "INFO":
            logger.info(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "WARNING":
            logger.warning(message)
    
    def refresh_logs(self):
        """Refresh logs display"""
        try:
            with open('logs/app.log', 'r') as f:
                logs = f.read()
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(tk.END, logs)
        except FileNotFoundError:
            self.log("INFO", "No se encontró archivo de logs")
    
    def clear_logs(self):
        """Clear logs display"""
        self.logs_text.delete(1.0, tk.END)
        self.log("INFO", "Logs limpiados")
    
    def export_logs(self):
        """Export logs to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(self.logs_text.get(1.0, tk.END))
            self.log("INFO", f"Logs exportados a {filename}")
    
    # Placeholder methods for treeview actions
    def publish_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            item = self.posts_tree.item(selection[0])
            messagebox.showinfo("Info", f"Publicando post ID: {item['values'][0]}")
    
    def schedule_selected(self):
        selection = self.posts_tree.selection()
        if selection:
            item = self.posts_tree.item(selection[0])
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
    
    def pause_scheduler(self):
        messagebox.showinfo("Info", "Scheduler pausado")
        self.log("INFO", "Scheduler pausado")
    
    def cancel_selected_schedule(self):
        selection = self.scheduled_tree.selection()
        if selection:
            item = self.scheduled_tree.item(selection[0])
            if messagebox.askyesno("Confirmar", "¿Cancelar este post programado?"):
                self.db.delete_post(item['values'][0])
                self.load_scheduled_posts()
                self.update_dashboard()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('data/settings.json'):
                with open('data/settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.linkedin_email.set(settings.get('linkedin_email', ''))
                self.linkedin_password.set(settings.get('linkedin_password', ''))
                self.profile_name.set(settings.get('profile_name', 'Software Engineer'))
                self.industry.set(settings.get('industry', 'technology'))
                self.topics.set(settings.get('topics', ''))
                self.auto_post.set(settings.get('auto_post', True))
                self.behavior_level.set(settings.get('behavior_level', 'high'))
                self.min_delay.set(settings.get('min_delay', 2))
                self.max_delay.set(settings.get('max_delay', 15))
                self.min_posts.set(settings.get('min_posts', 3))
                self.max_posts.set(settings.get('max_posts', 5))
                
                self.log("INFO", "Configuración cargada")
        except Exception as e:
            self.log("ERROR", f"Error cargando configuración: {str(e)}")


def main():
    """Main entry point"""
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Create root window
    root = tk.Tk()
    
    # Set icon if exists
    try:
        root.iconbitmap('assets/icon.ico')
    except:
        pass
    
    # Create and run app
    app = LinkedInAutomationApp(root)
    
    # Handle close
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()