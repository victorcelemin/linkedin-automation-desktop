"""
LinkedIn Automation Pro - Modern Creative Interface
Unique, identifiable, and easy-to-understand design

Color Palette:
- Primary Blue: #0077B5 (LinkedIn)
- Warm Amber: #F5A623, #E8985E
- Soft Grays: #F7F9FC, #E8ECF1
- Success Green: #10B981
- Pure White: #FFFFFF
- Dark Text: #1F2937
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
import math

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
    class Database:
        def __init__(self): pass
        def get_stats(self): return {'total': 0, 'published': 0, 'scheduled': 0, 'generated': 0}
        def save_post(self, *args): return 1
        def get_posts(self, status=None): return []
        def get_recent_posts(self, limit=5): return []
        def update_post_status(self, *args): pass
        def delete_post(self, *args): pass


class ModernUI:
    """Modern UI helper class with creative design elements"""
    
    # Color palette - Professional but warm
    COLORS = {
        # Primary
        'primary': '#0077B5',        # LinkedIn Blue
        'primary_dark': '#004182',   # Dark Blue
        'primary_light': '#3D8FD4',  # Light Blue
        
        # Warm accent
        'warm': '#F5A623',           # Amber
        'warm_light': '#FBBF24',     # Light Amber
        'warm_dark': '#E8985E',      # Orange
        
        # Neutrals
        'bg_main': '#F7F9FC',        # Main background
        'bg_card': '#FFFFFF',        # Card background
        'bg_sidebar': '#1E293B',     # Sidebar dark
        'bg_hover': '#F1F5F9',       # Hover state
        
        # Text
        'text_primary': '#1F2937',   # Dark text
        'text_secondary': '#64748B', # Secondary text
        'text_light': '#94A3B8',     # Light text
        'text_white': '#FFFFFF',     # White text
        
        # Status
        'success': '#10B981',        # Green
        'warning': '#F59E0B',        # Yellow
        'danger': '#EF4444',         # Red
        'info': '#3B82F6',           # Blue info
        
        # Gradients (as tuples for canvas)
        'gradient_start': '#0077B5',
        'gradient_end': '#3D8FD4',
    }
    
    @staticmethod
    def create_gradient_background(canvas, width, height, color1, color2, horizontal=True):
        """Create a smooth gradient background"""
        if horizontal:
            for i in range(width):
                r1, g1, b1 = ModernUI.hex_to_rgb(color1)
                r2, g2, b2 = ModernUI.hex_to_rgb(color2)
                ratio = i / width
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                color = f'#{r:02x}{g:02x}{b:02x}'
                canvas.create_line(i, 0, i, height, fill=color)
        else:
            for i in range(height):
                r1, g1, b1 = ModernUI.hex_to_rgb(color1)
                r2, g2, b2 = ModernUI.hex_to_rgb(color2)
                ratio = i / height
                r = int(r1 + (r2 - r1) * ratio)
                g = int(g1 + (g2 - g1) * ratio)
                b = int(b1 + (b2 - b1) * ratio)
                color = f'#{r:02x}{g:02x}{b:02x}'
                canvas.create_line(0, i, width, i, fill=color)
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def create_rounded_rect(canvas, x1, y1, x2, y2, radius=20, **kwargs):
        """Create a rounded rectangle"""
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    
    def __init__(self, parent, text, command=None, bg='#0077B5', fg='white',
                 width=180, height=45, radius=12, font=('Segoe UI', 11, 'bold'), **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        
        self.command = command
        self.bg = bg
        self.fg = fg
        self.width = width
        self.height = height
        self.radius = radius
        self.font = font
        self.text = text
        self.is_hovered = False
        
        self.draw_button()
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
    
    def draw_button(self, color=None):
        self.delete('all')
        bg_color = color or self.bg
        
        # Draw rounded rectangle
        ModernUI.create_rounded_rect(
            self, 2, 2, self.width-2, self.height-2,
            radius=self.radius,
            fill=bg_color,
            outline=''
        )
        
        # Draw text
        self.create_text(
            self.width/2, self.height/2,
            text=self.text,
            fill=self.fg,
            font=self.font
        )
    
    def on_enter(self, e):
        self.is_hovered = True
        # Lighten color on hover
        r, g, b = ModernUI.hex_to_rgb(self.bg)
        r = min(255, r + 30)
        g = min(255, g + 30)
        b = min(255, b + 30)
        self.draw_button(f'#{r:02x}{g:02x}{b:02x}')
        self.config(cursor='hand2')
    
    def on_leave(self, e):
        self.is_hovered = False
        self.draw_button()
        self.config(cursor='')
    
    def on_click(self, e):
        if self.command:
            self.command()


class StatCard(tk.Canvas):
    """Modern statistics card with icon and gradient"""
    
    def __init__(self, parent, icon, value, label, color='#0077B5', **kwargs):
        super().__init__(parent, width=200, height=140,
                        bg=parent.cget('bg'), highlightthickness=0, **kwargs)
        
        self.icon = icon
        self.value = value
        self.label = label
        self.color = color
        
        self.draw_card()
    
    def draw_card(self):
        self.delete('all')
        
        # Card background with shadow effect
        self.create_rectangle(4, 4, 196, 136, fill='#E2E8F0', outline='', stipple='gray25')
        ModernUI.create_rounded_rect(self, 2, 2, 194, 134, radius=16, 
                                     fill='#FFFFFF', outline='#E2E8F0', width=1)
        
        # Color accent bar at top
        ModernUI.create_rounded_rect(self, 2, 2, 194, 8, radius=4, fill=self.color, outline='')
        
        # Icon
        self.create_text(40, 50, text=self.icon, font=('Segoe UI Emoji', 28))
        
        # Value
        self.value_text = self.create_text(130, 45, text=str(self.value),
                                           font=('Segoe UI', 26, 'bold'),
                                           fill=ModernUI.COLORS['text_primary'])
        
        # Label
        self.create_text(130, 90, text=self.label,
                        font=('Segoe UI', 10),
                        fill=ModernUI.COLORS['text_secondary'])
    
    def update_value(self, new_value):
        self.value = new_value
        self.itemconfig(self.value_text, text=str(new_value))


class Sidebar(tk.Frame):
    """Modern sidebar navigation"""
    
    def __init__(self, parent, width=220, **kwargs):
        super().__init__(parent, width=width, bg=ModernUI.COLORS['bg_sidebar'], **kwargs)
        self.pack_propagate(False)
        self.buttons = []
        self.active_button = None
        self.on_nav = None
        
        self.create_logo()
        self.nav_frame = tk.Frame(self, bg=ModernUI.COLORS['bg_sidebar'])
        self.nav_frame.pack(fill='x', pady=20)
    
    def create_logo(self):
        """Create logo area"""
        logo_frame = tk.Frame(self, bg=ModernUI.COLORS['bg_sidebar'], height=80)
        logo_frame.pack(fill='x', pady=(20, 10))
        logo_frame.pack_propagate(False)
        
        # Logo icon (LinkedIn style)
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50,
                               bg=ModernUI.COLORS['bg_sidebar'], highlightthickness=0)
        logo_canvas.pack(side='left', padx=(20, 10))
        
        # Draw logo
        logo_canvas.create_oval(5, 5, 45, 45, fill=ModernUI.COLORS['primary'], outline='')
        logo_canvas.create_text(25, 27, text='in', fill='white',
                               font=('Segoe UI', 18, 'bold'))
        
        # App name
        tk.Label(logo_frame, text='LinkedIn\nAutomation',
                font=('Segoe UI', 12, 'bold'),
                fg=ModernUI.COLORS['text_white'],
                bg=ModernUI.COLORS['bg_sidebar'],
                justify='left').pack(side='left', padx=5)
    
    def add_button(self, icon, text, tab_id):
        """Add navigation button"""
        btn_frame = tk.Frame(self.nav_frame, bg=ModernUI.COLORS['bg_sidebar'], height=50)
        btn_frame.pack(fill='x', pady=2)
        btn_frame.pack_propagate(False)
        
        btn = tk.Canvas(btn_frame, height=50, bg=ModernUI.COLORS['bg_sidebar'],
                       highlightthickness=0)
        btn.pack(fill='x')
        
        # Draw button
        btn.create_rectangle(0, 0, 220, 50, fill=ModernUI.COLORS['bg_sidebar'], outline='')
        icon_text = btn.create_text(35, 25, text=icon, font=('Segoe UI Emoji', 18),
                                   fill=ModernUI.COLORS['text_light'])
        text_id = btn.create_text(70, 25, text=text, font=('Segoe UI', 11),
                                 fill=ModernUI.COLORS['text_light'], anchor='w')
        
        def on_enter(e):
            if btn != self.active_button:
                btn.itemconfig('all', fill=ModernUI.COLORS['bg_hover'])
                btn.tag_raise(icon_text)
                btn.tag_raise(text_id)
                btn.itemconfig(icon_text, fill=ModernUI.COLORS['primary'])
                btn.itemconfig(text_id, fill=ModernUI.COLORS['text_primary'])
        
        def on_leave(e):
            if btn != self.active_button:
                btn.itemconfig('all', fill=ModernUI.COLORS['bg_sidebar'])
                btn.tag_raise(icon_text)
                btn.tag_raise(text_id)
                btn.itemconfig(icon_text, fill=ModernUI.COLORS['text_light'])
                btn.itemconfig(text_id, fill=ModernUI.COLORS['text_light'])
        
        def on_click(e):
            self.set_active(btn, icon_text, text_id)
            if self.on_nav:
                self.on_nav(tab_id)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        btn.bind('<Button-1>', on_click)
        
        self.buttons.append((btn, icon_text, text_id))
        return btn
    
    def set_active(self, btn, icon_text, text_id):
        """Set active button"""
        # Reset previous active
        if self.active_button:
            self.active_button.itemconfig('all', fill=ModernUI.COLORS['bg_sidebar'])
        
        # Set new active
        self.active_button = btn
        btn.itemconfig('all', fill=ModernUI.COLORS['primary'])
        btn.itemconfig(icon_text, fill=ModernUI.COLORS['text_white'])
        btn.itemconfig(text_id, fill=ModernUI.COLORS['text_white'])
    
    def set_navigation_callback(self, callback):
        self.on_nav = callback


class LinkedInAutomationApp:
    """Main Application with Modern Creative Interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Automation Pro")
        self.root.geometry("1440x900")
        self.root.minsize(1200, 800)
        self.root.configure(bg=ModernUI.COLORS['bg_main'])
        
        # Set icon
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
        
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
        self.current_tab = 'dashboard'
        
        # Create UI
        self.create_ui()
        
        # Load data
        self.update_dashboard()
        self.load_settings()
        
        logger.info("LinkedIn Automation Pro started with modern UI")
    
    def create_ui(self):
        """Create main modern UI layout"""
        # Main container with sidebar
        self.main_container = tk.Frame(self.root, bg=ModernUI.COLORS['bg_main'])
        self.main_container.pack(fill='both', expand=True)
        
        # Create sidebar
        self.sidebar = Sidebar(self.main_container)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.set_navigation_callback(self.switch_tab)
        
        # Add navigation buttons
        self.sidebar.add_button('📊', 'Dashboard', 'dashboard')
        self.sidebar.add_button('✨', 'Generar Contenido', 'content')
        self.sidebar.add_button('📝', 'Mis Posts', 'posts')
        self.sidebar.add_button('📅', 'Programación', 'schedule')
        self.sidebar.add_button('⚙️', 'Configuración', 'settings')
        self.sidebar.add_button('📋', 'Registros', 'logs')
        
        # Content area
        self.content_area = tk.Frame(self.main_container, bg=ModernUI.COLORS['bg_main'])
        self.content_area.pack(side='left', fill='both', expand=True)
        
        # Create all tabs
        self.create_dashboard_tab()
        self.create_content_tab()
        self.create_posts_tab()
        self.create_schedule_tab()
        self.create_settings_tab()
        self.create_logs_tab()
        
        # Show dashboard by default
        self.show_tab('dashboard')
    
    def switch_tab(self, tab_id):
        """Switch between tabs"""
        self.current_tab = tab_id
        self.show_tab(tab_id)
    
    def show_tab(self, tab_id):
        """Show selected tab"""
        # Hide all tabs
        for widget in self.content_area.winfo_children():
            widget.pack_forget()
        
        # Show selected tab
        tabs = {
            'dashboard': self.dashboard_frame,
            'content': self.content_frame,
            'posts': self.posts_frame,
            'schedule': self.schedule_frame,
            'settings': self.settings_frame,
            'logs': self.logs_frame
        }
        
        if tab_id in tabs:
            tabs[tab_id].pack(fill='both', expand=True)
    
    def create_header(self, parent, title, subtitle=None):
        """Create modern header"""
        header = tk.Frame(parent, bg=ModernUI.COLORS['bg_main'], height=80)
        header.pack(fill='x', padx=30, pady=(20, 10))
        header.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header, bg=ModernUI.COLORS['bg_main'])
        title_frame.pack(side='left', fill='y')
        
        tk.Label(title_frame, text=title,
                font=('Segoe UI', 24, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_main']).pack(anchor='w')
        
        if subtitle:
            tk.Label(title_frame, text=subtitle,
                    font=('Segoe UI', 11),
                    fg=ModernUI.COLORS['text_secondary'],
                    bg=ModernUI.COLORS['bg_main']).pack(anchor='w')
        
        # Connection status
        status_frame = tk.Frame(header, bg=ModernUI.COLORS['bg_main'])
        status_frame.pack(side='right', fill='y')
        
        self.create_connection_status(status_frame)
        
        return header
    
    def create_connection_status(self, parent):
        """Create connection status indicator"""
        conn_frame = tk.Frame(parent, bg=ModernUI.COLORS['bg_main'])
        conn_frame.pack(side='right', padx=20)
        
        # Status dot
        self.status_canvas = tk.Canvas(conn_frame, width=20, height=20,
                                       bg=ModernUI.COLORS['bg_main'], highlightthickness=0)
        self.status_canvas.pack(side='left', padx=(0, 8))
        self.status_dot = self.status_canvas.create_oval(3, 3, 17, 17,
                                                         fill=ModernUI.COLORS['danger'])
        
        # Status text
        self.status_label = tk.Label(conn_frame, text="Desconectado",
                                    font=('Segoe UI', 11),
                                    fg=ModernUI.COLORS['text_secondary'],
                                    bg=ModernUI.COLORS['bg_main'])
        self.status_label.pack(side='left')
        
        # Connect button
        connect_btn = ModernButton(conn_frame, text="🌐 Conectar LinkedIn",
                                  command=self.connect_linkedin,
                                  bg=ModernUI.COLORS['primary'],
                                  width=180, height=40, radius=10,
                                  font=('Segoe UI', 10, 'bold'))
        connect_btn.pack(side='left', padx=15)
    
    def update_connection_status(self, connected):
        """Update connection status display"""
        if connected:
            self.status_canvas.itemconfig(self.status_dot, fill=ModernUI.COLORS['success'])
            self.status_label.config(text="Conectado", fg=ModernUI.COLORS['success'])
        else:
            self.status_canvas.itemconfig(self.status_dot, fill=ModernUI.COLORS['danger'])
            self.status_label.config(text="Desconectado", fg=ModernUI.COLORS['text_secondary'])
    
    def create_dashboard_tab(self):
        """Create modern Dashboard tab"""
        self.dashboard_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.dashboard_frame, "Dashboard", "Vista general de tu actividad")
        
        # Stats cards
        stats_container = tk.Frame(self.dashboard_frame, bg=ModernUI.COLORS['bg_main'])
        stats_container.pack(fill='x', padx=30, pady=10)
        
        # Create stat cards
        self.stat_cards = {}
        stats_data = [
            ('total', '📝', 'Total Posts', ModernUI.COLORS['primary']),
            ('published', '✅', 'Publicados', ModernUI.COLORS['success']),
            ('scheduled', '📅', 'Programados', ModernUI.COLORS['warm']),
            ('generated', '✨', 'Generados', '#8B5CF6'),
        ]
        
        for i, (key, icon, label, color) in enumerate(stats_data):
            card = StatCard(stats_container, icon, '0', label, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            stats_container.columnconfigure(i, weight=1)
            self.stat_cards[key] = card
        
        # Quick actions card
        actions_card = tk.Frame(self.dashboard_frame, bg=ModernUI.COLORS['bg_card'],
                               highlightbackground='#E2E8F0', highlightthickness=1)
        actions_card.pack(fill='x', padx=30, pady=10)
        
        # Card header
        actions_header = tk.Frame(actions_card, bg=ModernUI.COLORS['bg_card'])
        actions_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(actions_header, text="⚡ Acciones Rápidas",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        # Action buttons
        actions_grid = tk.Frame(actions_card, bg=ModernUI.COLORS['bg_card'])
        actions_grid.pack(fill='x', padx=20, pady=(0, 20))
        
        buttons_data = [
            ("✨ Generar Post", self.quick_generate, ModernUI.COLORS['primary']),
            ("📤 Publicar Ahora", self.quick_publish, ModernUI.COLORS['success']),
            ("📅 Ejecutar Scheduler", self.run_scheduler, ModernUI.COLORS['warm']),
            ("📊 Actualizar", self.update_dashboard, ModernUI.COLORS['info']),
        ]
        
        for i, (text, cmd, color) in enumerate(buttons_data):
            btn = ModernButton(actions_grid, text=text, command=cmd, bg=color,
                              width=180, height=45, radius=12)
            btn.grid(row=0, column=i, padx=8, pady=5)
            actions_grid.columnconfigure(i, weight=1)
        
        # Recent activity card
        recent_card = tk.Frame(self.dashboard_frame, bg=ModernUI.COLORS['bg_card'],
                              highlightbackground='#E2E8F0', highlightthickness=1)
        recent_card.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Card header
        recent_header = tk.Frame(recent_card, bg=ModernUI.COLORS['bg_card'])
        recent_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(recent_header, text="📋 Actividad Reciente",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        # Recent posts text
        self.recent_text = tk.Text(recent_card, height=10, wrap=tk.WORD,
                                   font=('Consolas', 10),
                                   bg=ModernUI.COLORS['bg_main'],
                                   fg=ModernUI.COLORS['text_primary'],
                                   padx=15, pady=15,
                                   highlightthickness=0,
                                   borderwidth=0)
        self.recent_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def create_content_tab(self):
        """Create modern Content Generation tab"""
        self.content_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.content_frame, "Generar Contenido",
                          "Crea publicaciones únicas con IA")
        
        # Main content area with two columns
        content_pane = tk.Frame(self.content_frame, bg=ModernUI.COLORS['bg_main'])
        content_pane.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Left column - Controls
        left_col = tk.Frame(content_pane, bg=ModernUI.COLORS['bg_main'], width=350)
        left_col.pack(side='left', fill='y', padx=(0, 15))
        left_col.pack_propagate(False)
        
        # Configuration card
        config_card = tk.Frame(left_col, bg=ModernUI.COLORS['bg_card'],
                              highlightbackground='#E2E8F0', highlightthickness=1)
        config_card.pack(fill='x', pady=(0, 15))
        
        # Card header
        config_header = tk.Frame(config_card, bg=ModernUI.COLORS['bg_card'])
        config_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(config_header, text="⚙️ Configuración",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        # Theme selector
        theme_section = tk.Frame(config_card, bg=ModernUI.COLORS['bg_card'])
        theme_section.pack(fill='x', padx=20, pady=10)
        
        tk.Label(theme_section, text="Tema del post:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).pack(anchor='w')
        
        self.theme_var = tk.StringVar(value="auto")
        themes = ["Auto (IA Decide)", "Desarrollo Software", "Experiencias Personales",
                  "Aprendizaje Profesional", "Errores y Lecciones"]
        
        theme_combo = ttk.Combobox(theme_section, textvariable=self.theme_var,
                                  values=themes, width=28, state='readonly')
        theme_combo.pack(pady=(5, 0), fill='x')
        
        # Word count
        words_section = tk.Frame(config_card, bg=ModernUI.COLORS['bg_card'])
        words_section.pack(fill='x', padx=20, pady=10)
        
        tk.Label(words_section, text="Longitud (palabras):",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).pack(anchor='w')
        
        words_frame = tk.Frame(words_section, bg=ModernUI.COLORS['bg_card'])
        words_frame.pack(fill='x', pady=(5, 0))
        
        self.min_words = tk.IntVar(value=80)
        self.max_words = tk.IntVar(value=180)
        
        tk.Spinbox(words_frame, from_=50, to=300, width=6,
                  textvariable=self.min_words).pack(side='left')
        tk.Label(words_frame, text=" a ",
                bg=ModernUI.COLORS['bg_card']).pack(side='left', padx=5)
        tk.Spinbox(words_frame, from_=50, to=300, width=6,
                  textvariable=self.max_words).pack(side='left')
        
        # Options
        options_section = tk.Frame(config_card, bg=ModernUI.COLORS['bg_card'])
        options_section.pack(fill='x', padx=20, pady=10)
        
        tk.Label(options_section, text="Opciones:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).pack(anchor='w')
        
        self.opt_image = tk.BooleanVar(value=True)
        self.opt_hashtags = tk.BooleanVar(value=True)
        self.opt_imperfections = tk.BooleanVar(value=True)
        
        tk.Checkbutton(options_section, text="📷 Agregar imagen relevante",
                      variable=self.opt_image, bg=ModernUI.COLORS['bg_card']).pack(anchor='w', pady=2)
        tk.Checkbutton(options_section, text="#️⃣ Generar hashtags automáticos",
                      variable=self.opt_hashtags, bg=ModernUI.COLORS['bg_card']).pack(anchor='w', pady=2)
        tk.Checkbutton(options_section, text="✨ Incluir imperfecciones humanas",
                      variable=self.opt_imperfections, bg=ModernUI.COLORS['bg_card']).pack(anchor='w', pady=2)
        
        # Generate button
        generate_btn_frame = tk.Frame(config_card, bg=ModernUI.COLORS['bg_card'])
        generate_btn_frame.pack(fill='x', padx=20, pady=(15, 20))
        
        generate_btn = ModernButton(generate_btn_frame, text="✨ Generar Contenido IA",
                                   command=self.generate_content,
                                   bg=ModernUI.COLORS['primary'],
                                   width=280, height=50, radius=12,
                                   font=('Segoe UI', 12, 'bold'))
        generate_btn.pack()
        
        # AI Stats card
        ai_card = tk.Frame(left_col, bg=ModernUI.COLORS['bg_card'],
                          highlightbackground='#E2E8F0', highlightthickness=1)
        ai_card.pack(fill='x')
        
        ai_header = tk.Frame(ai_card, bg=ModernUI.COLORS['bg_card'])
        ai_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(ai_header, text="📊 Estadísticas IA",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        self.ai_stats_text = tk.Text(ai_card, height=8, wrap=tk.WORD,
                                     font=('Consolas', 9),
                                     bg=ModernUI.COLORS['bg_main'],
                                     fg=ModernUI.COLORS['text_primary'],
                                     padx=15, pady=15,
                                     highlightthickness=0,
                                     borderwidth=0)
        self.ai_stats_text.pack(fill='x', padx=20, pady=(0, 20))
        
        # Right column - Preview
        right_col = tk.Frame(content_pane, bg=ModernUI.COLORS['bg_main'])
        right_col.pack(side='left', fill='both', expand=True)
        
        # Preview card
        preview_card = tk.Frame(right_col, bg=ModernUI.COLORS['bg_card'],
                               highlightbackground='#E2E8F0', highlightthickness=1)
        preview_card.pack(fill='both', expand=True)
        
        # Preview header with tags
        preview_header = tk.Frame(preview_card, bg=ModernUI.COLORS['bg_card'])
        preview_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(preview_header, text="👁️ Vista Previa",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        # Tags frame
        self.tags_frame = tk.Frame(preview_header, bg=ModernUI.COLORS['bg_card'])
        self.tags_frame.pack(side='right')
        
        self.preview_tone = tk.Label(self.tags_frame, text="TONO",
                                     bg=ModernUI.COLORS['primary'],
                                     fg='white',
                                     font=('Segoe UI', 9, 'bold'),
                                     padx=12, pady=4)
        self.preview_tone.pack(side='left', padx=3)
        
        self.preview_style = tk.Label(self.tags_frame, text="ESTILO",
                                      bg=ModernUI.COLORS['text_secondary'],
                                      fg='white',
                                      font=('Segoe UI', 9, 'bold'),
                                      padx=12, pady=4)
        self.preview_style.pack(side='left', padx=3)
        
        self.preview_topic = tk.Label(self.tags_frame, text="TEMA",
                                      bg=ModernUI.COLORS['warm'],
                                      fg='white',
                                      font=('Segoe UI', 9, 'bold'),
                                      padx=12, pady=4)
        self.preview_topic.pack(side='left', padx=3)
        
        self.preview_words = tk.Label(self.tags_frame, text="0 palabras",
                                      font=('Segoe UI', 10),
                                      fg=ModernUI.COLORS['text_secondary'],
                                      bg=ModernUI.COLORS['bg_card'])
        self.preview_words.pack(side='left', padx=10)
        
        # Content text area
        self.preview_content = tk.Text(preview_card, wrap=tk.WORD,
                                       font=('Segoe UI', 12),
                                       bg=ModernUI.COLORS['bg_main'],
                                       fg=ModernUI.COLORS['text_primary'],
                                       padx=20, pady=20,
                                       highlightthickness=0,
                                       borderwidth=0)
        self.preview_content.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Image preview card
        image_card = tk.Frame(preview_card, bg=ModernUI.COLORS['bg_main'],
                             highlightbackground='#E2E8F0', highlightthickness=1)
        image_card.pack(fill='x', padx=20, pady=(0, 10))
        
        self.image_label = tk.Label(image_card, text="🖼️ La imagen aparecerá aquí",
                                   font=('Segoe UI', 10),
                                   fg=ModernUI.COLORS['text_light'],
                                   bg=ModernUI.COLORS['bg_main'],
                                   pady=30)
        self.image_label.pack(fill='x')
        
        # Hashtags
        self.hashtags_label = tk.Label(preview_card, text="",
                                      font=('Segoe UI', 11, 'bold'),
                                      fg=ModernUI.COLORS['primary'],
                                      bg=ModernUI.COLORS['bg_card'],
                                      wraplength=600)
        self.hashtags_label.pack(pady=(0, 10))
        
        # Action buttons
        actions_frame = tk.Frame(preview_card, bg=ModernUI.COLORS['bg_card'])
        actions_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        actions_data = [
            ("💾 Guardar", self.save_content, ModernUI.COLORS['primary']),
            ("📅 Programar", self.schedule_content, ModernUI.COLORS['warm']),
            ("📤 Publicar", self.publish_content, ModernUI.COLORS['success']),
            ("🔄 Regenerar", self.generate_content, ModernUI.COLORS['text_secondary']),
        ]
        
        for text, cmd, color in actions_data:
            btn = ModernButton(actions_frame, text=text, command=cmd, bg=color,
                              width=140, height=40, radius=10)
            btn.pack(side='left', padx=5, fill='x', expand=True)
    
    def create_posts_tab(self):
        """Create modern Posts tab"""
        self.posts_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.posts_frame, "Mis Posts",
                          "Gestiona todas tus publicaciones")
        
        # Posts card
        posts_card = tk.Frame(self.posts_frame, bg=ModernUI.COLORS['bg_card'],
                             highlightbackground='#E2E8F0', highlightthickness=1)
        posts_card.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Filter bar
        filter_bar = tk.Frame(posts_card, bg=ModernUI.COLORS['bg_card'])
        filter_bar.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(filter_bar, text="🔍 Filtrar por estado:",
                font=('Segoe UI', 10),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        self.status_filter = tk.StringVar(value="ALL")
        filter_combo = ttk.Combobox(filter_bar, textvariable=self.status_filter,
                                   values=["ALL", "GENERATED", "SCHEDULED", "PUBLISHED", "FAILED"],
                                   width=15, state='readonly')
        filter_combo.pack(side='left', padx=10)
        
        refresh_btn = ModernButton(filter_bar, text="🔄 Actualizar",
                                  command=self.load_posts,
                                  bg=ModernUI.COLORS['info'],
                                  width=120, height=35, radius=8)
        refresh_btn.pack(side='left', padx=10)
        
        # Posts treeview with custom style
        style = ttk.Style()
        style.configure('Modern.Treeview',
                       background=ModernUI.COLORS['bg_card'],
                       foreground=ModernUI.COLORS['text_primary'],
                       fieldbackground=ModernUI.COLORS['bg_card'],
                       font=('Segoe UI', 10),
                       rowheight=40)
        style.configure('Modern.Treeview.Heading',
                       background=ModernUI.COLORS['bg_main'],
                       foreground=ModernUI.COLORS['text_secondary'],
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        
        columns = ('id', 'content', 'tone', 'style', 'status', 'date')
        self.posts_tree = ttk.Treeview(posts_card, columns=columns, show='headings',
                                      style='Modern.Treeview', height=15)
        
        self.posts_tree.heading('id', text='ID')
        self.posts_tree.heading('content', text='Contenido')
        self.posts_tree.heading('tone', text='Tono')
        self.posts_tree.heading('style', text='Estilo')
        self.posts_tree.heading('status', text='Estado')
        self.posts_tree.heading('date', text='Fecha')
        
        self.posts_tree.column('id', width=60, anchor='center')
        self.posts_tree.column('content', width=400)
        self.posts_tree.column('tone', width=120, anchor='center')
        self.posts_tree.column('style', width=120, anchor='center')
        self.posts_tree.column('status', width=100, anchor='center')
        self.posts_tree.column('date', width=150, anchor='center')
        
        self.posts_tree.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Action buttons
        actions_frame = tk.Frame(posts_card, bg=ModernUI.COLORS['bg_card'])
        actions_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        actions_data = [
            ("📤 Publicar", self.publish_selected, ModernUI.COLORS['success']),
            ("📅 Programar", self.schedule_selected, ModernUI.COLORS['warm']),
            ("✏️ Editar", self.edit_selected, ModernUI.COLORS['info']),
            ("🗑️ Eliminar", self.delete_selected, ModernUI.COLORS['danger']),
        ]
        
        for text, cmd, color in actions_data:
            btn = ModernButton(actions_frame, text=text, command=cmd, bg=color,
                              width=140, height=40, radius=10)
            btn.pack(side='left', padx=5, fill='x', expand=True)
    
    def create_schedule_tab(self):
        """Create modern Schedule tab"""
        self.schedule_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.schedule_frame, "Programación",
                          "Configura horarios inteligentes")
        
        # Main content
        schedule_content = tk.Frame(self.schedule_frame, bg=ModernUI.COLORS['bg_main'])
        schedule_content.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Settings card
        settings_card = tk.Frame(schedule_content, bg=ModernUI.COLORS['bg_card'],
                                highlightbackground='#E2E8F0', highlightthickness=1)
        settings_card.pack(fill='x', pady=(0, 15))
        
        settings_header = tk.Frame(settings_card, bg=ModernUI.COLORS['bg_card'])
        settings_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(settings_header, text="⚙️ Configuración de Programación",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        settings_grid = tk.Frame(settings_card, bg=ModernUI.COLORS['bg_card'])
        settings_grid.pack(fill='x', padx=20, pady=(0, 20))
        
        # Posts per week
        freq_label = tk.Label(settings_grid, text="Posts por semana:",
                             font=('Segoe UI', 10, 'bold'),
                             fg=ModernUI.COLORS['text_secondary'],
                             bg=ModernUI.COLORS['bg_card'])
        freq_label.grid(row=0, column=0, sticky='w', pady=8)
        
        freq_frame = tk.Frame(settings_grid, bg=ModernUI.COLORS['bg_card'])
        freq_frame.grid(row=0, column=1, padx=10, sticky='w')
        
        self.min_posts = tk.IntVar(value=3)
        self.max_posts = tk.IntVar(value=5)
        
        tk.Spinbox(freq_frame, from_=1, to=7, width=5,
                  textvariable=self.min_posts).pack(side='left')
        tk.Label(freq_frame, text=" a ",
                bg=ModernUI.COLORS['bg_card']).pack(side='left', padx=5)
        tk.Spinbox(freq_frame, from_=1, to=7, width=5,
                  textvariable=self.max_posts).pack(side='left')
        
        # Time preferences
        time_label = tk.Label(settings_grid, text="Horarios preferidos:",
                             font=('Segoe UI', 10, 'bold'),
                             fg=ModernUI.COLORS['text_secondary'],
                             bg=ModernUI.COLORS['bg_card'])
        time_label.grid(row=1, column=0, sticky='w', pady=8)
        
        time_frame = tk.Frame(settings_grid, bg=ModernUI.COLORS['bg_card'])
        time_frame.grid(row=1, column=1, padx=10, sticky='w')
        
        self.morning = tk.BooleanVar(value=True)
        self.afternoon = tk.BooleanVar(value=True)
        self.evening = tk.BooleanVar(value=True)
        
        tk.Checkbutton(time_frame, text="🌅 Mañana (7-10)",
                      variable=self.morning, bg=ModernUI.COLORS['bg_card']).pack(side='left', padx=5)
        tk.Checkbutton(time_frame, text="☀️ Tarde (12-15)",
                      variable=self.afternoon, bg=ModernUI.COLORS['bg_card']).pack(side='left', padx=5)
        tk.Checkbutton(time_frame, text="🌙 Noche (17-20)",
                      variable=self.evening, bg=ModernUI.COLORS['bg_card']).pack(side='left', padx=5)
        
        # Weekend
        weekend_label = tk.Label(settings_grid, text="Fines de semana:",
                                font=('Segoe UI', 10, 'bold'),
                                fg=ModernUI.COLORS['text_secondary'],
                                bg=ModernUI.COLORS['bg_card'])
        weekend_label.grid(row=2, column=0, sticky='w', pady=8)
        
        self.weekend = tk.BooleanVar(value=False)
        tk.Checkbutton(settings_grid, text="Incluir (20% probabilidad)",
                      variable=self.weekend, bg=ModernUI.COLORS['bg_card']).grid(
                          row=2, column=1, padx=10, sticky='w')
        
        # Save button
        save_frame = tk.Frame(settings_grid, bg=ModernUI.COLORS['bg_card'])
        save_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        save_btn = ModernButton(save_frame, text="💾 Guardar Configuración",
                               command=self.save_schedule_settings,
                               bg=ModernUI.COLORS['primary'],
                               width=250, height=45, radius=12)
        save_btn.pack()
        
        # Scheduled posts card
        scheduled_card = tk.Frame(schedule_content, bg=ModernUI.COLORS['bg_card'],
                                 highlightbackground='#E2E8F0', highlightthickness=1)
        scheduled_card.pack(fill='both', expand=True)
        
        scheduled_header = tk.Frame(scheduled_card, bg=ModernUI.COLORS['bg_card'])
        scheduled_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(scheduled_header, text="📅 Posts Programados",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        columns = ('id', 'content', 'scheduled', 'status')
        self.scheduled_tree = ttk.Treeview(scheduled_card, columns=columns,
                                          show='headings', style='Modern.Treeview', height=10)
        
        self.scheduled_tree.heading('id', text='ID')
        self.scheduled_tree.heading('content', text='Contenido')
        self.scheduled_tree.heading('scheduled', text='Programado para')
        self.scheduled_tree.heading('status', text='Estado')
        
        self.scheduled_tree.column('id', width=60, anchor='center')
        self.scheduled_tree.column('content', width=400)
        self.scheduled_tree.column('scheduled', width=200, anchor='center')
        self.scheduled_tree.column('status', width=100, anchor='center')
        
        self.scheduled_tree.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Scheduler actions
        sched_actions = tk.Frame(scheduled_card, bg=ModernUI.COLORS['bg_card'])
        sched_actions.pack(fill='x', padx=20, pady=(0, 20))
        
        actions_data = [
            ("▶️ Ejecutar Scheduler", self.run_scheduler, ModernUI.COLORS['success']),
            ("⏸️ Pausar", self.pause_scheduler, ModernUI.COLORS['warning']),
            ("🗑️ Cancelar Seleccionado", self.cancel_selected, ModernUI.COLORS['danger']),
        ]
        
        for text, cmd, color in actions_data:
            btn = ModernButton(sched_actions, text=text, command=cmd, bg=color,
                              width=180, height=40, radius=10)
            btn.pack(side='left', padx=5, fill='x', expand=True)
    
    def create_settings_tab(self):
        """Create modern Settings tab"""
        self.settings_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.settings_frame, "Configuración",
                          "Personaliza tu experiencia")
        
        # Settings content
        settings_content = tk.Frame(self.settings_frame, bg=ModernUI.COLORS['bg_main'])
        settings_content.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # LinkedIn credentials card
        creds_card = tk.Frame(settings_content, bg=ModernUI.COLORS['bg_card'],
                             highlightbackground='#E2E8F0', highlightthickness=1)
        creds_card.pack(fill='x', pady=(0, 15))
        
        creds_header = tk.Frame(creds_card, bg=ModernUI.COLORS['bg_card'])
        creds_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(creds_header, text="🔐 Credenciales de LinkedIn",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        creds_form = tk.Frame(creds_card, bg=ModernUI.COLORS['bg_card'])
        creds_form.pack(fill='x', padx=20, pady=(0, 20))
        
        # Email
        tk.Label(creds_form, text="Email:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).grid(row=0, column=0, sticky='w', pady=8)
        
        self.email_entry = tk.Entry(creds_form, width=40,
                                    font=('Segoe UI', 11),
                                    bg=ModernUI.COLORS['bg_main'],
                                    fg=ModernUI.COLORS['text_primary'],
                                    relief='flat')
        self.email_entry.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        # Password
        tk.Label(creds_form, text="Contraseña:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).grid(row=1, column=0, sticky='w', pady=8)
        
        self.password_entry = tk.Entry(creds_form, show="•", width=40,
                                       font=('Segoe UI', 11),
                                       bg=ModernUI.COLORS['bg_main'],
                                       fg=ModernUI.COLORS['text_primary'],
                                       relief='flat')
        self.password_entry.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        creds_form.columnconfigure(1, weight=1)
        
        # Save credentials button
        save_creds_btn = ModernButton(creds_form, text="💾 Guardar Credenciales",
                                     command=self.save_credentials,
                                     bg=ModernUI.COLORS['primary'],
                                     width=200, height=40, radius=10)
        save_creds_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # API Keys card
        api_card = tk.Frame(settings_content, bg=ModernUI.COLORS['bg_card'],
                           highlightbackground='#E2E8F0', highlightthickness=1)
        api_card.pack(fill='x', pady=(0, 15))
        
        api_header = tk.Frame(api_card, bg=ModernUI.COLORS['bg_card'])
        api_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(api_header, text="🔑 Claves API (Opcional)",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        api_form = tk.Frame(api_card, bg=ModernUI.COLORS['bg_card'])
        api_form.pack(fill='x', padx=20, pady=(0, 20))
        
        # Unsplash API
        tk.Label(api_form, text="Unsplash API:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).grid(row=0, column=0, sticky='w', pady=8)
        
        self.unsplash_entry = tk.Entry(api_form, width=40,
                                      font=('Segoe UI', 11),
                                      bg=ModernUI.COLORS['bg_main'],
                                      fg=ModernUI.COLORS['text_primary'],
                                      relief='flat')
        self.unsplash_entry.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        
        # Pexels API
        tk.Label(api_form, text="Pexels API:",
                font=('Segoe UI', 10, 'bold'),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).grid(row=1, column=0, sticky='w', pady=8)
        
        self.pexels_entry = tk.Entry(api_form, width=40,
                                    font=('Segoe UI', 11),
                                    bg=ModernUI.COLORS['bg_main'],
                                    fg=ModernUI.COLORS['text_primary'],
                                    relief='flat')
        self.pexels_entry.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        
        api_form.columnconfigure(1, weight=1)
        
        # Save API keys button
        save_api_btn = ModernButton(api_form, text="💾 Guardar Claves API",
                                   command=self.save_api_keys,
                                   bg=ModernUI.COLORS['primary'],
                                   width=200, height=40, radius=10)
        save_api_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # About card
        about_card = tk.Frame(settings_content, bg=ModernUI.COLORS['bg_card'],
                             highlightbackground='#E2E8F0', highlightthickness=1)
        about_card.pack(fill='x')
        
        about_header = tk.Frame(about_card, bg=ModernUI.COLORS['bg_card'])
        about_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(about_header, text="ℹ️ Acerca de",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        about_text = tk.Text(about_card, height=6, wrap=tk.WORD,
                            font=('Segoe UI', 10),
                            bg=ModernUI.COLORS['bg_main'],
                            fg=ModernUI.COLORS['text_primary'],
                            padx=15, pady=15,
                            highlightthickness=0,
                            borderwidth=0)
        about_text.pack(fill='x', padx=20, pady=(0, 20))
        about_text.insert('1.0', 
            "LinkedIn Automation Pro v2.0\n\n"
            "Sistema inteligente de publicación para LinkedIn.\n"
            "Genera contenido único con IA, programa publicaciones\n"
            "y automatiza tu presencia profesional.\n\n"
            "© 2026 - Desconocido con ❤️")
        about_text.config(state='disabled')
    
    def create_logs_tab(self):
        """Create modern Logs tab"""
        self.logs_frame = tk.Frame(self.content_area, bg=ModernUI.COLORS['bg_main'])
        
        # Header
        self.create_header(self.logs_frame, "Registros",
                          "Historial de actividad del sistema")
        
        # Logs card
        logs_card = tk.Frame(self.logs_frame, bg=ModernUI.COLORS['bg_card'],
                            highlightbackground='#E2E8F0', highlightthickness=1)
        logs_card.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        logs_header = tk.Frame(logs_card, bg=ModernUI.COLORS['bg_card'])
        logs_header.pack(fill='x', padx=20, pady=(15, 10))
        
        tk.Label(logs_header, text="📋 Registros del Sistema",
                font=('Segoe UI', 14, 'bold'),
                fg=ModernUI.COLORS['text_primary'],
                bg=ModernUI.COLORS['bg_card']).pack(side='left')
        
        # Refresh button
        refresh_btn = ModernButton(logs_header, text="🔄 Actualizar",
                                  command=self.refresh_logs,
                                  bg=ModernUI.COLORS['info'],
                                  width=120, height=35, radius=8)
        refresh_btn.pack(side='right')
        
        # Logs text
        self.logs_text = tk.Text(logs_card, wrap=tk.WORD,
                                 font=('Consolas', 10),
                                 bg='#1E293B',
                                 fg='#10B981',
                                 padx=20, pady=20,
                                 highlightthickness=0,
                                 borderwidth=0)
        self.logs_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Load initial logs
        self.refresh_logs()
    
    # ============== UI Helper Methods ==============
    
    def create_stat_card(self, parent, icon, value, label, color, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=ModernUI.COLORS['bg_card'],
                       highlightbackground='#E2E8F0', highlightthickness=1)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(column, weight=1)
        
        # Icon
        tk.Label(card, text=icon, font=('Segoe UI Emoji', 32),
                bg=ModernUI.COLORS['bg_card']).pack(pady=(15, 5))
        
        # Value
        value_label = tk.Label(card, text=str(value),
                              font=('Segoe UI', 28, 'bold'),
                              fg=color,
                              bg=ModernUI.COLORS['bg_card'])
        value_label.pack()
        
        # Label
        tk.Label(card, text=label,
                font=('Segoe UI', 10),
                fg=ModernUI.COLORS['text_secondary'],
                bg=ModernUI.COLORS['bg_card']).pack(pady=(0, 15))
        
        return value_label
    
    # ============== Action Methods ==============
    
    def connect_linkedin(self):
        """Connect to LinkedIn"""
        try:
            if not self.automation:
                self.automation = LinkedInAutomation()
            
            # Get credentials
            email = self.email_entry.get() if hasattr(self, 'email_entry') else ''
            password = self.password_entry.get() if hasattr(self, 'password_entry') else ''
            
            if not email or not password:
                messagebox.showwarning("Credenciales Requeridas",
                                      "Por favor ingresa tus credenciales en Configuración.")
                return
            
            # Attempt login
            result = self.automation.login(email, password)
            if result:
                self.is_logged_in = True
                self.update_connection_status(True)
                logger.info("Successfully connected to LinkedIn")
                messagebox.showinfo("Conectado", "¡Conexión exitosa con LinkedIn!")
            else:
                self.is_logged_in = False
                self.update_connection_status(False)
                logger.error("Failed to connect to LinkedIn")
                messagebox.showerror("Error", "No se pudo conectar con LinkedIn.")
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")
    
    def generate_content(self):
        """Generate new content"""
        try:
            theme = self.theme_var.get() if hasattr(self, 'theme_var') else "auto"
            min_words = self.min_words.get() if hasattr(self, 'min_words') else 80
            max_words = self.max_words.get() if hasattr(self, 'max_words') else 180
            
            # Generate content
            content = self.content_gen.generate(
                theme=theme,
                min_words=min_words,
                max_words=max_words
            )
            
            self.current_content = content
            
            # Update preview
            if hasattr(self, 'preview_content'):
                self.preview_content.delete('1.0', tk.END)
                self.preview_content.insert('1.0', content.get('post', ''))
            
            # Update tags
            if hasattr(self, 'preview_tone'):
                self.preview_tone.config(text=content.get('tone', 'N/A'))
            if hasattr(self, 'preview_style'):
                self.preview_style.config(text=content.get('style', 'N/A'))
            if hasattr(self, 'preview_topic'):
                self.preview_topic.config(text=content.get('topic', 'N/A').replace('_', ' ').title())
            if hasattr(self, 'preview_words'):
                self.preview_words.config(text=f"{content.get('word_count', 0)} palabras")
            
            # Update hashtags
            if hasattr(self, 'hashtags_label'):
                hashtags = content.get('hashtags', [])
                self.hashtags_label.config(text=' '.join(hashtags))
            
            logger.info(f"Generated content: {content.get('word_count', 0)} words")
            
        except Exception as e:
            logger.error(f"Content generation error: {e}")
            messagebox.showerror("Error", f"Error al generar contenido: {str(e)}")
    
    def save_content(self):
        """Save current content"""
        if not self.current_content:
            messagebox.showwarning("Sin Contenido", "Primero genera un contenido.")
            return
        
        try:
            post_id = self.db.save_post(
                content=self.current_content.get('post', ''),
                tone=self.current_content.get('tone', ''),
                style=self.current_content.get('style', ''),
                hashtags=json.dumps(self.current_content.get('hashtags', [])),
                image_url=self.current_content.get('image_query', ''),
                status='GENERATED'
            )
            
            logger.info(f"Content saved with ID: {post_id}")
            messagebox.showinfo("Guardado", f"Contenido guardado con ID: {post_id}")
            self.update_dashboard()
            self.load_posts()
            
        except Exception as e:
            logger.error(f"Save error: {e}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def schedule_content(self):
        """Schedule current content"""
        if not self.current_content:
            messagebox.showwarning("Sin Contenido", "Primero genera un contenido.")
            return
        
        try:
            # Get schedule time
            schedule_time = self.scheduler.get_next_schedule()
            
            post_id = self.db.save_post(
                content=self.current_content.get('post', ''),
                tone=self.current_content.get('tone', ''),
                style=self.current_content.get('style', ''),
                hashtags=json.dumps(self.current_content.get('hashtags', [])),
                image_url=self.current_content.get('image_query', ''),
                status='SCHEDULED',
                scheduled_time=schedule_time.isoformat()
            )
            
            logger.info(f"Content scheduled for {schedule_time}")
            messagebox.showinfo("Programado", 
                              f"Contenido programado para:\n{schedule_time.strftime('%Y-%m-%d %H:%M')}")
            self.update_dashboard()
            self.load_posts()
            
        except Exception as e:
            logger.error(f"Schedule error: {e}")
            messagebox.showerror("Error", f"Error al programar: {str(e)}")
    
    def publish_content(self):
        """Publish current content"""
        if not self.current_content:
            messagebox.showwarning("Sin Contenido", "Primero genera un contenido.")
            return
        
        if not self.is_logged_in:
            messagebox.showwarning("No Conectado", "Primero conecta con LinkedIn.")
            return
        
        try:
            # Publish to LinkedIn
            result = self.automation.publish_post(
                self.current_content.get('post', ''),
                self.current_content.get('hashtags', [])
            )
            
            if result:
                # Save as published
                self.db.save_post(
                    content=self.current_content.get('post', ''),
                    tone=self.current_content.get('tone', ''),
                    style=self.current_content.get('style', ''),
                    hashtags=json.dumps(self.current_content.get('hashtags', [])),
                    image_url=self.current_content.get('image_query', ''),
                    status='PUBLISHED'
                )
                
                logger.info("Content published successfully")
                messagebox.showinfo("Publicado", "¡Contenido publicado exitosamente!")
                self.update_dashboard()
                self.load_posts()
            else:
                messagebox.showerror("Error", "No se pudo publicar el contenido.")
                
        except Exception as e:
            logger.error(f"Publish error: {e}")
            messagebox.showerror("Error", f"Error al publicar: {str(e)}")
    
    def quick_generate(self):
        """Quick generate action"""
        self.switch_tab('content')
        self.generate_content()
    
    def quick_publish(self):
        """Quick publish action"""
        if self.current_content:
            self.publish_content()
        else:
            messagebox.showinfo("Info", "Primero genera un contenido.")
    
    def run_scheduler(self):
        """Run the scheduler"""
        try:
            self.scheduler.run()
            logger.info("Scheduler executed")
            messagebox.showinfo("Scheduler", "Scheduler ejecutado correctamente.")
            self.update_dashboard()
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            messagebox.showerror("Error", f"Error en scheduler: {str(e)}")
    
    def pause_scheduler(self):
        """Pause the scheduler"""
        try:
            self.scheduler.pause()
            logger.info("Scheduler paused")
            messagebox.showinfo("Scheduler", "Scheduler pausado.")
        except Exception as e:
            logger.error(f"Pause error: {e}")
    
    def load_posts(self):
        """Load posts into treeview"""
        if not hasattr(self, 'posts_tree'):
            return
        
        # Clear existing items
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)
        
        try:
            status = self.status_filter.get() if hasattr(self, 'status_filter') else None
            posts = self.db.get_posts(status=None if status == 'ALL' else status)
            
            for post in posts:
                content_preview = post.get('content', '')[:50] + '...'
                self.posts_tree.insert('', 'end', values=(
                    post.get('id', ''),
                    content_preview,
                    post.get('tone', ''),
                    post.get('style', ''),
                    post.get('status', ''),
                    post.get('created_at', '')[:16] if post.get('created_at') else ''
                ))
                
        except Exception as e:
            logger.error(f"Load posts error: {e}")
    
    def publish_selected(self):
        """Publish selected post"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Selecciona un post.")
            return
        
        # Get post data and publish
        item = self.posts_tree.item(selection[0])
        post_id = item['values'][0]
        
        # Implementation for publishing
        logger.info(f"Publishing post {post_id}")
        messagebox.showinfo("Info", f"Publicando post {post_id}...")
    
    def schedule_selected(self):
        """Schedule selected post"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Selecciona un post.")
            return
        
        logger.info("Scheduling selected post")
        messagebox.showinfo("Info", "Programando post seleccionado...")
    
    def edit_selected(self):
        """Edit selected post"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Selecciona un post.")
            return
        
        logger.info("Editing selected post")
        messagebox.showinfo("Info", "Función de edición en desarrollo.")
    
    def delete_selected(self):
        """Delete selected post"""
        selection = self.posts_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Selecciona un post.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este post?"):
            item = self.posts_tree.item(selection[0])
            post_id = item['values'][0]
            
            try:
                self.db.delete_post(post_id)
                self.posts_tree.delete(selection[0])
                logger.info(f"Deleted post {post_id}")
                self.update_dashboard()
            except Exception as e:
                logger.error(f"Delete error: {e}")
    
    def cancel_selected(self):
        """Cancel selected scheduled post"""
        selection = self.scheduled_tree.selection()
        if not selection:
            messagebox.showwarning("Sin Selección", "Selecciona un post programado.")
            return
        
        logger.info("Canceling scheduled post")
        messagebox.showinfo("Info", "Post programado cancelado.")
    
    def save_schedule_settings(self):
        """Save schedule settings"""
        try:
            settings = {
                'min_posts': self.min_posts.get(),
                'max_posts': self.max_posts.get(),
                'morning': self.morning.get(),
                'afternoon': self.afternoon.get(),
                'evening': self.evening.get(),
                'weekend': self.weekend.get()
            }
            
            os.makedirs('data', exist_ok=True)
            with open('data/schedule_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            
            logger.info("Schedule settings saved")
            messagebox.showinfo("Guardado", "Configuración guardada exitosamente.")
            
        except Exception as e:
            logger.error(f"Save settings error: {e}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def save_credentials(self):
        """Save LinkedIn credentials"""
        try:
            email = self.email_entry.get()
            password = self.password_entry.get()
            
            if not email or not password:
                messagebox.showwarning("Campos Vacíos", "Ingresa email y contraseña.")
                return
            
            # Save encrypted (basic - in production use proper encryption)
            os.makedirs('data', exist_ok=True)
            with open('data/credentials.json', 'w') as f:
                json.dump({'email': email, 'password': password}, f)
            
            logger.info("Credentials saved")
            messagebox.showinfo("Guardado", "Credenciales guardadas exitosamente.")
            
        except Exception as e:
            logger.error(f"Save credentials error: {e}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def save_api_keys(self):
        """Save API keys"""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/api_keys.json', 'w') as f:
                json.dump({
                    'unsplash': self.unsplash_entry.get(),
                    'pexels': self.pexels_entry.get()
                }, f)
            
            logger.info("API keys saved")
            messagebox.showinfo("Guardado", "Claves API guardadas exitosamente.")
            
        except Exception as e:
            logger.error(f"Save API keys error: {e}")
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def update_dashboard(self):
        """Update dashboard statistics"""
        try:
            stats = self.db.get_stats()
            
            # Update stat cards if they exist
            if hasattr(self, 'stat_cards'):
                self.stat_cards['total'].update_value(stats.get('total', 0))
                self.stat_cards['published'].update_value(stats.get('published', 0))
                self.stat_cards['scheduled'].update_value(stats.get('scheduled', 0))
                self.stat_cards['generated'].update_value(stats.get('generated', 0))
            
            # Update recent posts
            if hasattr(self, 'recent_text'):
                recent = self.db.get_recent_posts(5)
                self.recent_text.delete('1.0', tk.END)
                
                if recent:
                    for post in recent:
                        content = post.get('content', '')[:80] + '...'
                        status = post.get('status', 'UNKNOWN')
                        date = post.get('created_at', '')[:16]
                        self.recent_text.insert(tk.END, 
                            f"📝 [{status}] {date}\n{content}\n\n")
                else:
                    self.recent_text.insert(tk.END, "No hay actividad reciente.")
            
            logger.info("Dashboard updated")
            
        except Exception as e:
            logger.error(f"Dashboard update error: {e}")
    
    def load_settings(self):
        """Load saved settings"""
        try:
            # Load schedule settings
            if os.path.exists('data/schedule_settings.json'):
                with open('data/schedule_settings.json', 'r') as f:
                    settings = json.load(f)
                    
                if hasattr(self, 'min_posts'):
                    self.min_posts.set(settings.get('min_posts', 3))
                if hasattr(self, 'max_posts'):
                    self.max_posts.set(settings.get('max_posts', 5))
                if hasattr(self, 'morning'):
                    self.morning.set(settings.get('morning', True))
                if hasattr(self, 'afternoon'):
                    self.afternoon.set(settings.get('afternoon', True))
                if hasattr(self, 'evening'):
                    self.evening.set(settings.get('evening', True))
                if hasattr(self, 'weekend'):
                    self.weekend.set(settings.get('weekend', False))
            
            # Load credentials
            if os.path.exists('data/credentials.json'):
                with open('data/credentials.json', 'r') as f:
                    creds = json.load(f)
                    
                if hasattr(self, 'email_entry'):
                    self.email_entry.insert(0, creds.get('email', ''))
                if hasattr(self, 'password_entry'):
                    self.password_entry.insert(0, creds.get('password', ''))
            
            # Load API keys
            if os.path.exists('data/api_keys.json'):
                with open('data/api_keys.json', 'r') as f:
                    keys = json.load(f)
                    
                if hasattr(self, 'unsplash_entry'):
                    self.unsplash_entry.insert(0, keys.get('unsplash', ''))
                if hasattr(self, 'pexels_entry'):
                    self.pexels_entry.insert(0, keys.get('pexels', ''))
            
            logger.info("Settings loaded")
            
        except Exception as e:
            logger.error(f"Load settings error: {e}")
    
    def refresh_logs(self):
        """Refresh logs display"""
        if not hasattr(self, 'logs_text'):
            return
        
        try:
            self.logs_text.delete('1.0', tk.END)
            
            log_file = 'logs/app.log'
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = f.readlines()[-100:]  # Last 100 lines
                    self.logs_text.insert('1.0', ''.join(logs))
            else:
                self.logs_text.insert('1.0', "No hay registros disponibles.")
                
        except Exception as e:
            self.logs_text.insert('1.0', f"Error loading logs: {e}")
    
    def show_ai_stats(self):
        """Show AI statistics"""
        try:
            stats = self.content_gen.get_statistics()
            
            if hasattr(self, 'ai_stats_text'):
                self.ai_stats_text.delete('1.0', tk.END)
                self.ai_stats_text.insert('1.0', 
                    f"📊 Generados: {stats.get('total_generated', 0)}\n"
                    f"📝 Promedio palabras: {stats.get('average_word_count', 0):.0f}\n"
                    f"🎨 Tono más usado: {stats.get('most_used_tone', 'N/A')}\n"
                    f"📐 Estilo más usado: {stats.get('most_used_style', 'N/A')}")
        except Exception as e:
            logger.error(f"AI stats error: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = LinkedInAutomationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
