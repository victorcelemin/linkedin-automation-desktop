"""
Advanced Content Generator Module
Follows specific rules for LinkedIn human-like content generation

Rules implemented:
- Human, close, natural tone
- Occasional slight imperfections
- Variable style (direct vs storytelling)
- Length: 80-180 words
- Flexible structure
- Hook + Development + Closing with question/reflection
- Topics: Software development, personal experiences, professional learning, errors & lessons
"""

import random
import json
import os
from datetime import datetime


class AdvancedContentGenerator:
    """Advanced content generator following strict LinkedIn rules"""
    
    def __init__(self):
        self.memory = {
            'recent_posts': [],
            'used_tones': [],
            'used_styles': [],
            'used_topics': [],
            'word_count_history': []
        }
        self.load_memory()
    
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
    
    def generate(self, theme="auto", min_words=80, max_words=180):
        """
        Generate content following strict rules:
        - Human, close, natural tone
        - Occasional imperfections
        - Variable style
        - 80-180 words
        - Hook + Development + Closing
        """
        
        # Select tone (avoid recent repetition)
        available_tones = ['MOTIVATIONAL', 'REFLECTIVE', 'TECHNICAL', 'CASUAL', 
                          'INSPIRATIONAL', 'EDUCATIONAL', 'STORYTELLING']
        recent_tones = self.memory.get('used_tones', [])[-3:]
        tones_pool = [t for t in available_tones if t not in recent_tones]
        if not tones_pool:
            tones_pool = available_tones
        tone = random.choice(tones_pool)
        
        # Select style
        available_styles = ['DIRECT', 'NARRATIVE', 'QUESTION_BASED', 
                           'LIST_BASED', 'EXPERIENCE_BASED', 'LESSON_LEARNED']
        recent_styles = self.memory.get('used_styles', [])[-3:]
        styles_pool = [s for s in available_styles if s not in recent_styles]
        if not styles_pool:
            styles_pool = available_styles
        style = random.choice(styles_pool)
        
        # Select topic
        topics = {
            'software_development': {
                'keywords': ['código', 'bug', 'feature', 'deploy', 'refactoring', 
                           'pull request', 'code review', 'programming', 'debugging'],
                'image_queries': ['developer coding', 'code screen', 'programming workspace']
            },
            'personal_experiences': {
                'keywords': ['proyecto', 'equipo', 'deadline', 'reunión', 'cliente',
                           'challenge', 'logro', 'meta', 'decisión'],
                'image_queries': ['team collaboration', 'office meeting', 'professional success']
            },
            'professional_learning': {
                'keywords': ['aprendí', 'curso', 'certificación', 'mentor', 'crecimiento',
                           'skill', 'habilidad', 'formación', 'desarrollo profesional'],
                'image_queries': ['learning online', 'professional development', 'studying']
            },
            'errors_and_lessons': {
                'keywords': ['error', 'mistake', 'lesson', 'lección', 'failure', 
                           'fracaso', 'aprendizaje', 'mejora', 'evolución'],
                'image_queries': ['lessons learned', 'professional growth', 'reflection']
            }
        }
        
        recent_topics = self.memory.get('used_topics', [])[-2:]
        topics_pool = {k: v for k, v in topics.items() if k not in recent_topics}
        if not topics_pool:
            topics_pool = topics
        selected_topic = random.choice(list(topics_pool.keys()))
        topic_data = topics[selected_topic]
        
        # Generate content based on tone and style
        content = self._generate_content(tone, style, selected_topic, topic_data, min_words, max_words)
        
        # Add human imperfections
        content = self._add_imperfections(content)
        
        # Calculate word count
        word_count = len(content.split())
        
        # Select image query
        image_query = random.choice(topic_data['image_queries'])
        
        # Update memory
        self._update_memory(tone, style, selected_topic, word_count, content)
        
        return {
            'post': content,
            'image_query': image_query,
            'image_description': f"Illustration related to {selected_topic.replace('_', ' ')}",
            'tone': tone,
            'style': style,
            'word_count': word_count,
            'topic': selected_topic,
            'hashtags': self._generate_hashtags(selected_topic, tone),
            'imperfections_added': True
        }
    
    def _generate_content(self, tone, style, topic, topic_data, min_words, max_words):
        """Generate content based on parameters"""
        
        # Content templates based on style
        templates = {
            'DIRECT': {
                'hook_variations': [
                    "Hoy quiero compartir algo que aprendí",
                    "Una verdad que descubrí recientemente",
                    "Lo que nadie te dice sobre",
                    "Mi consejo número uno para",
                    "Después de años en esto, puedo decirte que"
                ],
                'development': self._get_direct_development(topic),
                'closing': [
                    "¿Qué piensas tú?",
                    "¿Has experimentado algo similar?",
                    "Me encantaría conocer tu opinión",
                    "¿Cuál es tu experiencia con esto?",
                    "Comparte en los comentarios"
                ]
            },
            'NARRATIVE': {
                'hook_variations': [
                    "Hace unos años, estaba en una situación complicada",
                    "Recuerdo perfectamente el día que entendí",
                    "Mi historia con esto comenzó cuando",
                    "Todo empezó cuando",
                    "Nunca olvidaré el momento en que"
                ],
                'development': self._get_narrative_development(topic),
                'closing': [
                    "Y tú, ¿tienes una historia similar?",
                    "¿Cuál ha sido tu momento 'aha'?",
                    "¿Te ha pasado algo parecido?",
                    "Quiero escuchar tu historia",
                    "Cuéntame tu experiencia"
                ]
            },
            'QUESTION_BASED': {
                'hook_variations': [
                    "¿Alguna vez te has preguntado por qué",
                    "¿Por qué algunos desarrolladores",
                    "¿Qué pasaría si",
                    "¿Es esto correcto o estamos",
                    "¿Realmente necesitamos"
                ],
                'development': self._get_question_development(topic),
                'closing': [
                    "¿Cuál es tu respuesta?",
                    "¿Qué opinas?",
                    "Vota en los comentarios",
                    "¿Team A o Team B?",
                    "Deja tu respuesta abajo"
                ]
            },
            'LIST_BASED': {
                'hook_variations': [
                    "5 cosas que aprendí sobre",
                    "3 errores que todo principiante comete",
                    "Las 4 reglas que sigo para",
                    "7 hábitos que cambieron mi",
                    "Top 3 herramientas para"
                ],
                'development': self._get_list_development(topic),
                'closing': [
                    "¿Cuál agregarías a esta lista?",
                    "¿Coincides con estos puntos?",
                    "¿Cuál es tu favorito?",
                    "¿Hay algo que omití?",
                    "Comparte tu top list"
                ]
            },
            'EXPERIENCE_BASED': {
                'hook_variations': [
                    "Mi primera vez con esto fue un desastre",
                    "Aprendí esto de la manera difícil",
                    "Esta experiencia me cambió la perspectiva",
                    "Lo que viví me enseñó que",
                    "Mi error más costoso fue"
                ],
                'development': self._get_experience_development(topic),
                'closing': [
                    "¿Cuál ha sido tu mayor aprendizaje?",
                    "¿Quéerror te cambió más?",
                    "Comparte tu experiencia",
                    "¿Qué hubieras hecho diferente?",
                    "Aprendamos juntos de los errores"
                ]
            },
            'LESSON_LEARNED': {
                'hook_variations': [
                    "Lección #47: No confundir estar ocupado con ser productivo",
                    "Lo que este proyecto me enseñó sobre paciencia",
                    "La lección más cara de mi carrera",
                    "Aprendí que la simplicidad siempre gana",
                    "Error = Oportunidad de aprendizaje"
                ],
                'development': self._get_lesson_development(topic),
                'closing': [
                    "¿Cuál es tu lección favorita?",
                    "¿Qué lección cambiarías si pudieras?",
                    "Comparte tu lección número uno",
                    "¿Qué aprendiste hoy?",
                    "Las mejores lecciones vienen de errores"
                ]
            }
        }
        
        # Get template components
        template = templates.get(style, templates['DIRECT'])
        hook = random.choice(template['hook_variations'])
        development = template['development']
        closing = random.choice(template['closing'])
        
        # Combine with natural flow
        content = f"{hook}.\n\n{development}\n\n{closing}"
        
        return content
    
    def _get_direct_development(self, topic):
        developments = {
            'software_development': [
                "El código limpio no es sobre seguir reglas, es sobre comunicación. Cuando escribes código, no estás hablando con la computadora - estás hablando con el desarrollador que lo leerá después. Y ese desarrollador podrías ser tú mismo en 6 meses.",
                "Una de las mejores decisiones que tomé fue dejar de buscar el código perfecto y empezar a buscar el código suficientemente bueno. La perfección es el enemigo del progreso, especialmente en desarrollo de software.",
                "Después de years programando, entendí algo clave: las mejores arquitecturas no son las más complejas, son las más simples que resuelven el problema. KISS siempre gana."
            ],
            'personal_experiences': [
                "La persona que fui hace 5 años no reconocería al que soy hoy. Cada reunión difícil, cada proyecto que parecía imposible, cada feedback duro - todos formaron quien soy ahora como profesional.",
                "Trabajar en equipo no significa estar de acuerdo en todo. Significa respetar las diferencias y encontrar el mejor camino juntos. Las mejores ideas nacen del debate respetuoso.",
                "Mi mayor logro no fue un proyecto técnico, sino ver a un junior que mentorié liderar su equipo. Ese momento confirmó que invertir en personas siempre vale la pena."
            ],
            'professional_learning': [
                "Los cursos te dan conocimiento, pero la práctica te da maestría. He tomado más de 50 cursos online. Los que realmente marcaron diferencia fueron donde apliqué inmediatamente lo aprendido.",
                "La certificación más valiosa no está en un papel, está en la confianza de resolver problemas complejos. Esa confianza solo viene de enfrentar desafíos reales.",
                "Mi mejor mentor no fue el más experimentado, fue el más paciente. Alguien que me dejó equivocarme y luego me ayudó a entender por qué."
            ],
            'errors_and_lessons': [
                "Mi primer deploy a producción falló spectacularmente. Olvidé una variable de entorno. Desde entonces, tengo un checklist de 25 items que reviso antes de cada deploy.",
                "Asumir que el usuario pensaría como yo fue mi peor error en diseño. Después de esa experiencia, siempre pregunto '¿Y si no supiera nada?' antes de cada decisión.",
                "Perseguir deadlines sin considerar technical debt casi me cuesta un proyecto completo. Ahora incluyo tiempo para refactorizar en cada sprint."
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _get_narrative_development(self, topic):
        developments = {
            'software_development': [
                "Mi primer code review fue un desastre. El senior developer me devolvió el PR con 47 comentarios. Me sentí terrible ese día. Pero cada comentario era una lección disfrazada de crítica. Hoy hago code reviews con paciencia, recordando cómo me sentí esa vez.",
                "Estaba a punto de renunciar a la programación después de mi primer burnout. Un colega me dijo: 'No es el código, es el ritmo'. Aprendí a establecer límites y a decir que no. Mi carrera cambio para siempre ese día.",
                "La migración que duró 3 meses en lugar de 2 semanas me enseñó más que cualquier curso. Cuando asumes que algo es simple, la realidad te humilla. Ahordocumento cada proceso, por obvio que parezca."
            ],
            'personal_experiences': [
                "Mi primera presentación ante stakeholders fue un desastre técnico. El WiFi falló, la demo no cargó, me quedé en blanco. Pero en lugar de rendirme, preparé versiones offline de todo. Ahora siempre tengo un Plan B, C y D.",
                "Cuando me ofrecieron mi primer liderazgo, dije que no. Tenía miedo de dejar de escribir código. Aprendí que liderar no significa dejar de aprender, sino ayudar a otros a crecer también.",
                "Una vez trabajé 72 horas seguidas para cumplir un deadline. El código que escribí fue terrible. Esa experiencia me enseñó que descansar no es opcional, es parte del trabajo."
            ],
            'professional_learning': [
                "Empecé aprendiendo Python, después JavaScript, luego Java, después Go. Cada lenguaje me dio una nueva perspectiva. La variedad no te hace confuso, te hace adaptable.",
                "Mi primer mentor me dijo: 'No te preocupes por no saber todo, preocúpate por no querer aprender'. Esa frase guía mi carrera desde entonces. La humildad abre más puertas que la arrogancia.",
                "Después de 10 años, sigo haciendo cursos básicos. No porque no sepa, sino porque siempre hay formas mejores de hacer las cosas. El experto永远 es un eterno estudiante."
            ],
            'errors_and_lessons': [
                "Subí credenciales a GitHub públicamente. Alguien las usó. Tuve que cambiar todas las passwords en producción. Ese día aprendí sobre seguridad de la forma más cara posible.",
                "Ignoré un error porque 'funcionaba en mi máquina'. 500 usuarios afectados después, aprendí sobre testing en ambiente real. Ahora testeo como si fuera el usuario más torpe del mundo.",
                "Deje un servidor sin monitorar durante el weekend. El lunes llegué a 200GB de logs. Automatice todo el monitoring ese mismo día. Los errores son oportunidades disfrazadas."
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _get_question_development(self, topic):
        developments = {
            'software_development': [
                "¿Por qué seguimos escribiendo código cuando la IA puede hacerlo? Porque la programación no es solo escribir sintaxis, es resolver problemas. Y eso, por ahora, sigue siendo humano.",
                "¿Realidad necesitamos 15 frameworks JavaScript? Probablemente no. Pero cada uno resuelve un problema específico. La clave está en elegir el right tool for the job, no el más popular.",
                "¿Por qué algunos equipos shippean todos los días y otros tardan semanas en un release? La diferencia no es técnica, es cultural. Truster, comunicación y process ágiles."
            ],
            'personal_experiences': [
                "¿Por qué algunos profesionales crecen más rápido que otros? No es talento, es curiosidad. Los que preguntan 'por qué' en lugar de solo 'cómo' entienden más profundo.",
                "¿Qué hace a un equipo realmente efectivo? No son los individuos más brillantes, es cómo se comunican. He visto equipos mediocres superar a equipos de genios por comunicación.",
                "¿Por qué la diversidad importa en tech? Porque los equipos homogéneos piensan igual. Diferentes perspectivas significan más soluciones potenciales para cualquier problema."
            ],
            'professional_learning': [
                "¿Los certificados valen la pena? Depende. Si buscas un trabajo, pueden abrir puertas. Si ya estás trabajando, la experiencia vale más. Pero ambos juntos? Eso es poder.",
                "¿Deberías especializarte o generalizar? Mi respuesta: primero generaliza, después especializa, y nunca dejes de hacer ninguno de los dos.",
                "¿Cómo decides qué aprender? Los mercados cambian, pero los fundamentos permanecen. Invierte primero en fundamentos sólidos, después en tendencias."
            ],
            'errors_and_lessons': [
                "¿Deberías shippear código aunque no esté perfecto? Depende. ¿Hay usuarios esperando? ¿Es reversible? ¿Tienes un plan B? La perfección es enemiga del progreso, pero no de la calidad.",
                "¿Por qué los bugs pasan a producción? Porque no testeamos como usuarios reales usan el producto. Simular el uso humano es diferente de testear features.",
                "¿Cuándo debes refactorizar? No esperes al 'gran refactor'. Hazlo continuamente, en pequeño scale. Technical debt se paga diariamente, no una vez al año."
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _get_list_development(self, topic):
        developments = {
            'software_development': [
                "1. Escribe código para el humano que lo leerá después, no para la máquina\n2. Testea como si fueras un usuario torpe\n3. Documenta como si fueras nuevo en el proyecto\n4. Code review como si fuera una conversación, no una crítica\n5. Refactoriza continuamente, no esperes al 'gran refactor'",
                "1. Entiende el problema ANTES de escribir código\n2. Divide tareas grandes en pequeñas entregables\n3. Comunica frecuentemente con tu equipo\n4. Establece límites claros en tu tiempo\n5. Celebra los pequeños logros",
                "1. Aprende un nuevo concepto cada semana\n2. Construye algo práctico inmediatamente\n3. Enseña lo que aprendes a otros\n4. Participa en comunidades técnicas\n5. Conecta con mentores y peers"
            ],
            'personal_experiences': [
                "1. Escucha más de lo que hablas\n2. Pregunta cuando no sepas (siempre)\n3. Admite tus errores rápidamente\n4. Celebra los logros de otros\n5. Mantén tu curiosidad activa",
                "1. Tu salud mental es prioridad\n2. Los boundaries son necesarios\n3. No todos los proyectos valen tu tiempo extra\n4. Las relaciones profesionales importan\n5. Diversión es parte del trabajo",
                "1. La comunicación es más importante que la técnica\n2. La empatía te hace mejor profesional\n3. El feedback es un regalo\n4. La paciencia es una virtud técnica\n5. El balance vida-trabajo es no negociable"
            ],
            'professional_learning': [
                "1. Invierte en fundamentos, no solo en frameworks\n2. Construye proyectos reales, no solo tutoriales\n3. Contribuye a open source\n4. Asiste a meetups y conferencias\n5. Busca mentoría activamente",
                "1. Lee documentación oficial, no solo blogs\n2. Entiende el 'por qué', no solo el 'cómo'\n3. Practica consistentemente, no intensivamente\n4. Aprende en público (escribe, comparte)\n5. No tengas miedo de ser principiante",
                "1. Los fundamentos son eternos\n2. La práctica supera la teoría\n3. La comunidad es tu mejor recurso\n4. La documentación es tu amiga\n5. Los errores son tus maestros"
            ],
            'errors_and_lessons': [
                "1. Testea temprano y frecuentemente\n2. Automatiza lo repetitivo\n3. Documenta decisiones técnicas\n4. Versiona todo, no solo código\n5. Ten un plan de rollback siempre",
                "1. El código que no pruebas es código roto\n2. El timing importa, pero la calidad importa más\n3. Comunica antes de asumir\n4. Establece expectativas claras\n5. Aprende de cada incidente",
                "1. Los shortcuts se convierten en deuda técnica\n2. La seguridad no es opcional\n3. El performance importa desde el día 1\n4. El logging salva vidas\n5. El monitoring previene desastres"
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _get_experience_development(self, topic):
        developments = {
            'software_development': [
                "Mi primer deploy a producción fue un viernes a las 5 PM. Todos estaban yéndose. Yo quería 'probar algo rápido'. Ese algo causó 2 horas de downtime. Desde entonces, los viernes son para code review, no para deployments.",
                "Pasé 3 días buscando un bug que resultó ser un simple espacio extra en un JSON. Tres días. Desde entonces, siempre reviso lo obvio primero antes de asumir que el código es complejo.",
                "Mi primera arquitectura microservicios tenía 50 servicios para una app que 10 personas usaban. Aprendí que elegir la arquitectura correcta depende del problema, no de las tendencias."
            ],
            'personal_experiences': [
                "Dije 'no' a una promoción porque no me sentía listo. Mi manager me dijo: 'Nadie se siente listo. La preparación viene en el camino'. Acepté la siguiente oferta. Tenía razón.",
                "Tuve un conflicto con un colega por un technical decision. En lugar de confrontar,邀请é a un café. Hablamos como personas, no como desarrolladores. Resolvimos todo en 30 minutos.",
                "Mi primer equipo remoto era desorganizado. Propuse daily standups de 15 minutos. Se resistieron al principio. Ahora es nuestro ritual más productivo del día."
            ],
            'professional_learning': [
                "Tomé un curso de comunicación técnica pensando que era 'para junior'. Fue la clase más valiosa de mi carrera. La comunicación es el skill más underated en tech.",
                "Leí sobre liderazgo técnico creyendo que era para managers. Resulta que todo developer leadership. Liderar features, liderar conversations, liderar decisiones.",
                "Aprendí testing por necessity, no por interés. Un bug en producción me despertó a las 3 AM. Desde entonces, testear es mi activity favorita (sí, es weird, pero funciona)."
            ],
            'errors_and_lessons': [
                "Ignoré un error de performance porque 'solo pasaba una vez al mes'. El día que pasó durante una demo con el CEO, aprendí que 'raro' no significa 'raro para siempre'.",
                "Me obsesioné con optimizar un código que nadie usaba. 2 semanas de trabajo para un 0.1% de mejora. Ahora pregunto primero: '¿Quién usa esto?' antes de cualquier optimización.",
                "Deje un feature incompleto porque 'el cliente no lo notará'. El cliente lo notó. Ahora delivero completo o no delivero, sin términos medios."
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _get_lesson_development(self, topic):
        developments = {
            'software_development': [
                "Lección que aprendí hoy: El código más elegante no es el que menos líneas tiene, es el que el junior puede entender en 5 minutos. Legibilidad > Cleverness, siempre.",
                "Lección #23: No mezcles feature changes con refactor en el mismo PR. Los reviewers odian eso, y con razón. Separa concerns, siempre.",
                "Lección que volví a aprender: Documentar decisiones técnicas AHOROR es mejor que documentarlas 'cuando tenga tiempo'. Spoiler: nunca tienes tiempo después."
            ],
            'personal_experiences': [
                "Lección personal: Tu salud mental no es negociable. He cancelado deadlines por burnout y aprendí que las personas adecuadas siempre entenderán. Los que no, no merecen tu tiempo extra.",
                "Lección sobre equipos: El mejor equipo no es el de los mejores programadores, es el donde la gente se siente segura para hacer preguntas y admitir errores.",
                "Lección sobre crecimiento: No necesitas saberlo todo para liderar. Necesitas saber aprender rápido y ser honesto cuando no sabes algo."
            ],
            'professional_learning': [
                "Lección de aprendizaje: 30 minutos de coding diarios valen más que 8 horas un sábado. La consistencia vence a la intensidad en cualquier habilidad técnica.",
                "Lección sobre mentoría: La mejor forma de aprender es enseñar. Desde que empecé a mentorear junior devs, mi propio código mejoró significativamente.",
                "Lección sobre feedback: Dar feedback específico y actionable es más difícil que escribir código limpio. Pero es la skill que más impacto tiene en tu equipo."
            ],
            'errors_and_lessons': [
                "Lección #1: Los errores en producción son inevitables. Lo que importa es cómo respondes. Tener un runbook de incidentes te salva en las 3 AM.",
                "Lección sobre testing: Si no es testeable, no es deployable. He aprendido esto de la forma difícil, varias veces. Automatiza todo lo que puedas.",
                "Lección sobre debugging: Los logs son tus mejores amigos. Si no puedes debuggear en 15 minutos, probablemente necesitas mejores logs, no más tiempo."
            ]
        }
        
        return random.choice(developments.get(topic, developments['software_development']))
    
    def _add_imperfections(self, content):
        """Add human-like imperfections"""
        
        imperfections = [
            # Occasional contractions
            (r'\bes\b', 's'),
            (r'\bno es\b', 'no es'),
            
            # Conversational phrases
            (r'\bEntiendes\b', 'Entiendes'),
            (r'\bSaben qué\b', 'Saben qué'),
            (r'\bLa verdad\b', 'La verdad'),
            
            # Occasional hesitation markers
            (r'\.\s*$', '...'),
        ]
        
        # 30% chance to add imperfection
        if random.random() < 0.3:
            # Add conversational filler
            fillers = [
                "\n\n(PD: ",
                "\n\nPor cierto, ",
                "\n\nAh, y ",
                "\n\nUna cosa más: "
            ]
            filler = random.choice(fillers)
            filler_end = random.choice([
                "esto me pasó realmente.)",
                "nunca lo mencioné antes.",
                "se me olvidaba mencionarlo.",
                "eso es todo por hoy."
            ])
            content += f"{filler}{filler_end}"
        
        # 20% chance to add emoji
        if random.random() < 0.2:
            emojis = ['🤔', '💡', '🚀', '✨', '💪', '🎯', '👍', '🔥']
            emoji = random.choice(emojis)
            # Add at end or before closing question
            if '?' in content:
                content = content.replace('?', f'? {emoji}', 1)
            else:
                content += f"\n\n{emoji}"
        
        return content
    
    def _generate_hashtags(self, topic, tone):
        """Generate relevant hashtags"""
        topic_hashtags = {
            'software_development': ['#Programming', '#Coding', '#DevLife', '#SoftwareDevelopment', '#TechTips'],
            'personal_experiences': ['#CareerGrowth', '#ProfessionalDevelopment', '#WorkLife', '#CareerTips'],
            'professional_learning': ['#Learning', '#Growth', '#Education', '#Skills', '#Development'],
            'errors_and_lessons': ['#LessonsLearned', '#Mistakes', '#Growth', '#Learning', '#ProfessionalGrowth']
        }
        
        tone_hashtags = {
            'MOTIVATIONAL': ['#Motivation', '#Inspiration', '#Mindset'],
            'REFLECTIVE': ['#Reflection', '#Thinking', '#Insights'],
            'TECHNICAL': ['#TechTips', '#Programming', '#Development'],
            'CASUAL': ['#Casual', '#Authentic', '#RealTalk'],
            'INSPIRATIONAL': ['#Inspiration', '#DreamBig', '#Believe'],
            'EDUCATIONAL': ['#Learning', '#Education', '#Knowledge'],
            'STORYTELLING': ['#Storytelling', '#MyStory', '#Experience']
        }
        
        # Combine topic and tone hashtags
        all_hashtags = topic_hashtags.get(topic, []) + tone_hashtags.get(tone, [])
        
        # Select 3-5 random hashtags
        count = random.randint(3, min(5, len(all_hashtags)))
        return random.sample(all_hashtags, count)
    
    def _update_memory(self, tone, style, topic, word_count, content):
        """Update memory with new content"""
        
        # Update recent posts (keep last 10)
        self.memory['recent_posts'] = self.memory.get('recent_posts', [])[-9:]
        self.memory['recent_posts'].append(content[:100])  # Store first 100 chars
        
        # Update tone usage
        self.memory['used_tones'] = self.memory.get('used_tones', [])[-9:]
        self.memory['used_tones'].append(tone)
        
        # Update style usage
        self.memory['used_styles'] = self.memory.get('used_styles', [])[-9:]
        self.memory['used_styles'].append(style)
        
        # Update topic usage
        self.memory['used_topics'] = self.memory.get('used_topics', [])[-9:]
        self.memory['used_topics'].append(topic)
        
        # Update word count history
        self.memory['word_count_history'] = self.memory.get('word_count_history', [])[-19:]
        self.memory['word_count_history'].append(word_count)
        
        # Save memory
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
        return {
            'total_generated': len(self.memory.get('recent_posts', [])),
            'average_word_count': sum(self.memory.get('word_count_history', [0])) / 
                                 max(len(self.memory.get('word_count_history', [1])), 1),
            'most_used_tone': max(set(self.memory.get('used_tones', [])), 
                                 key=self.memory.get('used_tones', []).count) 
                             if self.memory.get('used_tones') else 'N/A',
            'most_used_style': max(set(self.memory.get('used_styles', [])), 
                                  key=self.memory.get('used_styles', []).count) 
                              if self.memory.get('used_styles') else 'N/A'
        }