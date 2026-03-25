"""
Advanced Content Generator Module
Generates reflective, interesting posts about trending tech topics

Features:
- Fetches trending topics automatically
- Generates longer, more thoughtful posts
- Natural, non-forced engagement
- Multiple writing styles and tones
- Spanish language with authentic voice
"""

import random
import json
import os
from datetime import datetime
import re


class AdvancedContentGenerator:
    """Advanced content generator for LinkedIn posts"""
    
    def __init__(self):
        self.memory = {
            'recent_posts': [],
            'used_tones': [],
            'used_styles': [],
            'used_topics': [],
            'used_trending': [],
            'word_count_history': [],
            'post_themes': []
        }
        self.load_memory()
        
        # Import trending topics
        try:
            from modules.trending_topics import TrendingTopics
            self.trending = TrendingTopics()
        except ImportError:
            self.trending = None
    
    def load_memory(self):
        """Load memory from file"""
        try:
            with open('data/memory.json', 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        except FileNotFoundError:
            self.save_memory()
    
    def save_memory(self):
        """Save memory to file"""
        os.makedirs('data', exist_ok=True)
        with open('data/memory.json', 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def generate(self, theme="auto", min_words=150, max_words=350):
        """
        Generate a reflective, interesting post about trending topics
        
        Args:
            theme: Specific theme or 'auto' for AI selection
            min_words: Minimum word count (default 150)
            max_words: Maximum word count (default 350)
        """
        
        # Get trending topic
        trending_topic = self._get_trending_topic(theme)
        
        # Select writing approach
        approach = self._select_approach()
        
        # Select tone (avoid recent repetition)
        tone = self._select_tone()
        
        # Generate the post
        content = self._generate_reflective_post(trending_topic, approach, tone)
        
        # Calculate word count
        word_count = len(content.split())
        
        # Generate relevant hashtags
        hashtags = self._generate_hashtags(trending_topic, approach)
        
        # Update memory
        self._update_memory(trending_topic, approach, tone, word_count, content)
        
        return {
            'post': content,
            'image_query': self._generate_image_query(trending_topic),
            'image_description': f"Imagen relacionada con {trending_topic.get('title', 'tecnología')}",
            'tone': tone,
            'style': approach,
            'word_count': word_count,
            'topic': trending_topic.get('category', 'tech'),
            'trending_title': trending_topic.get('title', ''),
            'hashtags': hashtags,
            'imperfections_added': True
        }
    
    def _get_trending_topic(self, theme):
        """Get a trending topic based on theme"""
        if self.trending:
            if theme == "auto":
                topic = self.trending.get_random_topic()
            else:
                # Map theme to category
                category_map = {
                    "Desarrollo Software": "programming",
                    "Experiencias Personales": "career",
                    "Aprendizaje Profesional": "career",
                    "Errores y Lecciones": "general"
                }
                category = category_map.get(theme)
                topic = self.trending.get_random_topic(category)
            
            if topic:
                return topic
        
        # Fallback to built-in trending topics
        return self._get_fallback_topic(theme)
    
    def _get_fallback_topic(self, theme):
        """Fallback trending topics"""
        current_year = datetime.now().year
        
        fallback_topics = [
            {
                'title': f'La IA Generativa está cambiando cómo programamos en {current_year}',
                'description': 'Las herramientas de IA están transformando el flujo de trabajo diario',
                'tags': ['ai', 'programming', 'productivity'],
                'category': 'ai'
            },
            {
                'title': 'Rust vs Go: La batalla de los lenguajes modernos',
                'description': 'Análisis de las tendencias en sistemas y backend',
                'tags': ['rust', 'go', 'programming'],
                'category': 'programming'
            },
            {
                'title': 'Platform Engineering es el nuevo DevOps',
                'description': 'Las Internal Developer Platforms están revolucionando el desarrollo',
                'tags': ['platform-engineering', 'devops', 'infrastructure'],
                'category': 'devops'
            },
            {
                'title': 'WebAssembly está madurando rápidamente',
                'description': 'Apps complejas en el navegador ya no son ciencia ficción',
                'tags': ['webassembly', 'webdev', 'performance'],
                'category': 'webdev'
            },
            {
                'title': 'El trabajo remoto en tech ha evolucionado',
                'description': 'Nuevas dinámicas y herramientas para equipos distribuidos',
                'tags': ['remote-work', 'culture', 'productivity'],
                'category': 'culture'
            },
            {
                'title': 'TypeScript sigue dominando el frontend',
                'description': 'Por qué cada vez más equipos adoptan TypeScript',
                'tags': ['typescript', 'javascript', 'frontend'],
                'category': 'frontend'
            },
            {
                'title': 'Kubernetes no es para todos',
                'description': 'Reflexiones sobre cuándo usar y cuándo no usar K8s',
                'tags': ['kubernetes', 'devops', 'architecture'],
                'category': 'devops'
            },
            {
                'title': 'La importancia de escribir menos código',
                'description': 'A veces la mejor solución es la más simple',
                'tags': ['simplicity', 'architecture', 'best-practices'],
                'category': 'architecture'
            },
            {
                'title': 'GraphQL ha encontrado su lugar',
                'description': 'No reemplazó REST, pero找到了 su nicho perfecto',
                'tags': ['graphql', 'api', 'backend'],
                'category': 'backend'
            },
            {
                'title': 'El auge de los LLMs locales',
                'description': 'Ejecutar modelos de lenguaje en tu propia máquina es viable',
                'tags': ['llm', 'local-ai', 'privacy'],
                'category': 'ai'
            }
        ]
        
        return random.choice(fallback_topics)
    
    def _select_approach(self):
        """Select writing approach (non-forced, natural)"""
        approaches = [
            'reflection',      # Personal reflection on topic
            'story',          # Anecdotal story
            'analysis',       # Technical analysis
            'opinion',        # Thoughtful opinion
            'question',       # Genuine curiosity
            'comparison',     # Comparing perspectives
            'lesson',         # Learning experience
            'observation'     # Noticing a trend
        ]
        
        # Weight away from question (less forced engagement)
        weights = [25, 20, 15, 15, 8, 7, 5, 5]
        return random.choices(approaches, weights=weights, k=1)[0]
    
    def _select_tone(self):
        """Select tone avoiding recent repetition"""
        tones = [
            'thoughtful',      # Deep reflection
            'conversational',  # Casual, friendly
            'professional',    # Formal, authoritative
            'humble',          # Learning mindset
            'enthusiastic',    # Passionate about tech
            'balanced',        # Nuanced perspective
            'experienced',     # Sharing wisdom
            'curious'          # Exploring ideas
        ]
        
        recent_tones = self.memory.get('used_tones', [])[-5:]
        available = [t for t in tones if t not in recent_tones]
        if not available:
            available = tones
        
        return random.choice(available)
    
    def _generate_reflective_post(self, topic, approach, tone):
        """Generate a reflective, longer post"""
        
        title = topic.get('title', 'la tecnología')
        description = topic.get('description', '')
        category = topic.get('category', 'tech')
        
        # Get templates based on approach
        templates = {
            'reflection': self._reflection_template,
            'story': self._story_template,
            'analysis': self._analysis_template,
            'opinion': self._opinion_template,
            'question': self._question_template,
            'comparison': self._comparison_template,
            'lesson': self._lesson_template,
            'observation': self._observation_template
        }
        
        template_func = templates.get(approach, self._reflection_template)
        return template_func(title, description, category, tone)
    
    def _reflection_template(self, title, description, category, tone):
        """Personal reflection template"""
        
        hooks = [
            f"Hace unos días me encontré pensando en {title.lower()}",
            f"Últimamente no puedo dejar de reflexionar sobre {title.lower()}",
            f"Hubo un momento esta semana que me hizo pensar profundamente en {title.lower()}",
            f"Después de años en este mundo, {title.lower()} me sigue generando reflexiones",
            f"Esta mañana desperté con una pregunta en mente relacionada con {title.lower()}"
        ]
        
        reflections = {
            'ai': [
                "La inteligencia artificial ha dejado de ser ese tema futurista del que hablábamos en conferencias. Hoy está en mi editor de código, en mis reuniones de equipo, en mis decisiones de arquitectura. Y eso me genera una mezcla extraña de emoción y responsabilidad.",
                "Recuerdo cuando escribí mi primer script hace años. Me tomaba horas entender errores básicos. Ahora veo a herramientas de IA resolver en segundos problemas que me tomaban días. No sé si debería sentirme amenazado o agradecido. Probablemente ambas cosas.",
                "La IA no va a reemplazar a los programadores. Pero los programadores que usan IA van a reemplazar a los que no. Ese pensamiento me mantuvo despierto anoche, reevaluando cómo aprendo y trabajo."
            ],
            'programming': [
                "Programar siempre ha sido más sobre las personas que sobre las máquinas. Cada línea de código que escribo es una conversación con el desarrollador que vendrá después. ¿Qué quiero decirle? ¿Le estoy ayudando o confundiendo?",
                "He cambiado de opinión muchas veces sobre cuál es el 'mejor' lenguaje, framework, o patrón. Cada cambio me enseñó que lo importante no es la herramienta, sino el problema que intentas resolver y las personas que resolverán después.",
                "La elegancia en el código no se trata de fewer lines o clever tricks. Se trata de que alguien pueda leerlo a las 3 AM cuando algo se rompió en producción y entender exactamente qué hacer."
            ],
            'devops': [
                "DevOps no es una herramienta ni una checklist. Es una mentalidad que tomó años desarrollar en mi equipo. Empezamos con las mejores prácticas documentadas, pero lo que realmente funcionó fue sentarnos juntos y preguntarnos: '¿Qué nos está frenando?'",
                "La infraestructura como código cambió mi perspectiva completamente. De repente, los servidores dejaron de ser ese tema mágico que solo entendía el equipo de infra. Ahora cualquier desarrollador puede entender, modificar y contribuir.",
                "He visto demasiadas empresas implementar Kubernetes porque 'la gente lo usa'. Sin entender que a veces un simple servidor con Docker Compose resuelve el 90% de los problemas. La complejidad no es un badge de honor."
            ],
            'frontend': [
                "El frontend ha evolucionado tanto que a veces siento que me quedo atrás. Cada mes hay un nuevo framework, una nueva forma de hacer las cosas. Pero aprendí que lo constante es labase: HTML bien hecho, CSS que funciona, JavaScript que其他人 pueden leer.",
                "Vi una charla hace años donde alguien dijo: 'El mejor framework es el que tu equipo conoce'. En ese momento pensé que era una respuesta aburrida. Hoy entiendo que es la verdad más importante de nuestra industria.",
                "CSS ya no es el enemigo. Tomó años aceptarlo, pero una vez que dejas de luchar contra él y empiezas a trabajar con él, descubres que es increíblemente poderoso y elegante."
            ],
            'general': [
                "A veces me pregunto si estamos construyendo software para resolver problemas reales o solo para impresionar a otros ingenieros. Las mejores soluciones que he visto no son las más complejas, sino las que hacen que el usuario ni siquiera note que hay tecnología funcionando.",
                "La tecnología debería ser invisible. Cuando alguien usa nuestra app y no piensa en la app, sino en lo que está logrando, entonces sabemos que hicimos algo bien. La complejidad debe estar en el código, no en la experiencia.",
                "Después de años trabajando en este campo, he aprendido que las predicciones tecnológicas casi siempre están equivocadas. Lo que importa no es adivinar el futuro, sino construir cosas que funcionen hoy y sean adaptables mañana."
            ]
        }
        
        # Get category-specific reflections or fallback to general
        category_reflections = reflections.get(category, reflections['general'])
        reflection = random.choice(category_reflections)
        
        # Build the post
        hook = random.choice(hooks)
        
        # Personal connection
        personal_connections = [
            "Yo mismo estuve en esa situación hace no mucho tiempo.",
            "Esto me recuerda a una experiencia personal que tuve el año pasado.",
            "No te voy a mentir, al principio yo también era escéptico.",
            "Mi perspectiva cambió después de una conversación con un colega.",
            "Fue después de un proyecto particularmente difícil que entendí esto."
        ]
        personal = random.choice(personal_connections)
        
        # Nuanced thoughts
        nuances = [
            "Eso no significa que todo sea perfecto o que no haya desafíos.",
            "Claro, hay limitaciones y cosas que aún no resolvemos completamente.",
            "No es una solución mágica, pero es un paso importante en la dirección correcta.",
            "Hay debates legítimos en ambos lados de este tema.",
            "Entiendo los argumentos en contra, y algunos son válidos."
        ]
        nuance = random.choice(nuances)
        
        # Future perspective
        futures = [
            "Lo que me emociona es ver hacia dónde va esto en los próximos años.",
            "Me pregunto cómo veremos este momento dentro de cinco años.",
            "Lo interesante es que esto apenas está comenzando.",
            "El potencial de lo que viene es genuinamente emocionante.",
            "Tengo esperanza de que esto lleve a un trabajo más significativo."
        ]
        future = random.choice(futures)
        
        # Natural closing (not forced engagement)
        closings = [
            "¿Qué piensan ustedes? Me genuinamente interesa conocer otras perspectivas.",
            "Si han tenido experiencias similares, me encantaría escucharlas.",
            "Estoy seguro de que otros han llegado a conclusiones diferentes.",
            "¿Han notado lo mismo en sus equipos o empresas?",
            "Curioso saber si esto resuena con lo que están viviendo.",
            "Sería interesante ver cómo se compara con experiencias en otros contextos."
        ]
        closing = random.choice(closings)
        
        # Assemble post
        post = f"""{hook}. {personal}

{reflection}

{nuance}

{future}

{closing}"""
        
        return post
    
    def _story_template(self, title, description, category, tone):
        """Anecdotal story template"""
        
        hooks = [
            f"Les cuento algo que me pasó relacionado con {title.lower()}",
            f"Hay una historia que quiero compartir sobre {title.lower()}",
            f"No suelo contar esto, pero {title.lower()} me recordó algo",
            f"Hace unas semanas viví algo que tiene que ver con {title.lower()}",
            f"Esta historia cambió mi perspectiva sobre {title.lower()}"
        ]
        
        story_bodies = {
            'ai': [
                "Estaba en una reunión de planning cuando alguien mencionó que había resuelto un bug complejo usando IA en lugar de buscar documentación. Al principio pensé que era un atajo. Después entendí que era una evolución en cómo resolvemos problemas. No dejamos de pensar, solo pensamos diferente.",
                "Mi compañero llegó un día y me mostró código generado por IA que había refactorizado. No era perfecto, pero era un excelente punto de partida. Discutimos por qué ciertas partes funcionaban y otras no. Fue una de las mejores sesiones de aprendizaje que he tenido.",
                "Añadimos una herramienta de IA a nuestro flujo de trabajo sin mucho bombo. Dos meses después, nos dimos cuenta de que estábamos shippeando features 30% más rápido. No por escribir código más rápido, sino por pasar menos tiempo en el boilerplate y más en el diseño."
            ],
            'programming': [
                "Mi primer code review fue devastador. 47 comentarios en un PR que yo creía perfecto. Me sentí terrible ese día. Pero cada comentario era una lección. Hoy hago code reviews con paciencia, recordando cómo me sentí. El código no se trata de ser inteligente, se trata de comunicarse.",
                "Trabajé en un proyecto donde el código más elegante no era el que menos líneas tenía, sino el que cualquier nuevo desarrollador podía entender en una tarde. Esa experiencia me enseñó más sobre arquitectura que cualquier libro.",
                "Una vez pasé tres días buscando un bug. Tres días. Resultó ser un espacio extra en un JSON. En lugar de frustrarme, celebré que lo encontré y documenté mi proceso para que otros no pierdan tiempo similar."
            ],
            'devops': [
                "Hace un año nuestro deploy process tomaba 2 horas y involucraba 15 pasos manuales. Hoy toma 5 minutos y es completamente automatizado. El cambio no fue la herramienta, fue sentarnos a mapear cada paso y preguntarnos '¿por qué hacemos esto así?'",
                "Perdimos datos en producción una vez. Fue una experiencia formativa. No solo por lo que aprendimos sobre backups, sino sobre comunicación. Desde entonces, tenemos runbooks para cada tipo de incidente y drills regulares.",
                "Mi equipo resistió Kubernetes por dos años. 'Es complejo', decían. Tenían razón. Pero cuando finalmente lo adoptamos para el caso correcto, la diferencia fue notable. La lección: evalúa las herramientas para tu contexto, no para las tendencias."
            ],
            'frontend': [
                "Pasé años peleando con CSS hasta que un diseñador me mostró que estaba usando mal el grid system. En 10 minutos resolvió problemas que yo tenía hace semanas. A veces el expertise viene de donde no esperas.",
                "Creamos un componente que pensábamos era perfecto. Hasta que el equipo de accessibility nos mostró que era completamente inusable para personas con lectores de pantalla. Humillante pero educativo.",
                "Un junior me preguntó por qué usábamos un framework específico. No supe responder bien. Investigamos juntos, probamos alternativas y terminamos cambiando. Fue la mejor decisión que tomamos ese quarter."
            ],
            'general': [
                "En mi primera startup, intentamos hacer todo. Analytics, AI, blockchain (era 2018). Al final, lo que funcionó fue lo más simple: una buena UI, performance rápida, y resolver el problema específico del usuario. La complejidad no es sinónimo de valor.",
                "Tuve un jefe que decía: 'Si puedes explicarlo en una servilleta, puedes construirlo'. Lo desprecié al principio. Ahora es mi mantra. Los proyectos más exitosos que he visto tenían una visión que cabía en una frase.",
                "Perdí un cliente importante porque no escuché. No por el producto, sino porque no pregunté qué necesitaban realmente. Asumí. Desde entonces, pregunto primero y construyo después. La humildad es la mejor feature."
            ]
        }
        
        bodies = story_bodies.get(category, story_bodies['general'])
        body = random.choice(bodies)
        hook = random.choice(hooks)
        
        # Lessons learned
        lessons = [
            "La lección que saqué fue clara: nunca subestimes lo simple.",
            "Desde entonces, mi approach ha sido diferente.",
            "Ese día aprendí que la experiencia no siempre viene de los años, sino de la reflexión.",
            "No fue la primera ni la última vez que algo así me pasó, pero sí la que más recordaré.",
            "Hoy veo esa experiencia como un punto de inflexión en mi carrera."
        ]
        lesson = random.choice(lessons)
        
        # Connection to reader
        connections = [
            "Seguro que a muchos les ha pasado algo similar.",
            "No sé si es una experiencia universal, pero creo que es común.",
            "Imagino que otros en mi posición habrían reaccionado diferente.",
            "Tal vez mi historia no sea única, pero la reflexión sí.",
            "¿Les ha pasado algo parecido en sus carreras?"
        ]
        connection = random.choice(connections)
        
        post = f"""{hook}.

{body}

{lesson}

{connection}"""
        
        return post
    
    def _analysis_template(self, title, description, category, tone):
        """Technical analysis template"""
        
        hooks = [
            f"He estado analizando {title.lower()} y quiero compartir algunas observaciones",
            f"{title.upper()} es un tema complejo que merece un análisis más profundo",
            f"Después de investigar bastante sobre {title.lower()}, tengo algunas conclusiones",
            f"No hay respuestas simples cuando hablamos de {title.lower()}",
            f"Les comparto mi análisis de {title.lower()} después de semanas de investigación"
        ]
        
        analyses = {
            'ai': [
                "La IA Generativa no va a resolver todos nuestros problemas. Pero sí va a cambiar cómo abordamos ciertos tipos de problemas. La clave está en entender dónde agrega valor real y dónde es solo complejidad extra.",
                "Hay una diferencia crucial entre IA que ayuda y IA que reemplaza. La primera amplifica nuestras capacidades. La segunda nos hace dependientes. Las organizaciones inteligentes van a buscar el equilibrio correcto.",
                "Los LLMs tienen limitaciones reales: alucinaciones, sesgos, costos. Pero también tienen capacidades reales: acelerar tareas repetitivas, sugerir alternativas, documentar código. Ignorar cualquiera de los dos lados es un error."
            ],
            'programming': [
                "Los lenguajes de programación evolucionan, pero los principios permanecen. Entender data structures, algoritmos, y patterns de diseño te sirve en cualquier lenguaje. La inversión en fundamentals siempre paga dividendos.",
                "Hay un patrón interesante: las empresas más exitosas no siempre usan las tecnologías más modernas. Usan las que sus equipos dominan. La velocidad de desarrollo importa más que la innovación tecnológica.",
                "El clean code no es una cuestión de estética. Es una cuestión de costo. Código difícil de leer es código difícil de mantener. Y mantener code cuesta 10x más que escribirlo."
            ],
            'devops': [
                "DevOps maduro no se trata de herramientas. Se trata de cultura. He visto empresas con las mejores herramientas pero peor dev experience, y empresas con herramientas simples pero equipos increíblemente productivos.",
                "El monitoring no es solo alertas. Es entender tu sistema profundamente. Los mejores equipos que he visto no solo saben cuándo algo falla, sino por qué y cómo recuperarse.",
                "La automatización tiene un punto de retorno. Automatizar todo es tan malo como no automatizar nada. La clave está en priorizar: qué nos duele más y qué nos ahorra más tiempo."
            ],
            'frontend': [
                "Los frameworks frontend compiten en features, pero lo que realmente importa es developer experience. Si tu equipo pelea contra el framework en lugar de trabajar con él, estás perdiendo tiempo.",
                "Performance web ya no es opcional. Core Web Vitals impactan SEO, retention, y conversiones. Invertir en performance es invertir en negocio.",
                "El diseño de componentes es un skill subestimado. Un buen sistema de componentes ahorra meses de desarrollo. Uno malo crea deuda técnica que dura años."
            ],
            'general': [
                "La arquitectura de software no es sobre elegir las tecnologías correctas. Es sobre tomar decisiones que puedas vivir y modificar cuando sea necesario. La flexibilidad a menudo supera a la optimización.",
                "El testing en producción tiene mala reputación, pero los mejores sistemas lo practican de manera controlada. Feature flags, A/B testing, y rollout progresivo son testing en producción responsable.",
                "La deuda técnica no es inherentemente mala. Es una herramienta. Tomar deuda estratégica para shipper más rápido está bien, si tienes un plan para pagarla. La deuda que mata es la que nadie reconoce."
            ]
        }
        
        body = analyses.get(category, analyses['general'])
        hook = random.choice(hooks)
        
        # Nuanced points
        points = [
            "Este no es un debate blanco y negro. Hay grises importantes que considerar.",
            "No estoy sugiriendo que mi perspectiva sea la única correcta. Solo que es una que he desarrollado después de tiempo considerable.",
            "Hay trade-offs en cada dirección. Lo importante es entenderlos antes de decidir.",
            "Cada contexto es diferente. Lo que funciona en una startup no necesariamente funciona en enterprise.",
            "Mi conclusión podría cambiar con nueva información. Y eso está bien."
        ]
        point = random.choice(points)
        
        # Thought-provoking ending
        endings = [
            "¿Qué factores consideran ustedes más importantes en estas decisiones?",
            "Me interesa saber cómo otros abordan estos trade-offs.",
            "¿Han llegado a conclusiones diferentes en sus contextos?",
            "Siempre estoy aprendiendo, así que cualquier perspectiva es bienvenida.",
            "Estoy seguro de que mi entendimiento seguirá evolucionando."
        ]
        ending = random.choice(endings)
        
        post = f"""{hook}

{body}

{point}

{ending}"""
        
        return post
    
    def _opinion_template(self, title, description, category, tone):
        """Thoughtful opinion template"""
        
        hooks = [
            f"Tengo una opinión que quizás no sea popular sobre {title.lower()}",
            f"Sobre {title.lower()}: algo que quiero compartir con ustedes",
            f"He cambiado mi opinión varias veces sobre {title.lower()}",
            f"Últimamente he estado pensando diferente sobre {title.lower()}",
            f"No siempre estuve de acuerdo con lo que se dice sobre {title.lower()}"
        ]
        
        opinions = {
            'ai': [
                "Creo que estamos sobreestimando la IA a corto plazo y subestimándola a largo plazo. Las herramientas actuales son útiles pero imperfectas. En cinco años, probablemente no reconoceremos cómo trabajábamos.",
                "Mi opinión: la IA va a cambiar más los roles de lo que pensamos, pero no de la forma que esperamos. No va a eliminar programadores. Va a hacer que sean más productivos y que se enfocen en problemas más interesantes.",
                "Soy escéptico de las predicciones de 'la IA va a reemplazar X'. La historia muestra que la tecnología crea más trabajo del que elimina. Solo cambia el tipo de trabajo."
            ],
            'programming': [
                "Creo que la industria sobrecomplica el desarrollo de software. Las mejores aplicaciones que he usado son simples. No necesitan 15 microservicios ni un data lake. Necesitan resolver un problema bien.",
                "Opinión controvertida: más código no es mejor. A veces el PR más valioso es uno que elimina líneas. La mantenibilidad debería ser el KPI principal de cualquier equipo.",
                "He llegado a pensar que la obsesión con las 'best practices' a veces nos distrae del objetivo real: entregar valor. Las prácticas son herramientas, no fines en sí mismos."
            ],
            'devops': [
                "Mi opinión: Kubernetes es una solución fantástica para problemas que la mayoría de las empresas no tienen. La complejidad que introduce rara vez justifica los beneficios para equipos pequeños.",
                "Creo que el DevOps debería medirse en developer happiness, no en métricas técnicas. Si tu equipo odia el proceso de deploy, tienes un problema de DevOps sin importar cuántas herramientas tengas.",
                "Hot take: los pipelines de CI/CD más complejos que he visto son los peores. Si tu pipeline tiene más de 20 pasos, probablemente hay algo que simplificar."
            ],
            'frontend': [
                "Opinión: React no va a desaparecer pronto, pero su dominio absoluto sí. Los equipos están empezando a elegir herramientas más específicas para sus problemas. Y eso es saludable.",
                "Creo que hemos subestimado la importancia del CSS nativo. Los frameworks CSS resuelven problemas que podríamos evitar con mejor educación en fundamentos.",
                "Mi take: el mejor estado global es el que no necesitas compartir. Antes de llegar para un state manager, pregunta si puedes rediseñar los datos."
            ],
            'general': [
                "Creo que la industria valora demasiado la velocidad y no suficiente la sostenibilidad. Code que shippeas rápido hoy puede costarte meses mañana. El balance importa.",
                "Opinión personal: la documentación es más importante que el código. Puedes reescribir código. No puedes recuperar el contexto que se pierde cuando alguien se va.",
                "He pensado mucho en esto: el mayor indicador de éxito en un proyecto no es la tecnología, el equipo, o el mercado. Es la capacidad de adaptarse cuando las cosas cambian."
            ]
        }
        
        body = opinions.get(category, opinions['general'])
        hook = random.choice(hooks)
        
        # Caveats
        caveats = [
            "Esto viene de mi experiencia específica, que tiene sus limitaciones.",
            "No pretendo tener la respuesta definitiva. Solo una perspectiva que he desarrollado.",
            "Entiendo que otros pueden verlo diferente, y probablemente tienen razones válidas.",
            "Estoy abierto a cambiar de opinión con nueva información o perspectivas.",
            "Cada organización es diferente. Lo que funciona para mí puede no funcionar para otros."
        ]
        caveat = random.choice(caveats)
        
        # Inviting dialogue (natural, not forced)
        dialogues = [
            "¿Qué opinan ustedes? Genuinamente me interesa.",
            "Si tienen experiencias que contradicen esto, me encantaría escucharlas.",
            "Las mejores ideas vienen de discusiones, así que adelante.",
            "¿Estoy completamente equivocado? Es posible.",
            "Curioso saber si esto resuena o si mi burbuja es diferente."
        ]
        dialogue = random.choice(dialogues)
        
        post = f"""{hook}

{body}

{caveat}

{dialogue}"""
        
        return post
    
    def _question_template(self, title, description, category, tone):
        """Genuine curiosity template (not engagement bait)"""
        
        hooks = [
            f"Una pregunta genuina sobre {title.lower()} que he estado pensando",
            f"No tengo una respuesta clara sobre {title.lower()}. ¿Ustedes?",
            f"¿Alguien más ha tenido esta experiencia con {title.lower()}?",
            f"Últimamente me pregunto sobre algo relacionado con {title.lower()}",
            f"Hay algo sobre {title.lower()} que no me queda claro"
        ]
        
        questions = {
            'ai': [
                "¿Cómo están equilibrando el uso de IA con el aprendizaje real? Tengo la sensación de que si dependo demasiado, pierdo la capacidad de resolver problemas por mí mismo. Pero si no la uso, estoy perdiendo productividad.",
                "¿Ustedes sienten que la IA les está ayudando a escribir mejor código o solo código más rápido? Yo estoy tratando de usarla como learning tool, no como shortcut.",
                "¿Cuál es su límite con la IA? Yo he decidido que para decisiones de arquitectura y código crítico, prefiero pensar sin asistencia. Pero para boilerplate y testing, la uso libremente."
            ],
            'programming': [
                "¿Cuánto tiempo deberíamos dedicar a aprender frameworks nuevos versus profundizar en fundamentos? Siento que la industria nos presiona a correr constantemente hacia lo nuevo.",
                "¿Es más valioso un developer que conoce perfectamente un stack o uno que puede adaptarse a cualquier stack? He estado pensando mucho en esto al planear mi aprendizaje.",
                "¿Cuándo decidieron que un proyecto era suficientemente complejo para reconsiderar la arquitectura? Hay una línea difícil de encontrar entre refactorizar y reescribir."
            ],
            'devops': [
                "¿Cómo manejan el balance entre automación y flexibilidad? He visto equipos automatizar tanto que cualquier cambio requiere modificar 15 scripts.",
                "¿Qué métricas realmente importan para el DevOps? Digo métricas de valor real, no vanity metrics como 'deploy frequency' que no correlacionan con outcomes.",
                "¿Cuándo saben que necesitan cambiar su infrastructure? ¿Hay señales tempranas que deberíamos estar buscando?"
            ],
            'frontend': [
                "¿Cómo deciden cuándo un framework es worth it? He visto proyectos donde el overhead del framework supera los beneficios.",
                "¿Están invirtiendo en web components? Me parece interesante pero veo poca adopción real en producción.",
                "¿Cuál es su approach al CSS? ¿Usan frameworks, CSS modules, styled components, o vanilla? Cada opción tiene trade-offs."
            ],
            'general': [
                "¿Cómo definen 'éxito' en un proyecto técnico? ¿Es performance, adoption, code quality, business metrics? He visto equipos desalineados por no responder esta pregunta.",
                "¿Cuánto tiempo dedican a mantenerse actualizados versus profundizar en lo que ya saben? Siento que la respuesta correcta cambia según la etapa de la carrera.",
                "¿Han encontrado una forma efectiva de estimar proyectos? Después de años, sigo pensando que es más arte que ciencia."
            ]
        }
        
        body = questions.get(category, questions['general'])
        hook = random.choice(hooks)
        
        # Context (why this matters)
        contexts = [
            "No pregunto por engagement. Genuinamente estoy tratando de entender mejor.",
            "Esta es una pregunta que me ha estado molestando y no encuentro respuestas claras en internet.",
            "He preguntado a colegas pero tengo perspectivas mixtas. Quiero más data points.",
            "Probablemente la respuesta depende del contexto, pero quiero ver patrones.",
            "Sé que no hay una respuesta simple, pero quiero entender cómo otros lo abordan."
        ]
        context = random.choice(contexts)
        
        # Sharing own perspective
        perspective = [
            "Personalmente, todavía estoy figuring it out. Hoy creo una cosa, mañana quizás otra.",
            "Mi tendencia actual es [esto], pero estoy abierto a que me convenzan de lo contrario.",
            "He probado diferentes approaches y ninguno me ha convencido completamente.",
            "Lo que he aprendido es que la respuesta correcta depende mucho del contexto específico.",
            "Tengo una hipótesis pero necesito más experiencia para confirmarla."
        ]
        persp = random.choice(perspective)
        
        post = f"""{hook}

{body}

{context}

{persp}"""
        
        return post
    
    def _comparison_template(self, title, description, category, tone):
        """Comparing perspectives template"""
        
        hooks = [
            f"He estado pensando en cómo {title.lower()} se compara con alternativas",
            f"Las dos caras de {title.lower()}: una reflexión honesta",
            f"{title.upper()} tiene pros y cons. Les comparto mi análisis",
            f"No todo es blanco o negro cuando hablamos de {title.lower()}",
            f"Comparando perspectivas sobre {title.lower()}"
        ]
        
        comparisons = {
            'ai': [
                "La IA como assistente vs la IA como reemplazo. La primera amplifica tus capacidades, la segunda te hace dependiente. Personalmente busco herramientas que me ayuden a pensar mejor, no que piensen por mí.",
                "IA cerrada (GPT, Claude) vs IA local (Ollama, LM Studio). La primera es más potente pero tiene concerns de privacidad. La segunda es más privada pero menos capaz. El trade-off depende del caso de uso.",
                "Usar IA para escribir código vs usar IA para revisar código. Escribir es más rápido pero arriesgas perder habilidad. Revisar es más seguro y probablemente más educativo."
            ],
            'programming': [
                "Aprender haciendo vs aprender leyendo. Los libros te dan fundamentos, los proyectos te dan contexto. Mi balance actual: 20% lectura, 80% construcción. Pero tuve épocas inversas.",
                "Especialización vs generalización. Especializarte te hace valioso en un nicho. Generalizarte te hace adaptable. La clave está en T-shaped: ancho para adaptarte, profundidad para contribuir.",
                "Optimizar prematurely vs optimizar tarde. Ambos son problemáticos. El sweet spot: optimizar cuando tienes datos de que algo es un problema real, no una preocupación hipotética."
            ],
            'devops': [
                "Monorepo vs multi-repo. Monorepo facilita sharing y consistency. Multi-repo da más independencia. He visto ambos funcionar y fallar. El contexto del equipo importa más que la teoría.",
                "Self-hosted vs cloud managed. Self-hosted te da control pero requiere expertise. Managed te da simplicidad pero menos control. Mi regla: self-host solo si es tu core competency.",
                "GitOps tradicional vs platform engineering. GitOps es poderoso pero puede ser complejo. Platform engineering es más amigable pero requiere inversión upfront. El camino evolutivo suele ser de uno al otro."
            ],
            'frontend': [
                "SSR vs CSR vs ISR. Cada uno tiene su lugar. SSR para SEO y first load, CSR para apps dinámicas, ISR para sites semi-estáticos. La tendencia hacia hybrid me parece correcta.",
                "Estado global vs estado local. Estado global es tentador pero crea coupling. Estado local es más simple pero puede llevar a prop drilling. El balance: compartir solo lo necesario.",
                "Componentes controlados vs no controlados. Controlados te dan más control pero más código. No controlados son más simples pero menos predecibles. Dependiendo del caso de uso."
            ],
            'general': [
                "Velocidad vs calidad. Ambos son importantes pero la industria sobrevalora velocidad. Código rápido hoy puede ser código lento de mantener mañana. El balance está en iterar calidad incrementalmente.",
                "Innovación vs execution. La innovación sin execution no genera valor. Execution sin innovación te deja vulnerable. Las empresas que veo triunfar hacen ambos: innovan estratégicamente y ejecutan consistentemente.",
                "Individual contributor vs management. ICs construyen cosas. Managers construyen equipos que construyen cosas. Ninguno es mejor, son diferentes. La clave es elegir según tus fortalezas y deseos."
            ]
        }
        
        body = comparisons.get(category, comparisons['general'])
        hook = random.choice(hooks)
        
        # Personal stance
        stances = [
            "Mi posición actual ha sido desarrollada después de experimentar con ambos lados.",
            "No tengo una respuesta definitiva. Hay días en que prefiero un lado, días en que prefiero el otro.",
            "Lo que he aprendido es que el contexto determina cuál opción es mejor, no principios absolutos.",
            "Ambos enfoques tienen validez. La discusiónShould ser sobre cuándo aplicar cuál, no cuál es 'mejor'.",
            "He cambiado de opinión varias veces. Hoy creo en el balance, mañana quizás en uno específico."
        ]
        stance = random.choice(stances)
        
        # Asking for others' experiences
        experiences = [
            "¿Cómo han resuelto este dilema en sus contextos?",
            "Me interesa saber si otros han llegado a conclusiones diferentes.",
            "Si tienen data o experiencias que respalden un lado, me ayudaría.",
            "¿Hay algo que me estoy perdiendo en este análisis?",
            "Siempre estoy refinando mi perspectiva, así que cualquier input es valioso."
        ]
        experience = random.choice(experiences)
        
        post = f"""{hook}

{body}

{stance}

{experience}"""
        
        return post
    
    def _lesson_template(self, title, description, category, tone):
        """Learning experience template"""
        
        hooks = [
            f"Algo que aprendí recientemente sobre {title.lower()}",
            f"La lección más valiosa que {title.lower()} me ha enseñado",
            f"Después de mi experiencia con {title.lower()}, tengo una lección que compartir",
            f"{title.upper()} me enseñó algo que quería compartir",
            f"Una lección que aprendí de la manera difícil con {title.lower()}"
        ]
        
        lessons = {
            'ai': [
                "La IA no hace el trabajo por ti. Te da un mejor punto de partida. La tentación es copiar sin entender. La realidad es que necesitas entender lo suficiente para evaluar el output. La IA es un accelerante, no un sustituto de conocimiento.",
                "Las herramientas de IA son increíbles para acelerar lo que ya sabes hacer. Son peligrosas para lo que no sabes. He aprendido a usarlas para tareas donde tengo fundamentos, no para explorar territorio completamente nuevo.",
                "Alucinaciones no son el único problema de la IA. También hay sesgos, limitaciones de contexto, y una falsa sensación de confianza. La lección: siempre verificar, especialmente en áreas donde no eres experto."
            ],
            'programming': [
                "El código 'clever' es código problemático. Pasé años orgulloso de escribir código conciso y elegante. Hasta que otros tuvieron que mantenerlo. Ahora escribo para ser entendido, no para impresionar.",
                "Los mejores programadores que conozco no son los más rápidos escribiendo código. Son los que piensan más antes de escribir. Planificar 30 minutos puede ahorrar horas de refactorización.",
                "Aprender a debuggear es más valioso que aprender un nuevo framework. Los frameworks cambian, pero la capacidad de encontrar y resolver problemas es transferible y eternal."
            ],
            'devops': [
                "La automatización que no entiendes es una bomba de tiempo. Automatizamos un proceso complejo sin documentarlo. Cuando falló, nadie sabía cómo arreglarlo. Desde entonces, automatizo solo lo que puedo explicar en una servilleta.",
                "El monitoring sin alertas es observación sin acción. Tuve dashboards hermosos que nadie miraba. Cuando algo fallaba, nos enterábamos por usuarios. Las alertas correctas valen más que 100 métricas.",
                "Rollbacks funcionan mejor si los practicas. Implementamos un sistema de rollback que nunca habíamos probado. Falló cuando más lo necesitábamos. Ahora hacemos drills regulares."
            ],
            'frontend': [
                "Los edge cases no son edge cases. Son los casos que tus usuarios reales van a encontrar. Asumí que nadie usaría cierto flujo de la app. Un 15% de usuarios lo usaba diariamente. Humillante pero educativo.",
                "El performance es una feature, no un afterthought. Dejamos optimización para 'después'. El después nunca llegó y los usuarios notaron. Ahora incluimos performance budget desde el día uno.",
                "El accessibility no es opcional. Pensé que era algo para 'cumplir el requisito'. Hasta que vi a alguien real luchando con nuestra app. Desde entonces, a11y es parte de Definition of Done."
            ],
            'general': [
                "Las estimaciones sin datos son pronósticos. Pasé años estimando proyectos basándome en 'instinto'. Los números nunca cuadraban. Ahora uso velocity real y datos históricos. No es perfecto, pero es mejor que adivinar.",
                "Comunicar mal es fallar. Pensé que el trabajo técnico era lo importante. Hasta que malentendidos causaron semanas de trabajo wasted. Ahora la comunicación es tan importante como el código.",
                "Los shortcuts se pagan con intereses. Tomé atajos en un proyecto urgente. Funcionó en el momento. Dos meses después, Technical debt nos costó más tiempo que si lo hubiéramos hecho bien. La lección: hazlo bien una vez."
            ]
        }
        
        body = lessons.get(category, lessons['general'])
        hook = random.choice(hooks)
        
        # How it changed behavior
        changes = [
            "Desde entonces, mi approach ha sido diferente.",
            "Ahora hago las cosas de manera distusa.",
            "Esa experiencia me llevó a cambiar mi workflow completamente.",
            "Hoy incorporo esta lección en cada proyecto que empiezo.",
            "No fue una lección fácil, pero fue una necesaria."
        ]
        change = random.choice(changes)
        
        # Sharing forward
        sharing = [
            "Comparto esto porque quizás a alguien le sirva no cometer el mismo error.",
            "Si mi experiencia puede ahorrarle tiempo a alguien, vale la pena compartir.",
            "Las mejores lecciones que he recibido vinieron de otros compartiendo sus errores.",
            "No tengo todas las respuestas, pero tengo estas lecciones que aprendí caro.",
            "Aprendí esto de la manera difícil, espero que otros puedan aprender de mi experiencia."
        ]
        share = random.choice(sharing)
        
        post = f"""{hook}

{body}

{change}

{share}"""
        
        return post
    
    def _observation_template(self, title, description, category, tone):
        """Noticing a trend template"""
        
        hooks = [
            f"He notado algo interesante sobre {title.lower()}",
            f"Una observación que quiero compartir sobre {title.lower()}",
            f"Últimamente veo un patrón relacionado con {title.lower()}",
            f"{title.upper()} me ha llamado la atención por una razón específica",
            f"Algo que he estado observando en la industria relacionado con {title.lower()}"
        ]
        
        observations = {
            'ai': [
                "Los mejores usos de IA que he visto no son revolucionarios. Son incrementales. Alguien usando IA para escribir tests más rápido. Alguien usándola para documentar código legacy. Pequeñas mejoras que se acumulan.",
                "Hay un patrón interesante: las personas más resistentes a la IA son las que más se benefician de ella. Los seniors que 'ya saben hacerlo' son los que podrían acelerarse más con asistencia.",
                "Observo que la conversación sobre IA ha madurado. Ya no es ni hype ni miedo existencial. Es pragmatismo. ¿Cómo me ayuda esto a hacer mejor mi trabajo? Esa es la pregunta correcta."
            ],
            'programming': [
                "Los lenguajes más populares no son necesariamente los mejores. Son los que tienen mejor ecosistema. JavaScript domina no por su diseño, sino por npm, documentación, y comunidad. La lección: el lenguaje es solo parte de la ecuación.",
                "He notado que los mejores equipos tienen algo en común: code reviews como conversaciones, no como inspecciones. No buscan errores, buscan entender el razonamiento. Cambia completamente la dinámica.",
                "Hay una tendencia a escribir más código del necesario. Cada feature que agregamos es unafeature que alguien tiene que mantener. A veces la mejor contribución es decir 'no' o 'simplifiquemos'."
            ],
            'devops': [
                "Los equipos que shippean más no son los que trabajan más. Son los que eliminan fricción. Menos aprobaciones, mejores herramientas, automatización donde importa. La velocidad es un resultado, no un objetivo directo.",
                "Observo que el DevOps más efectivo es invisible. Los desarrolladores ni siquiera saben que hay un pipeline corriendo. El peor DevOps es el que te obliga a pensar en infra en lugar de tu feature.",
                "Hay una correlación interesante entre team size y infraestructura compleja. Equipos pequeños con infra simple shipspean más rápido que equipos grandes con infra compleja. La complejidad tiene un costo."
            ],
            'frontend': [
                "Los sitios más rápidos que he visto no usan las últimas tecnologías. Usan las básicas correctamente. HTML semántico, CSS optimizado, JavaScript mínimo. La novedad no equivale a performance.",
                "He notado que las mejores UIs no son las más bonitas. Son las más comprensibles. El usuario promedio prefiere algo obvio y rápido sobre algo hermoso pero confuso.",
                "Hay un patrón: los proyectos que más éxito tienen son los que el equipo realmente usa internamente. Dogfooding no es solo testing, es empatía."
            ],
            'general': [
                "Las startups más exitosas que conozco no tenían el mejor producto al inicio. Tenían el mejor entendimiento del problema. El producto mejoró con el tiempo, pero el problema lo entendieron desde el día uno.",
                "He observado que los mejores managers son los que más preguntan. No los que más saben. Preguntar demuestra humildad y genera confianza. La arrogancia es el enemigo del liderazgo.",
                "Un patrón que veo: los proyectos que fracasan no fracasan por razones técnicas. Fracasan por falta de comunicación, alineación, o entendimiento del usuario. La tecnología raramente es el problema real."
            ]
        }
        
        body = observations.get(category, observations['general'])
        hook = random.choice(hooks)
        
        # Questioning the observation
        questioning = [
            "Puede ser que mi observación esté sesgada por mi contexto específico.",
            "No tengo data científico para respaldar esto, solo experiencia observacional.",
            "Estoy seguro de que hay excepciones importantes que no estoy considerando.",
            "Mi burbuja profesional puede no ser representativa de la industria en general.",
            "Es posible que esto sea más un patrón local que global."
        ]
        questioning_text = random.choice(questioning)
        
        # Curious about others' observations
        curiosity = [
            "¿Han notado algo similar en sus contextos?",
            "Me interesa saber si esto es universal o específico de mi experiencia.",
            "Si tienen data que contradiga esto, genuinamente quiero verla.",
            "¿Hay observaciones que ustedes hayan hecho que yo debería considerar?",
            "Las mejores insights vienen de perspectivas diversas."
        ]
        curious = random.choice(curiosity)
        
        post = f"""{hook}

{body}

{questioning_text}

{curious}"""
        
        return post
    
    def _generate_image_query(self, topic):
        """Generate image search query based on topic"""
        category = topic.get('category', 'tech')
        
        queries = {
            'ai': ['artificial intelligence abstract', 'neural network visualization', 'AI robot coding'],
            'programming': ['developer coding screen', 'code editor abstract', 'programming workspace'],
            'devops': ['server infrastructure', 'cloud computing', 'devops pipeline'],
            'frontend': ['web design mockup', 'frontend development', 'responsive design'],
            'backend': ['server room', 'database schema', 'API architecture'],
            'career': ['professional meeting', 'career growth', 'team collaboration'],
            'security': ['cybersecurity lock', 'data protection', 'secure coding'],
            'architecture': ['system design diagram', 'software architecture', 'microservices'],
            'trends': ['technology innovation', 'future tech', 'digital transformation']
        }
        
        category_queries = queries.get(category, ['technology abstract', 'software development'])
        return random.choice(category_queries)
    
    def _generate_hashtags(self, topic, approach):
        """Generate relevant hashtags"""
        title = topic.get('title', '')
        tags = topic.get('tags', [])
        category = topic.get('category', 'tech')
        
        # Category hashtags
        category_hashtags = {
            'ai': ['#AI', '#ArtificialIntelligence', '#MachineLearning', '#TechTrends'],
            'programming': ['#Programming', '#Coding', '#SoftwareDevelopment', '#DevLife'],
            'devops': ['#DevOps', '#CloudComputing', '#Infrastructure', '#Automation'],
            'frontend': ['#Frontend', '#WebDev', '#JavaScript', '#UI'],
            'backend': ['#Backend', '#API', '#ServerSide', '#Database'],
            'career': ['#CareerGrowth', '#TechCareer', '#ProfessionalDevelopment'],
            'security': ['#Cybersecurity', '#DataSecurity', '#InfoSec'],
            'architecture': ['#SoftwareArchitecture', '#SystemDesign', '#BestPractices'],
            'trends': ['#TechTrends', '#Innovation', '#FutureOfWork'],
            'general': ['#Tech', '#Software', '#Development', '#Learning']
        }
        
        base_hashtags = category_hashtags.get(category, category_hashtags['general'])
        
        # Add tags from topic
        for tag in tags[:2]:
            if tag and len(tag) > 2:
                base_hashtags.append(f"#{tag.capitalize()}")
        
        # Select 3-5 hashtags
        count = random.randint(3, min(5, len(base_hashtags)))
        return random.sample(base_hashtags, count)
    
    def _update_memory(self, topic, approach, tone, word_count, content):
        """Update memory with new content"""
        
        # Update recent posts (keep last 15)
        self.memory['recent_posts'] = self.memory.get('recent_posts', [])[-14:]
        self.memory['recent_posts'].append(content[:100])
        
        # Update used items
        self.memory['used_tones'] = self.memory.get('used_tones', [])[-9:]
        self.memory['used_tones'].append(tone)
        
        self.memory['used_styles'] = self.memory.get('used_styles', [])[-9:]
        self.memory['used_styles'].append(approach)
        
        self.memory['used_topics'] = self.memory.get('used_topics', [])[-9:]
        self.memory['used_topics'].append(topic.get('category', 'general'))
        
        self.memory['used_trending'] = self.memory.get('used_trending', [])[-9:]
        self.memory['used_trending'].append(topic.get('title', '')[:50])
        
        self.memory['word_count_history'] = self.memory.get('word_count_history', [])[-19:]
        self.memory['word_count_history'].append(word_count)
        
        self.memory['post_themes'] = self.memory.get('post_themes', [])[-9:]
        self.memory['post_themes'].append({
            'topic': topic.get('title', ''),
            'approach': approach,
            'tone': tone,
            'word_count': word_count,
            'timestamp': datetime.now().isoformat()
        })
        
        self.save_memory()
    
    def generate_multiple(self, count=3, theme="auto"):
        """Generate multiple unique content variations"""
        posts = []
        for _ in range(count):
            post = self.generate(theme=theme)
            posts.append(post)
        return posts
    
    def get_statistics(self):
        """Get generation statistics"""
        word_counts = self.memory.get('word_count_history', [0])
        
        return {
            'total_generated': len(self.memory.get('recent_posts', [])),
            'average_word_count': sum(word_counts) / max(len(word_counts), 1),
            'most_used_tone': max(set(self.memory.get('used_tones', [])), 
                                 key=self.memory.get('used_tones', []).count) 
                             if self.memory.get('used_tones') else 'N/A',
            'most_used_style': max(set(self.memory.get('used_styles', [])), 
                                  key=self.memory.get('used_styles', []).count) 
                              if self.memory.get('used_styles') else 'N/A',
            'recent_topics': list(set(self.memory.get('used_trending', [])))[-5:]
        }
    
    def refresh_trending(self):
        """Force refresh trending topics"""
        if self.trending:
            return self.trending.force_refresh()
        return []
