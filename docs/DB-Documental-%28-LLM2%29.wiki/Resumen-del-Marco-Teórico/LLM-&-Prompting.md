[[_TOC_]]


# Introducción
---

Un modelo de lenguaje grande (LLM, por sus siglas en inglés) es un tipo de modelo de inteligencia artificial que está diseñado para comprender y generar texto en varios idiomas. Utiliza técnicas de aprendizaje automático avanzadas para analizar grandes cantidades de datos de texto y aprender las reglas y patrones del lenguaje. Los LLM pueden generar texto coherente y relevante, responder preguntas y realizar tareas basadas en el lenguaje. Estos modelos son muy útiles en aplicaciones como la traducción automática, la generación de texto y la asistencia en la redacción de contenido. Sin embargo, es importante tener en cuenta que los LLM también pueden tener limitaciones y desafíos éticos, como la propagación de información falsa o sesgada si no se controlan adecuadamente.

## Técnicas de ML más usadas

A continuación se enlistan brevemente algunos de los tipos de técnicas avanzadas de aprendizaje automático utilizadas en los "Large Language Models":

1. **Aprendizaje profundo (Deep Learning):** Este enfoque utiliza redes neuronales artificiales con múltiples capas para aprender y representar de manera jerárquica la estructura del lenguaje.
2. **Transformers:** Los transformers son una arquitectura de red neuronal que permite capturar las relaciones de largo alcance entre palabras y generar representaciones contextualizadas.
3. **Aprendizaje por refuerzo (Reinforcement Learning):** Esta técnica implica que el modelo aprenda a través de la interacción con su entorno, recibiendo recompensas o castigos según las acciones tomadas.
4. **Aprendizaje semi-supervisado (Semi-Supervised Learning):** En este enfoque, se utiliza una combinación de datos etiquetados y no etiquetados para entrenar al modelo, lo que permite aprovechar un mayor volumen de información.
5. **Aprendizaje activo (Active Learning):** En lugar de recibir un conjunto estático de datos de entrenamiento, este enfoque permite que el modelo seleccione activamente qué datos le resultan más útiles para aprender.

Estas son solo algunas de las técnicas utilizadas en los Large Language Models, que les permiten comprender y generar texto de manera efectiva en varios idiomas.

## Efectividad de los LMs

La efectividad de los Language Models depende de los siguientes factores:

- Tamaño de la arquitectura de las Redes Neuronales
- Parámetros de las Redes Neuronales (A mayor cantidad de parámetros, mejor desempeño)
- Transformers (Mecanismos de Atención y Word Embeddings)

# Transfer Learning
---

El Transfer Learning, o aprendizaje por transferencia, es un concepto clave en el campo del aprendizaje automático y la inteligencia artificial. Consiste en aprovechar el conocimiento y la experiencia adquiridos al resolver una tarea para aplicarlos en otra tarea relacionada. En el contexto de los modelos de lenguaje, el Transfer Learning implica utilizar un modelo previamente entrenado en una gran cantidad de datos para luego adaptarlo a una tarea específica utilizando un conjunto de datos más pequeño.

La idea principal detrás del Transfer Learning es que un modelo previamente entrenado pueda capturar características generales del lenguaje y del dominio, lo que lo convierte en un punto de partida sólido para resolver nuevas tareas. Al utilizar Transfer Learning, se pueden lograr resultados prometedores incluso con conjuntos de datos más limitados, ya que el modelo ya ha aprendido patrones y estructuras relevantes en un contexto más amplio.

# Arquitecturas de los Transformers
---

A continuación se enumeran algunas de las arquitecturas de los Transformers utilizadas en la inteligencia artificial:

1. **BERT (Bidirectional Encoder Representations from Transformers):** BERT es un modelo de lenguaje basado en Transformers que utiliza la atención bidireccional para capturar el contexto tanto a la izquierda como a la derecha de una palabra en una oración.
2. **GPT (Generative Pre-trained Transformer):** GPT es un modelo de lenguaje que utiliza Transformers para generar texto coherente y relevante. Se entrena en grandes cantidades de datos para aprender las reglas y patrones del lenguaje.
3. **T5 (Text-to-Text Transfer Transformer):** T5 es un modelo de lenguaje basado en Transformers diseñado para realizar una variedad de tareas de procesamiento de lenguaje natural, como traducción automática, resumen de texto y generación de preguntas y respuestas.
4. **XLNet:** XLNet es una variante de los Transformers que utiliza una atención permutada para capturar las dependencias de largo alcance en el texto. Esto permite que el modelo capture relaciones más complejas entre las palabras.
5. **RoBERTa (Robustly Optimized BERT Pretraining Approach):** RoBERTa es una mejora del modelo BERT que se entrena con una mayor cantidad de datos y durante más tiempo. Esto le permite obtener un mejor rendimiento en una amplia gama de tareas de procesamiento de lenguaje natural.

