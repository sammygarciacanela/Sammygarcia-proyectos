# (src_start, src_end, z0, z1, mode)  mode: ease = transición suave desde el zoom anterior, cut = corte seco (punch-in)
SEGS = [
 (3.58, 5.95, 1.00,1.07,'cut'),   # El ego no construye líderes
 (7.05, 8.36, 1.12,1.14,'ease'),  # porque si tú necesitas
 (11.10,14.30,1.03,1.07,'ease'),  # que constantemente ... jefe
 (14.30,18.55,1.15,1.18,'cut'),   # quizás no has entendido ... liderazgo
 (19.25,20.85,1.06,1.00,'ease'),  # Mira, con los años
 (22.08,23.44,1.09,1.11,'ease'),  # el liderazgo no se trata
 (23.98,25.55,1.03,1.05,'ease'),  # de siempre tener la razón
 (26.16,28.80,1.10,1.13,'ease'),  # controlar ... reconocimiento
 (28.80,30.45,1.02,1.05,'cut'),   # porque cuando el ego dirige
 (31.30,33.45,1.15,1.17,'cut'),   # la persona deja de sentirse valorada
 (34.85,36.06,1.00,1.00,'card'),  # Un verdadero líder  (pantalla azul)
 (36.06,36.62,1.02,1.04,'cut'),   # escucha
 (38.20,39.45,1.09,1.11,'ease'),  # reconoce sus errores
 (39.98,41.50,1.02,1.04,'ease'),  # comparte su conocimiento
 (41.50,44.55,1.15,1.18,'cut'),   # y sobre todo, desarrolla personas
 (46.33,48.38,1.07,1.00,'ease'),  # Y esa muchas veces es la diferencia
 (48.88,52.15,1.02,1.08,'ease'),  # Un líder inseguro ...
 (53.80,55.10,1.13,1.14,'cut'),   # Un líder humilde
 (57.36,60.02,1.05,1.08,'ease'),  # trabaja para que otros también triunfen
 (60.82,62.36,1.00,1.03,'ease'),  # porque el éxito de un líder
 (64.70,67.70,1.07,1.10,'ease'),  # no se mide ... personalmente
 (67.70,70.25,1.15,1.19,'cut'),   # sino por las personas que ayuda a crecer
 (72.10,74.52,1.00,1.04,'ease'),  # Y ahora te pregunto, ¿tu equipo
 (75.50,77.12,1.09,1.11,'ease'),  # te sigue por tu posición
 (79.15,79.48,1.04,1.05,'ease'),  # o
 (80.78,82.75,1.15,1.18,'cut'),   # por cómo lo has ayudado?
 (83.72,85.70,1.03,1.08,'ease'),  # Te leo en los comentarios + sonrisa final
]
TAIL_FREEZE = 1.0   # segundos extra congelados al final para la firma
AX, AY = 0.40, 0.44 # punto de anclaje del zoom (rostro)
