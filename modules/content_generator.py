"""
Content Generator Module - AI-powered content generation
"""

import random
from datetime import datetime


class ContentGenerator:
    """Generate LinkedIn content with AI-like patterns"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load content templates"""
        return {
            "reflection": [
                {
                    "content": "Hoy completé un proyecto que llevaba meses en desarrollo.\n\nNo fue fácil - hubo noches sin dormir, bugs imposibles de encontrar, y momentos de duda.\n\nPero cada desafío me enseñó algo nuevo. La clave no es evitar los problemas, sino aprender a resolverlos con paciencia y creatividad.\n\n¿Cuál ha sido tu mayor aprendizaje este año? 👇",
                    "tone": "REFLECTIVE",
                    "style": "EXPERIENCE_BASED",
                    "wordCount": 78,
                    "hashtags": ["DesarrolloSoftware", "Aprendizaje", "Crecimiento"],
                    "image_query": "developer working late"
                },
                {
                    "content": "Una lección que aprendí esta semana: no siempre hay que tener la respuesta perfecta.\n\nA veces, compartir tus dudas abiertamente genera mejores conversaciones que fingir que lo sabes todo.\n\nLa vulnerabilidad construye conexión. La autenticidad genera confianza.\n\n¿Alguien más siente esto? 🤔",
                    "tone": "REFLECTIVE",
                    "style": "NARRATIVE",
                    "wordCount": 72,
                    "hashtags": ["Liderazgo", "Autenticidad", "CrecimientoPersonal"],
                    "image_query": "team discussion meeting"
                }
            ],
            "educational": [
                {
                    "content": "3 herramientas que transformaron mi flujo de trabajo este año:\n\n1️⃣ GitHub Copilot - Coding asistido por IA\n2️⃣ Notion - Documentación y planificación\n3️⃣ Figma - Diseño colaborativo\n\nLa combinación de estas tres me permitió ser 3x más productivo.\n\n¿Cuáles son tus herramientas favoritas? 💡",
                    "tone": "EDUCATIONAL",
                    "style": "LIST_BASED",
                    "wordCount": 65,
                    "hashtags": ["Productividad", "Herramientas", "Desarrollo"],
                    "image_query": "developer workspace tools"
                },
                {
                    "content": "Después de 10 años como desarrollador, aquí van 5 verdades que nadie te dice:\n\n1. El código perfecto no existe\n2. Pedir ayuda es una fortaleza\n3. Los mejores aprendizajes vienen de errores\n4. El balance vida-trabajo es crucial\n5. La comunidad lo es todo\n\n¿Agree? 💭",
                    "tone": "EDUCATIONAL",
                    "style": "LIST_BASED",
                    "wordCount": 70,
                    "hashtags": ["Programacion", "Consejos", "Desarrollador"],
                    "image_query": "senior developer coding"
                }
            ],
            "motivational": [
                {
                    "content": "Mi primer código en producción tenía un bug que pasé 3 días buscando.\n\nEra un simple typo.\n\nPero sabes qué aprendí? Que la paciencia es más valiosa que la velocidad, y que siempre debemos tener a alguien revise nuestro código antes de deployar.\n\nLos errores nos hacen mejores. 🚀",
                    "tone": "MOTIVATIONAL",
                    "style": "STORYTELLING",
                    "wordCount": 75,
                    "hashtags": ["Programacion", "Aprendizaje", "TechCareer"],
                    "image_query": "coding bug fix"
                },
                {
                    "content": "No esperes el momento perfecto para empezar.\n\nEl momento perfecto no existe.\n\nEmpieza con lo que tienes, donde estás. Mejora durante el camino.\n\nCada experto fue alguna vez un principiante que decidió comenzar.\n\n¿Qué estás esperando para empezar tu proyecto? 💪",
                    "tone": "MOTIVATIONAL",
                    "style": "DIRECT",
                    "wordCount": 62,
                    "hashtags": ["Motivacion", "Start", "Accion"],
                    "image_query": "starting new project"
                }
            ],
            "technical": [
                {
                    "content": "Hot take: El 80% de los bugs que he encontrado en producción eran errores de lógica, no de sintaxis.\n\nEl código compila no significa que funciona.\n\nTests unitarios + code reviews + pruebas de integración = menos incidentes a las 3 AM.\n\n¿Cuál ha sido tu bug más épico? 🐛",
                    "tone": "TECHNICAL",
                    "style": "QUESTION_BASED",
                    "wordCount": 68,
                    "hashtags": ["Testing", "Bugs", "DesarrolloSoftware"],
                    "image_query": "code debugging screen"
                },
                {
                    "content": "Arquitectura de software que he aprendido a valorar:\n\n✅ Modularidad - Piezas independientes\n✅ Escalabilidad - Crece con la demanda\n✅ Mantenibilidad - Fácil de modificar\n✅ Observabilidad - Saber qué pasa\n\nNo se trata de ser fancy, se trata de ser práctico.\n\n¿Qué addition harías? 🏗️",
                    "tone": "TECHNICAL",
                    "style": "LIST_BASED",
                    "wordCount": 72,
                    "hashtags": ["Arquitectura", "SoftwareDesign", "BestPractices"],
                    "image_query": "software architecture diagram"
                }
            ]
        }
    
    def generate(self, theme="auto", min_words=80, max_words=180):
        """Generate content based on theme"""
        
        # Select theme if auto
        if theme == "auto" or theme == "Auto (IA Decide)":
            theme_key = random.choice(list(self.templates.keys()))
        else:
            # Map theme selection to template categories
            theme_map = {
                "Desarrollo Software": "technical",
                "Crecimiento Profesional": "reflection",
                "Tendencias Tech": "educational",
                "Liderazgo": "motivational",
                "Experiencia Personal": "reflection"
            }
            theme_key = theme_map.get(theme, random.choice(list(self.templates.keys())))
        
        # Select random template from theme
        template = random.choice(self.templates.get(theme_key, self.templates["reflection"]))
        
        # Apply slight variations to make content unique
        content = self._add_variations(template['content'])
        
        # Calculate actual word count
        word_count = len(content.split())
        
        return {
            'content': content,
            'tone': template['tone'],
            'style': template['style'],
            'wordCount': word_count,
            'hashtags': template['hashtags'],
            'image_query': template['image_query'],
            'theme': theme_key
        }
    
    def _add_variations(self, content):
        """Add human-like variations to content"""
        
        variations = [
            # Add emoji variations
            lambda x: x.replace("👍", random.choice(["👍", "💪", "🎯"])),
            lambda x: x.replace("🤔", random.choice(["🤔", "💭", "❓"])),
            lambda x: x.replace("🚀", random.choice(["🚀", "⭐", "✨"])),
            
            # Add slight rewording
            lambda x: x.replace("¿Cuál ha sido", random.choice(["¿Cuál ha sido", "Cuéntame cuál ha sido", "Qué has aprendido"])),
            lambda x: x.replace("hoy aprendí", random.choice(["hoy aprendí", "esta semana aprendí", "recientemente entendí"])),
            
            # Add contractions occasionally
            lambda x: x.replace("no es", random.choice(["no es", "no es"])),
            lambda x: x.replace("Es un", random.choice(["Es un", "Es un"])),
        ]
        
        # Apply 2-3 random variations
        for _ in range(random.randint(2, 3)):
            variation = random.choice(variations)
            try:
                content = variation(content)
            except:
                pass
        
        return content
    
    def generate_multiple(self, count=3, theme="auto"):
        """Generate multiple content variations"""
        posts = []
        for _ in range(count):
            post = self.generate(theme=theme)
            posts.append(post)
        return posts