Estas son algunas de las arquitecturas de los Transformers utilizadas en la inteligencia artificial para comprender y generar texto de manera efectiva.

## Encoder

Un modelo codificador en un LLM (Large Language Model) es una parte fundamental de la arquitectura del modelo. El objetivo principal del codificador es procesar y comprender la información de entrada, como texto o secuencias de palabras. Utiliza técnicas avanzadas de aprendizaje automático, como las redes neuronales, para extraer características y representaciones significativas de los datos de entrada.

El codificador de un LLM puede ser una red neuronal profunda o una arquitectura basada en Transformers. Transforma las palabras o secuencias de palabras en vectores de alta dimensionalidad, donde cada dimensión representa una característica o aspecto específico del texto. Estos vectores de características capturan la información semántica y contextual del texto, lo que permite al modelo comprender y generar texto coherente y relevante.

El codificador procesa la información de manera secuencial, teniendo en cuenta las relaciones entre las palabras y las estructuras gramaticales del lenguaje. A medida que se avanza en la secuencia de entrada, el codificador va actualizando su estado interno y generando representaciones contextualizadas de las palabras. Estas representaciones se utilizan posteriormente en la etapa de decodificación para generar texto o realizar tareas basadas en el lenguaje.

En resumen, un modelo codificador en un LLM es responsable de procesar y comprender la información de entrada, generando representaciones de alta dimensionalidad que capturan la semántica y el contexto del texto. Estas representaciones son fundamentales para que el LLM pueda generar texto coherente y relevante en diferentes idiomas y tareas de procesamiento del lenguaje natural.

## Decoder

Un decodificador en un LLM (Large Language Model) es una parte esencial de la arquitectura del modelo. Su función principal es generar texto comprensible y relevante basado en la información de entrada y las representaciones generadas por el codificador.

El decodificador utiliza técnicas avanzadas de aprendizaje automático, como redes neuronales y Transformers, para transformar las representaciones internas del codificador en texto legible y coherente. A medida que genera el texto, el decodificador considera el contexto y las estructuras gramaticales del lenguaje, asegurando que las palabras y las frases generadas sean fluidas y sigan las reglas lingüísticas adecuadas.

El proceso de decodificación implica utilizar las representaciones internas del codificador y aplicar técnicas de generación de texto, como la atención y la selección de palabras, para producir el texto final. El decodificador tiene en cuenta el contexto previo y la información generada hasta el momento para tomar decisiones sobre las palabras y frases siguientes.

En resumen, el decodificador en un LLM es responsable de generar texto coherente y relevante basado en las representaciones internas del codificador. Es una parte integral del modelo que utiliza técnicas avanzadas de aprendizaje automático para producir resultados comprensibles y de calidad en diversas tareas de procesamiento del lenguaje natural.

## Comparación de arquitecturas

|  | Codificador | Decodificador |
| --- | --- | --- |
| Función principal | Procesar y comprender la información de entrada | Generar texto comprensible y relevante |
| Técnicas utilizadas | Redes neuronales y Transformers | Redes neuronales y Transformers |
| Transformación de datos de entrada | Extracción de características y representaciones significativas | Transformación de representaciones internas en texto legible y coherente |
| Actualización del estado interno | Sí | No |
| Generación de representaciones contextualizadas | Sí | No |
| Consideración del contexto y estructuras gramaticales | No | Sí |
| Toma de decisiones basada en contexto previo | No | Sí |
| Tareas principales | Procesamiento de información de entrada | Generación de texto coherente y relevante |
| Importancia en el modelo | Fundamental | Esencial |

<center>

![Untitled.png](/.attachments/Untitled-c2198aa3-8e7c-409c-922c-58b20d05d2cc.png)
_LLM Árbol de evolución_

</center>

# RLHF
---

El aprendizaje por refuerzo a partir de la retroalimentación humana (RLHF) es un enfoque en el campo del aprendizaje automático y la inteligencia artificial en el cual un modelo de inteligencia artificial aprende de manera iterativa a través de la interacción con humanos. En lugar de basarse únicamente en recompensas o castigos definidos por un sistema de recompensas predefinido, el RLHF emplea la retroalimentación proporcionada por los humanos para guiar el aprendizaje del modelo.

En el RLHF, los humanos actúan como agentes de entrenamiento, brindando al modelo información adicional sobre qué acciones son deseables o indeseables en un determinado contexto. Esta retroalimentación puede ser proporcionada en forma de evaluaciones explícitas, como etiquetas o clasificaciones, o a través de interacciones directas con el modelo, como correcciones o sugerencias.

