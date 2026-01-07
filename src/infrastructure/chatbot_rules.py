#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chatbot Basado en Reglas - Sesión 1
Curso: Diseño e Implementación de Chatbots

Este chatbot funciona mediante coincidencia de patrones y reglas predefinidas.
Los mensajes y flujos están en el archivo flujos_conversacion.json
"""

import json
import re
import difflib
import random
import unicodedata
from pathlib import Path


class ChatbotReglas:
    """Chatbot basado en reglas con dos flujos de conversación"""
    def __init__(self, archivo_flujos='instructions.json'):
        """
        Inicializa el chatbot cargando los flujos desde JSON

        Args:
            archivo_flujos: Ruta al archivo JSON con los flujos
        """
        self.archivo_flujos = archivo_flujos
        self.cargar_flujos()
        self.contexto = {
            'nombre_usuario': None,
            'flujo_actual': None,
            'ultima_intencion': None,
            'historial': []
        }

    def cargar_flujos(self):
        """Carga los flujos de conversación desde el archivo JSON"""
        try:
            ruta = Path(__file__).parent / self.archivo_flujos
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.config = data['configuracion']
            self.flujos = data['flujos']
            print("✓ Flujos de conversación cargados correctamente\n")

        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.archivo_flujos}")
            exit(1)
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo {self.archivo_flujos} no es un JSON válido")
            exit(1)

    def normalizar_texto(self, texto):
        """
        Normaliza el texto del usuario para mejorar coincidencias

        Args:
            texto: Texto a normalizar

        Returns:
            Texto normalizado (minúsculas, sin tildes, sin puntuación extra)
        """
        # Convertir a minúsculas
        texto = texto.lower()

        # Eliminar tildes
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

        # Remover puntuación excesiva pero mantener espacios
        texto = re.sub(r'[^\w\s]', '', texto)

        # Normalizar espacios
        texto = ' '.join(texto.split())

        return texto

    def calcular_similitud(self, texto1, texto2):
        """
        Calcula la similitud entre dos textos usando difflib

        Args:
            texto1: Primer texto
            texto2: Segundo texto

        Returns:
            Score de similitud entre 0.0 y 1.0
        """
        return difflib.SequenceMatcher(None, texto1, texto2).ratio()

    def buscar_mejor_intencion(self, mensaje_usuario):
        """
        Busca la mejor intención que coincida con el mensaje del usuario

        Args:
            mensaje_usuario: Mensaje del usuario (ya normalizado)

        Returns:
            Tupla (intencion, score, flujo_nombre) o (None, 0, None)
        """
        mejor_intencion = None
        mejor_score = 0
        mejor_flujo = None

        # Buscar en todos los flujos
        for nombre_flujo, flujo in self.flujos.items():
            for intencion in flujo['intenciones']:
                # Calcular similitud con cada patrón
                for patron in intencion['patrones']:
                    patron_normalizado = self.normalizar_texto(patron)

                    # Similitud general
                    score = self.calcular_similitud(mensaje_usuario, patron_normalizado)

                    # Bonus si la palabra clave está contenida exactamente
                    if patron_normalizado in mensaje_usuario:
                        score = max(score, 0.8)

                    # Bonus si todas las palabras del patrón están en el mensaje
                    palabras_patron = patron_normalizado.split()
                    palabras_mensaje = mensaje_usuario.split()
                    if all(palabra in palabras_mensaje for palabra in palabras_patron):
                        score = max(score, 0.85)

                    if score > mejor_score:
                        mejor_score = score
                        mejor_intencion = intencion
                        mejor_flujo = nombre_flujo

        return mejor_intencion, mejor_score, mejor_flujo

    def seleccionar_respuesta(self, intencion):
        """
        Selecciona una respuesta aleatoria de la intención

        Args:
            intencion: Diccionario con la intención

        Returns:
            String con la respuesta
        """
        respuestas = intencion['respuestas']
        respuesta = random.choice(respuestas)

        # Agregar sugerencia si existe
        if 'siguiente_sugerencia' in intencion:
            respuesta += f"\n\n💡 {intencion['siguiente_sugerencia']}"

        return respuesta

    def procesar_mensaje(self, mensaje_usuario):
        """
        Procesa el mensaje del usuario y genera una respuesta

        Args:
            mensaje_usuario: Mensaje del usuario

        Returns:
            Respuesta del bot, o None si debe terminar
        """
        # Normalizar mensaje
        mensaje_normalizado = self.normalizar_texto(mensaje_usuario)

        # Guardar en historial
        self.contexto['historial'].append(mensaje_usuario)

        # Buscar mejor intención
        intencion, score, flujo = self.buscar_mejor_intencion(mensaje_normalizado)

        # Decidir respuesta
        if score >= self.config['umbral_similitud']:
            # Actualizar contexto
            self.contexto['ultima_intencion'] = intencion['id']
            self.contexto['flujo_actual'] = flujo

            # Verificar acciones especiales
            if 'accion_especial' in intencion:
                if intencion['accion_especial'] == 'terminar':
                    return self.seleccionar_respuesta(intencion), True

            return self.seleccionar_respuesta(intencion), False
        else:
            # No se entendió el mensaje
            return self.config['mensaje_no_entendido'], False

    def ejecutar(self):
        """Ejecuta el loop principal del chatbot"""
        print("=" * 70)
        print("CHATBOT BASADO EN REGLAS - CURSO DE CHATBOTS")
        print("=" * 70)
        print(self.config['mensaje_bienvenida'])
        print("=" * 70)

        # Loop principal
        while True:
            try:
                # Capturar input del usuario
                mensaje = input("\n🧑 Tú: ").strip()

                # Validar input vacío
                if not mensaje:
                    continue

                # Verificar comando de salida directo
                if mensaje.lower() in ['salir', 'exit', 'quit']:
                    print(f"\n🤖 Bot: {self.config['mensaje_despedida']}")
                    break

                # Procesar mensaje
                respuesta, debe_terminar = self.procesar_mensaje(mensaje)

                # Mostrar respuesta
                print(f"\n🤖 Bot: {respuesta}")

                # Terminar si es necesario
                if debe_terminar:
                    break

            except KeyboardInterrupt:
                print(f"\n\n🤖 Bot: {self.config['mensaje_despedida']}")
                break
            except Exception as e:
                print(f"\n❌ Error interno: {e}")
                print("Por favor, intenta de nuevo.")

        print("\n" + "=" * 70)
        print("Conversación terminada. ¡Gracias por usar el chatbot!")
        print("=" * 70)

    def mostrar_estadisticas(self):
        """Muestra estadísticas de la conversación"""
        print("\n📊 Estadísticas de la conversación:")
        print(f"  - Mensajes del usuario: {len(self.contexto['historial'])}")
        print(f"  - Último flujo usado: {self.contexto['flujo_actual']}")
        print(f"  - Última intención: {self.contexto['ultima_intencion']}")


def main():
    """Función principal"""
    # Crear instancia del chatbot
    bot = ChatbotReglas()

    # Ejecutar
    bot.ejecutar()

    # Mostrar estadísticas (opcional)
    # bot.mostrar_estadisticas()


if __name__ == "__main__":
    main()