El objetivo del RLHF es mejorar el desempeño del modelo, permitiéndole aprender de manera más efectiva y eficiente a través de la guía humana. Al incorporar la experiencia y el conocimiento humano, el RLHF busca superar las limitaciones del aprendizaje por refuerzo tradicional y obtener resultados más precisos y adaptados a las preferencias y objetivos específicos de los humanos involucrados.

En resumen, el aprendizaje por refuerzo a partir de la retroalimentación humana es un enfoque en el que un modelo de inteligencia artificial aprende a través de la interacción con humanos, utilizando la retroalimentación proporcionada por estos para mejorar su desempeño y lograr resultados más alineados con las necesidades y preferencias humanas.

<center>

![Untitled 1.png](/.attachments/Untitled%201-7686c99c-82b4-40fe-b93c-c03dc868a150.png)
_Chat GPT RLHF Training process_

</center>

# Prompt Engineering
---

La ingeniería de prompts es un enfoque en el campo del procesamiento del lenguaje natural que se centra en la creación y diseño de instrucciones o indicaciones para guiar y obtener resultados más precisos de los modelos de lenguaje. Se trata de formular de manera estratégica preguntas o frases de inicio que permitan al modelo comprender y generar texto coherente y relevante en función de la tarea o la información deseada. La ingeniería de prompts es especialmente útil para ajustar y personalizar los resultados de los modelos de lenguaje, asegurando que se alineen con las necesidades y las intenciones específicas de los usuarios o las aplicaciones.

## Casos de uso

A continuación se enumeran algunos casos de uso comunes de la ingeniería de prompts:

1. **Generación de respuestas específicas:** Al diseñar prompts adecuados, es posible guiar a los modelos de lenguaje para que generen respuestas específicas a preguntas o solicitudes particulares. Por ejemplo, se puede utilizar un prompt para obtener una respuesta precisa a una pregunta sobre una fecha histórica o para obtener una descripción detallada de un producto en particular.
2. **Personalización de respuestas:** La ingeniería de prompts permite personalizar los resultados de los modelos de lenguaje para que se ajusten a las preferencias individuales o las necesidades específicas de los usuarios. Por ejemplo, se puede diseñar un prompt para obtener recomendaciones de películas basadas en géneros o preferencias personales.
3. **Generación de contenido creativo:** Mediante la ingeniería de prompts, se pueden estimular modelos de lenguaje para generar contenido creativo, como poemas, historias cortas o canciones. Al proporcionar instrucciones o indicaciones específicas, se puede influir en el estilo o la temática del contenido generado.
4. **Traducción automática:** La ingeniería de prompts también se puede utilizar para mejorar la calidad y la precisión de las traducciones automáticas. Al proporcionar frases de inicio en el idioma de origen y el idioma de destino, se puede guiar al modelo para que genere traducciones más precisas y coherentes.
5. **Generación de código:** En el ámbito de la programación, la ingeniería de prompts puede ayudar a los modelos de lenguaje a generar código o soluciones para problemas específicos. Al proporcionar una descripción del problema y las restricciones, se puede obtener código funcional o sugerencias de solución.

Estos son solo algunos ejemplos de cómo se puede utilizar la ingeniería de prompts para mejorar y personalizar los resultados de los modelos de lenguaje en una amplia gama de aplicaciones y escenarios.

## Componentes de un Prompt

Un prompt consta de varios componentes que ayudan a guiar y obtener resultados más precisos de los modelos de lenguaje. Los componentes clave de un prompt son:

1. **Instrucciones:** Son las indicaciones o preguntas que se formulan para guiar al modelo y solicitar una respuesta específica. Las instrucciones deben ser claras, concisas y específicas, para que el modelo comprenda correctamente la tarea o la información deseada.
2. **Contexto inicial:** Es el texto o la información proporcionada antes del prompt en sí. El contexto inicial puede ayudar a establecer el escenario o el contexto en el que se realiza la tarea. Puede incluir datos relevantes, ejemplos o cualquier información adicional necesaria para que el modelo genere una respuesta coherente.
3. **Ejemplos de entrada y salida:** Los ejemplos de entrada y salida son pares de texto que ilustran la relación esperada entre una entrada y su correspondiente salida. Estos ejemplos pueden ayudar al modelo a comprender el formato y la estructura deseada de la respuesta. Los ejemplos de entrada y salida pueden ser especialmente útiles en tareas de generación de texto, donde se desea un formato específico de respuesta.
4. **Parámetros de configuración:** Los parámetros de configuración son ajustes o especificaciones adicionales que se pueden proporcionar al modelo para influir en su comportamiento. Estos parámetros pueden incluir información sobre el estilo, la longitud de la respuesta, las restricciones o cualquier otra preferencia que se desee aplicar al resultado generado.

Al combinar estos elementos de un prompt de manera efectiva, se puede guiar y personalizar la salida de los modelos de lenguaje, asegurando que se ajusten a las necesidades y requerimientos específicos de la tarea o la aplicación.

## Técnicas de Prompting

A continuación se enlistan algunas técnicas de prompting utilizadas en el procesamiento del lenguaje natural:

1. **Prompting directo:** Esta técnica consiste en proporcionar una instrucción clara y directa al modelo, indicándole exactamente lo que se espera como respuesta. Se utiliza cuando se desea una respuesta específica y precisa.
2. **Prompting en etapas:** Esta técnica implica dividir la tarea en etapas o pasos más pequeños y proporcionar instrucciones específicas para cada uno de ellos. Se utiliza para guiar al modelo en la generación de respuestas más detalladas y estructuradas.
3. **Prompting inverso:** En esta técnica, se plantea la pregunta o solicitud en sentido inverso, es decir, se proporciona la respuesta deseada y se le pide al modelo que genere la pregunta correspondiente. Se utiliza para fomentar la creatividad y la generación de preguntas interesantes.
4. **Prompting con ejemplos:** Esta técnica implica proporcionar ejemplos de entrada y salida que ilustren la relación esperada entre una pregunta y su respuesta. Los ejemplos ayudan al modelo a entender el formato y la estructura deseada de la respuesta.
5. **Prompting condicional:** En esta técnica, se establecen condiciones o restricciones específicas para guiar al modelo en la generación de respuestas. Por ejemplo, se puede indicar al modelo que genere una respuesta en forma de lista o que incluya ciertas palabras clave.
6. **Prompting por similitud:** Esta técnica consiste en proporcionar al modelo ejemplos similares o relacionados con la tarea o el contexto deseado. Se utiliza para ayudar al modelo a comprender mejor la tarea y generar respuestas coherentes.

Estas son algunas de las técnicas de prompting utilizadas en el procesamiento del lenguaje natural para guiar y obtener resultados más precisos de los modelos de lenguaje.

## Dificultades de los LLM

Estas son algunas de las dificultades más importantes que presentan los modelos LLM:

1. **Escasez de datos anotados:** Los modelos de lenguaje requieren grandes cantidades de datos anotados para entrenarse de manera efectiva. Sin embargo, puede ser difícil encontrar conjuntos de datos suficientes y de alta calidad para entrenar modelos LLM en ciertos dominios o idiomas específicos.
2. **Sesgos y discriminación en los datos de entrenamiento:** Los modelos LLM aprenden de los datos en los que se basan, lo que significa que pueden reflejar los sesgos y prejuicios presentes en esos datos. Esto puede llevar a resultados sesgados o discriminatorios en la generación de texto, lo que plantea preocupaciones éticas y de equidad.
3. **Interpretabilidad y explicabilidad limitadas:** Los modelos LLM son conocidos por ser cajas negras, lo que significa que es difícil comprender cómo y por qué toman ciertas decisiones. Esto puede dificultar la explicación de los resultados generados por el modelo y puede afectar la confianza en su uso en aplicaciones críticas.
4. **Incorporación de conocimiento externo:** Los modelos LLM a menudo tienen dificultades para incorporar conocimientos externos o actualizaciones en tiempo real. Esto puede limitar su capacidad para generar respuestas precisas y actualizadas en situaciones cambiantes o en dominios especializados.
5. **Generación de contenido no coherente o irrelevante:** Los modelos LLM pueden generar texto que carece de coherencia o relevancia en ciertos contextos. Esto puede deberse a la falta de comprensión contextual o a la falta de capacidad para capturar la intención o el propósito detrás de una solicitud.

Estas dificultades representan desafíos importantes en el desarrollo y la aplicación de modelos LLM, y requieren consideraciones cuidadosas en términos de selección de datos, mitigación de sesgos y garantía de la interpretabilidad y la calidad del modelo.

# **Enlaces de Referencia**
---

1. OpenAI. "Chat GPT." OpenAI, 2021. [Link](https://openai.com/chatgpt)
2. Brown, Tom B., et al. "Language Models are Few-Shot Learners." arXiv preprint arXiv:2005.14165 (2020). [Link](https://arxiv.org/abs/2005.14165)
3. Petroni, Fabio, et al. "Language Models as Knowledge Bases?" arXiv preprint arXiv:1909.01066 (2019). [Link](https://arxiv.org/abs/1909.01066)
4. Radford, Alec, et al. "Language models are unsupervised multitask learners." OpenAI Blog, 2019. [Link](https://openai.com/blog/better-language-models/)
5. Dodge, Jesse, et al. "Fine-tuning language models from human feedback." arXiv preprint arXiv:1909.08593 (2019). [Link](https://arxiv.org/abs/1909.08593)