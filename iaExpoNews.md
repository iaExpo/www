---
name: iaexpo-news
description: Convierte un correo de noticias de IA (LinkedIn News, newsletters, alertas) en un artículo HTML editorial en español con la identidad de IA Expo Internacional, listo para pegar en GoHighLevel como Custom HTML y en iaExpo.ai. Genera masthead con logo IAx, banner hero, headline, dropcap, pull quote, lista de reacciones, sección de análisis "Por qué importa para la comunidad IA<sup>x</sup>", bloque de fuente y CTA a iaexpo.ai.
---

## When to use

Usa este skill cuando el usuario:
- Esté leyendo un correo de noticias (LinkedIn News, Fortune, newsletters de IA, alertas) y pida convertirlo en artículo para iaExpo.ai o GoHighLevel.
- Diga frases como "haz un artículo de esto para IA Expo", "conviértelo en HTML para GHL", "resumen editorial estilo IA Expo", "newsletter de esto".
- Invoque explícitamente `/iaexpo-news`.

No lo uses para correos transaccionales, respuestas personales, o cuando el usuario solo quiera un resumen en chat sin HTML.

## Inputs que necesitas

Antes de generar el HTML, asegúrate de tener:

1. **Contenido fuente** — del cuerpo del correo abierto (`<user_context>` ya lo trae). Identifica:
   - Hecho principal (qué pasó, quién, dónde, cuándo).
   - Cita textual fuerte (si existe). Va en el pull quote.
   - Reacciones/voces destacadas (típicamente 3–5 personas u organizaciones con un comentario o ángulo cada una).
   - URL de la historia original (si está disponible — para el bloque de fuente).

2. **Idioma y variedad** — **español mexicano (es-MX) obligatorio**. Es la voz estándar de IA Expo Internacional para publicación en GoHighLevel y en iaExpo.ai. Aplica incluso cuando el correo fuente viene en español peninsular (España) o en inglés. Reglas concretas en la sección "Español mexicano" más abajo.

3. **Tono** — periodístico, analítico, con un cierre que conecte la noticia con la transformación del trabajo o la industria con IA (la voz de IA Expo Internacional).

Si falta una cita textual fuerte, omite el pull quote. Si faltan reacciones, omite la sección "El eco en LinkedIn" / "Voces". No inventes datos, citas, ni números de reacciones.

## Constantes de marca (no las cambies sin que el usuario lo pida)

- **Nombre publicación:** IA Expo Internacional
- **Dominio:** iaExpo.ai (capital E en la "E")
- **URL home:** `https://iaexpo.ai`
- **CTA URL:** `https://iaexpo.ai/#contacto`
- **CTA texto:** `Únete a la comunidad IA Expo →`
- **Comunidad en análisis:** `comunidad IA<sup>x</sup>` (con sup)
- **Paleta:**
  - Azul oscuro / navy: `#0b1f3a`
  - Azul brand: `#0a66c2`
  - Azul claro accent: `#7DD3FC`
  - Fondo página: `#f4f5f7`
  - Tarjeta: `#ffffff`
  - Texto cuerpo: `#1e293b`
  - Texto secundario: `#475569` / `#64748b`
  - Bordes suaves: `#e2e8f0`
- **Tipografía:**
  - Sans para UI: `-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif`
  - Serif para headlines/quotes: `Georgia,'Times New Roman',serif`
- **Ancho contenedor:** 720px
- **Imágenes (URLs estables en la CDN de GoHighLevel):**
  - Logo IAx (masthead, 28x28 redondeado): `https://assets.cdn.filesafe.space/5RXj1eDQIjNx7eCHKaZA/media/68fd1b0147cb3b35acb31d75.jpeg`
  - Banner hero: `https://assets.cdn.filesafe.space/5RXj1eDQIjNx7eCHKaZA/media/695c2db1d907492962090e4f.jpg`
- **Orden de bloques (fijo):**
  1. Masthead (logo IAx + nombre + fecha)
  2. Banner hero
  3. Kicker + headline + dech + byline
  4. Divisor azul
  5. Cuerpo con dropcap en la primera palabra
  6. Pull quote (si hay cita fuerte)
  7. Sección "El eco en LinkedIn" / lista de reacciones (si hay)
  8. Sección "Análisis — Por qué importa para la comunidad IA<sup>x</sup>"
  9. Source block oscuro con link a la historia original
  10. CTA pill
  11. Footer

## Workflow

1. **Lee el correo abierto.** El cuerpo y los metadatos están en `<user_context>` y `<initial_state>`. No llames a Graph ni a `body.getAsync` — ya tienes el texto.
2. **Extrae:** hecho principal, cita textual, lista de reacciones (nombre + una línea de ángulo cada una), URL de la fuente.
3. **Redacta en español editorial:** kicker (2–3 palabras MAYÚSCULA pequeña), headline (1 oración fuerte, 12–22 palabras), dech (1 oración de apoyo), cuerpo (1–2 párrafos densos), pull quote si aplica, voces (1 línea por persona, 3–5 ítems), análisis (2 párrafos: contexto + cierre con la voz de IA Expo).
4. **Identifica imágenes editoriales del correo fuente** (si las hay). Ver sección "Imágenes del correo fuente" abajo.
5. **Arma el HTML** usando la plantilla de abajo, respetando orden de bloques, paleta y constantes de marca. Inserta las imágenes editoriales del correo fuente en el bloque correspondiente.
6. **Entrega el HTML en un bloque de código** listo para pegar en GoHighLevel como Custom HTML. No envuelvas en `<html>/<body>` — solo el `<table>` raíz. El bloque debe llevar una etiqueta de nombre de archivo con el formato `yyyy.mm.dd <fuente>.html` (ver sección "Nombrado del bloque de código" abajo).
7. **Done when:** El HTML respeta el orden masthead → banner → contenido, usa todas las constantes de marca, no contiene placeholders ni datos inventados, las imágenes editoriales del correo fuente están incluidas (si existían), el bloque va precedido del nombre de archivo correcto, y el usuario tiene un bloque copy-paste listo.

## Plantilla HTML base

Reemplaza los marcadores `{{...}}` con el contenido derivado del correo. Si una sección no aplica (sin pull quote, sin reacciones), borra el `<tr>` completo de ese bloque.

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#f4f5f7; padding:32px 12px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <tr>
    <td align="center">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="720" style="max-width:720px; width:100%; background:#ffffff; border-radius:14px; box-shadow:0 8px 24px rgba(15,23,42,0.08); overflow:hidden;">

        <!-- MASTHEAD -->
        <tr>
          <td style="background:linear-gradient(135deg,#0b1f3a 0%,#0a66c2 100%); padding:18px 32px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td align="left" valign="middle" style="color:#ffffff; font-size:13px; letter-spacing:2px; text-transform:uppercase; font-weight:700;">
                  <img src="https://assets.cdn.filesafe.space/5RXj1eDQIjNx7eCHKaZA/media/68fd1b0147cb3b35acb31d75.jpeg" alt="IAx" width="28" height="28" style="vertical-align:middle; border-radius:6px; margin-right:10px; display:inline-block;">
                  <span style="vertical-align:middle;">IA Expo Internacional &nbsp;•&nbsp; Noticias</span>
                </td>
                <td align="right" valign="middle" style="color:#cbd5e1; font-size:12px; letter-spacing:1px; text-transform:uppercase; font-weight:500;">
                  {{FECHA_LARGA_ES}}
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- HERO BANNER -->
        <tr>
          <td style="line-height:0; font-size:0;">
            <img src="https://assets.cdn.filesafe.space/5RXj1eDQIjNx7eCHKaZA/media/695c2db1d907492962090e4f.jpg" alt="IA Expo Internacional" width="720" style="display:block; width:100%; max-width:720px; height:auto;">
          </td>
        </tr>

        <!-- KICKER + HEADLINE -->
        <tr>
          <td style="padding:36px 40px 0 40px;">
            <p style="margin:0 0 14px; display:inline-block; background:#0a66c2; color:#ffffff; font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding:6px 12px; border-radius:4px;">{{KICKER}}</p>
            <h1 style="margin:0; font-family:Georgia,'Times New Roman',serif; font-size:36px; line-height:1.15; color:#0b1f3a; font-weight:700; letter-spacing:-0.5px;">
              {{HEADLINE}}
            </h1>
            <p style="margin:18px 0 0; font-size:18px; line-height:1.5; color:#475569; font-weight:400;">
              {{DECH_SUBHEADLINE}}
            </p>
            <p style="margin:20px 0 0; font-size:13px; color:#64748b; letter-spacing:0.3px;">
              Por la redacción de <strong style="color:#0b1f3a;">IA Expo Internacional</strong> &nbsp;|&nbsp; Tiempo de lectura: {{TIEMPO_LECTURA}} min
            </p>
          </td>
        </tr>

        <!-- DIVIDER -->
        <tr>
          <td style="padding:24px 40px 0 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr><td style="border-top:3px solid #0a66c2; line-height:0; font-size:0;">&nbsp;</td></tr>
            </table>
          </td>
        </tr>

        <!-- BODY -->
        <tr>
          <td style="padding:24px 40px 8px 40px; font-size:16px; line-height:1.7; color:#1e293b;">
            <p style="margin:0;">
              <span style="float:left; font-family:Georgia,'Times New Roman',serif; font-size:62px; line-height:50px; color:#0a66c2; font-weight:700; padding:4px 12px 0 0;">{{PRIMERA_LETRA}}</span>{{RESTO_PRIMER_PARRAFO}}
            </p>
          </td>
        </tr>

        <!-- PULL QUOTE (omitir <tr> si no hay cita) -->
        <tr>
          <td style="padding:8px 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f1f5fb; border-left:5px solid #0a66c2; border-radius:0 8px 8px 0;">
              <tr>
                <td style="padding:24px 28px;">
                  <p style="margin:0; font-family:Georgia,'Times New Roman',serif; font-size:22px; line-height:1.4; color:#0b1f3a; font-style:italic; font-weight:500;">
                    "{{CITA_TEXTUAL}}"
                  </p>
                  <p style="margin:14px 0 0; font-size:12px; color:#475569; letter-spacing:1px; text-transform:uppercase; font-weight:600;">
                    — {{AUTOR_CITA}}
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- SECTION: REACCIONES (omitir si no hay) -->
        <tr>
          <td style="padding:28px 40px 0 40px;">
            <p style="margin:0 0 16px; font-size:11px; color:#0a66c2; font-weight:700; letter-spacing:2px; text-transform:uppercase;">{{KICKER_REACCIONES}}</p>
            <h2 style="margin:0 0 14px; font-family:Georgia,'Times New Roman',serif; font-size:24px; color:#0b1f3a; font-weight:700;">
              {{TITULO_REACCIONES}}
            </h2>
          </td>
        </tr>
        <tr>
          <td style="padding:0 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
              <!-- repetir <tr> por cada voz; última fila sin border-bottom -->
              <tr><td style="padding:14px 0; border-bottom:1px solid #e2e8f0; font-size:15px; line-height:1.6; color:#334155;">
                <strong style="color:#0b1f3a;">{{NOMBRE_VOZ}}</strong> &nbsp;<span style="color:#94a3b8;">·</span>&nbsp; {{ANGULO_VOZ}}
              </td></tr>
            </table>
          </td>
        </tr>

        <!-- SECTION: ANÁLISIS -->
        <tr>
          <td style="padding:36px 40px 0 40px;">
            <p style="margin:0 0 16px; font-size:11px; color:#0a66c2; font-weight:700; letter-spacing:2px; text-transform:uppercase;">Análisis</p>
            <h2 style="margin:0 0 14px; font-family:Georgia,'Times New Roman',serif; font-size:24px; color:#0b1f3a; font-weight:700;">
              Por qué importa para la comunidad IA<sup>x</sup>
            </h2>
            <p style="margin:0 0 14px; font-size:16px; line-height:1.7; color:#1e293b;">
              {{PARRAFO_CONTEXTO}}
            </p>
            <p style="margin:0; font-size:16px; line-height:1.7; color:#1e293b;">
              En <strong>IA Expo Internacional</strong> {{CIERRE_VOZ_MARCA}}
            </p>
          </td>
        </tr>

        <!-- SOURCE BLOCK -->
        <tr>
          <td style="padding:36px 40px 0 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#0b1f3a; border-radius:10px;">
              <tr>
                <td style="padding:22px 26px;">
                  <p style="margin:0 0 6px; font-size:10px; color:#7DD3FC; font-weight:700; letter-spacing:2px; text-transform:uppercase;">Fuente</p>
                  <p style="margin:0; font-size:14px; line-height:1.6; color:#e2e8f0;">
                    <a href="{{URL_FUENTE}}" style="color:#ffffff; text-decoration:underline; font-weight:600;">{{NOMBRE_FUENTE}}</a><br>
                    <span style="color:#94a3b8;">{{NOTA_FUENTE}}</span>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- CTA -->
        <tr>
          <td align="center" style="padding:36px 40px 8px 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:#0a66c2; border-radius:999px;">
                  <a href="https://iaexpo.ai/#contacto" style="display:inline-block; padding:14px 36px; font-size:14px; font-weight:700; letter-spacing:0.5px; color:#ffffff; text-decoration:none; text-transform:uppercase;">
                    Únete a la comunidad IA Expo →
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- FOOTER -->
        <tr>
          <td style="padding:24px 40px 32px 40px; border-top:1px solid #e2e8f0;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="font-size:12px; color:#64748b; line-height:1.6;">
                  Publicado por <strong style="color:#0b1f3a;">IA Expo Internacional</strong><br>
                  <a href="https://iaexpo.ai" style="color:#0a66c2; text-decoration:none; font-weight:600;">iaExpo.ai</a>
                </td>
                <td align="right" style="font-size:11px; color:#94a3b8; letter-spacing:1px; text-transform:uppercase;">
                  © {{AÑO}}
                </td>
              </tr>
            </table>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
```

## Reglas editoriales

- **Headline:** evita títulos sensacionalistas estilo clickbait. Usa una oración informativa con tensión ("X despide a Y y enciende debate sobre Z"). Sin signos de exclamación. Sin "OMG", "increíble", "no vas a creer".
- **Dech:** complementa el headline, no lo repite. Aporta el dato más importante o el contexto.
- **Cuerpo:** 1–2 párrafos. Quién, qué, dónde, cuándo, por qué. Densidad informativa.
- **Pull quote:** solo si hay cita textual fuerte y atribuible. No parafrasees ni inventes.
- **Reacciones:** 3–5 voces máximo. Una línea por persona con su ángulo. No repitas la opinión central; busca pluralidad.
- **Análisis:** conecta la noticia con la transformación del trabajo, automatización, gobernanza, talento, modelos humano+IA, o el ángulo que sea relevante. El cierre siempre debe sonar como IA Expo: editorial, prospectivo, sin tomar partido político.
- **Sin em dashes (—)** en el texto editorial; usa comas, paréntesis o punto. El único em dash permitido es el que precede al autor de la cita ("— Nombre").
- **Sin frases prefab:** "no te lo pierdas", "click aquí", "sigue leyendo", "¿qué opinas?".

## Español mexicano (es-MX) — voz estándar de IA Expo Internacional

Todo el contenido editorial generado (headline, dech, cuerpo, pull quote, listas, análisis) va en español mexicano neutro profesional. Cuando el correo fuente está escrito en español peninsular (España) o en inglés, traduce y adapta a esta variedad. Las citas textuales atribuibles a una fuente se conservan en su idioma y registro originales para fidelidad documental (un tweet en inglés queda en inglés; una declaración en español peninsular conserva sus marcas regionales).

### Pronombres y conjugaciones

- **"Ustedes" en lugar de "vosotros".** Nunca uses voseo argentino ni vosotros peninsular. Conjugación verbal correspondiente: ustedes hacen, ustedes pueden, ustedes verán.
- **Imperativos en forma de usted/ustedes** para instrucciones operativas: "verifiquen", "auditen", "consideren". Cuando el registro permite tú, conjuga así: "verifica", "audita", "considera". Nunca "verificad", "auditad".
- **Pretérito perfecto simple sobre el compuesto** en la mayoría de casos. México usa "OpenAI anunció" más que "OpenAI ha anunciado"; "Anthropic publicó" más que "Anthropic ha publicado". El compuesto se reserva para acciones cuyo efecto continúa muy claramente en el presente.

### Léxico mexicano vs peninsular

Reemplazos sistemáticos cuando el correo fuente o el borrador inicial usen el término peninsular:

- **computadora** (no ordenador)
- **carro / coche** (depende del contexto; ambos funcionan en MX, evita "auto" en contextos formales)
- **video** (sin acento; no vídeo)
- **app / aplicación** (no "app móvil" salvo necesidad)
- **celular** (no móvil) para teléfono
- **suscripción** (no subscripción)
- **manejar** (no conducir) en contextos coloquiales; "operar", "gestionar" en contextos profesionales
- **departamento** (no piso) cuando se refiere a vivienda
- **plomero, electricista** (no fontanero salvo cita textual)
- **botón, contraseña, pantalla** (estos son neutros y aplican igual)
- **plata / dinero / capital / financiamiento** según contexto. Usa **financiamiento** (no financiación) en notas económicas.
- **estadounidense** (no norteamericano salvo cuando se quiera incluir México y Canadá) cuando se refiere específicamente a EE. UU.

### Comillas y signos

- Usa **comillas latinas redondeadas tipográficas** “como estas” para citas y términos destacados, no comillas rectas "como estas".
- Conserva los **signos de apertura** de interrogación (¿) y exclamación (¡). No los omitas como hace el inglés.
- Comillas anidadas: usa simples para la cita interna (“dijo: ‘no’”).

### Decimales y moneda

- **Punto decimal**, no coma: 77.8% (no 77,8%). **Coma para miles**: 122,000 millones (no 122.000). Es la convención estadounidense que usa el español mexicano moderno y la que el lector hispanohablante en México y Latinoamérica reconoce de inmediato.
- **Dólares estadounidenses**: "$122,000 millones USD" o "122,000 millones de dólares" o "USD 122,000 millones". Evita "dolares" sin tilde.
- **Pesos**: usa "MXN" si necesitas distinguir entre pesos mexicanos y otros pesos latinoamericanos; en notas dirigidas a audiencia mexicana, "pesos" sin sufijo es suficiente.
- **Porcentajes**: pegados al número sin espacio: 30%, 77.8%.

### Fechas

- Formato **dd de mes de aaaa** en texto corrido: "11 de abril de 2026". Para el masthead y nombre de archivo se mantiene el formato establecido ("11 de abril de 2026" en masthead; "2026.04.11" en nombre de archivo).
- Meses **siempre en minúscula** (abril, no Abril).
- Para horas usa formato 24 hr en contextos profesionales ("19:30"), 12 hr coloquial con "a.m./p.m." en minúsculas para textos casuales.

### Voseos, calcos y giros a evitar

- **No usar voseo argentino**: "vos podés" → "tú puedes" o "usted puede".
- **No usar "flipar", "molar", "currárselo", "ostras", "jó", "vale"** ni otros peninsularismos cotidianos.
- **No usar "chamba" en títulos formales** (es coloquial mexicano); sí válido en cuerpo informal.
- **"Ahora" y "ahorita"**: "ahora" para textos formales; "ahorita" solo en cuerpo conversacional.
- **Anglicismos**: conserva "benchmark", "prompt", "agente", "workflow", "deepfake" cuando no haya equivalente preciso en español (son técnicos consolidados). Evita anglicismos innecesarios: "reportar" en lugar de "reportear", "correo" en lugar de "mail", "contraseña" en lugar de "password".

### Glosario express de adaptaciones frecuentes

Cuando el borrador inicial salga con tono peninsular (porque el newsletter fuente es de España), aplica estos reemplazos antes de entregar el HTML:

- "vosotros" → "ustedes"
- "¿Qué tenéis que hacer?" → "¿Qué tienen que hacer?"
- "el ordenador" → "la computadora"
- "el móvil" → "el celular"
- "la fontanería" → "la plomería"
- "coger" en sentido de "tomar" → sustituir por **tomar / agarrar / recoger** ("coger" tiene carga sexual en México; nunca dejarlo)
- "el piso" (vivienda) → "el departamento"
- "el mínimo de financiación" → "el mínimo de financiamiento"
- "acabamos de hacer" (uso peninsular del compuesto) → "acabamos de hacer" se conserva porque el "acabar de + infinitivo" funciona igual en MX; pero "hemos lanzado" → "lanzamos".

### Excepción: el footer y constantes de marca

El masthead ("IA Expo Internacional • Noticias"), el CTA ("Únete a la comunidad IA Expo"), el footer ("Publicado por IA Expo Internacional") y todas las constantes de marca quedan **sin cambios** sin importar la variedad del correo fuente. Son texto fijo del template, no editable.

## Imágenes del correo fuente (paso 4 del workflow)

Si el correo fuente contiene imágenes editoriales con URLs absolutas (http/https), inclúyelas en el artículo. **No las embebas como base64**, no las recrees, y no inventes URLs: usa solo las que vienen literalmente en el cuerpo del correo.

### Qué cuenta como "imagen editorial"

Incluye:
- Foto o gráfico que ilustra el hecho noticioso (ej. foto del producto recién lanzado, retrato del protagonista, captura del producto en acción, infografía con datos).
- Imagen marcada con leyenda o crédito de fuente en el correo (ej. "Fuente: Wikimedia Commons", "Foto: Rawpixel").
- Captura de pantalla relevante (UI de la herramienta, demo, screenshot del producto).

Excluye (estos son ruido del cliente de correo, no contenido editorial):
- Logos del newsletter o de la plataforma (Substack, LinkedIn, Mailchimp).
- Botones de UI: "Leer en la app", "Suscríbete", "Compartir", "Me gusta", "Comentario", "Restack".
- Avatares pequeños del autor (img de <40px).
- Tracking pixels (img de 1x1).
- Iconos sociales (X, Facebook, Instagram, LinkedIn).
- Imágenes promocionales de patrocinadores (Surfshark VPN, anuncios embebidos).
- Imágenes con URLs relativas o `cid:` (no resuelven fuera del correo).

Si tienes duda sobre una imagen, omitirla es la decisión segura.

### Dónde insertarlas

Inserta las imágenes después del cuerpo (dropcap) o del pull quote, ANTES de la primera sección con kicker ("Reacciones", "Frentes de automatización", etc.).

Si hay más de una , agápelas como una sola fila con dos imágenes lado a lado (max 2 por fila) . Si hay más de cuatro imágenes editoriales en el correo, elige las dos más relevantes y omite el resto.

Usa este `<tr>` después del pull quote (o después del cuerpo si no hay pull quote):

```html
<!-- IMAGEN DEL CORREO FUENTE (una sola) -->
<tr>
    <td style="padding:16px 40px 8px 40px;">
      <img src="{{URL_IMAGEN}}" alt="{{ALT_TEXT_DESCRIPTIVO}}" style="display:block; width:100%; max-width:640px; height:auto; border-radius:8px; margin:0 auto;">
      <p style="margin:8px 0 0; font-size:12px; color:#64748b; text-align:center; font-style:italic;">{{LEYENDA_OPCIONAL}}</p>
    </td>
  </tr>
**Posición por defecto (confirmada por el usuario el 20 de mayo de 2026):** inserta la imagen editorial del correo fuente DENTRO del mismo `<td>` del bloque Header (kicker + headline + dech), JUSTO ANTES del párrafo de byline ("Por la redacción de IA Expo Internacional"). Razonamiento: el lector ve la imagen sin desplazarse y el byline queda anclado a la imagen, no al headline aislado. Esta es la posición canónica salvo que el usuario indique lo contrario para un artículo específico.

Si hay más de una imagen, agrúpalas como una sola fila con dos imágenes lado a lado (max 2 por fila) en esa misma ubicación. Si hay más de cuatro imágenes editoriales en el correo, elige las dos más relevantes y omite el resto.

Usa este bloque embebido dentro del `<td>` del Header, entre el `<p>` del dech y el `<p>` del byline:

```html
<!-- IMAGEN DEL CORREO FUENTE (una sola, dentro del <td> del Header, antes del byline) -->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:24px;">
  <tr>
    <td style="padding:0;">
      <img src="{{URL_IMAGEN}}" alt="{{ALT_TEXT_DESCRIPTIVO}}" style="display:block; width:100%; max-width:640px; height:auto; border-radius:8px; margin:0 auto;">
      <p style="margin:8px 0 0; font-size:12px; color:#64748b; text-align:center; font-style:italic;">{{LEYENDA_OPCIONAL}}</p>
    </td>
  </tr>
</table>
```

Para dos imágenes lado a lado:

```html
<!-- DOS IMAGENES DEL CORREO FUENTE -->
<tr>
  <td style="padding:16px 40px 8px 40px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td width="50%" style="padding-right:8px; vertical-align:top;">
          <img src="{{URL_IMAGEN_1}}" alt="{{ALT_1}}" style="display:block; width:100%; height:auto; border-radius:8px;">
          <p style="margin:6px 0 0; font-size:11px; color:#64748b; text-align:center; font-style:italic;">{{LEYENDA_1}}</p>
        </td>
        <td width="50%" style="padding-left:8px; vertical-align:top;">
          <img src="{{URL_IMAGEN_2}}" alt="{{ALT_2}}" style="display:block; width:100%; height:auto; border-radius:8px;">
          <p style="margin:6px 0 0; font-size:11px; color:#64748b; text-align:center; font-style:italic;">{{LEYENDA_2}}</p>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

### Leyenda y atribución

- Si el correo fuente da crédito a una fuente externa ("Fuente: Wikimedia Commons", "Foto: PxHere.com"), respeta esa atribución en `{{LEYENDA_OPCIONAL}}`. Conserva el crédito original.
- Si el correo fuente describe lo que es la imagen (ej. "Robot de reparto de Coco Robotics"), úsalo como leyenda.
- Si no hay leyenda, usa el alt text como descripción mínima en italic.
- `alt` text siempre debe ser descriptivo (lo que muestra la imagen), no decorativo ("image", "foto").

### Si no hay imágenes editoriales

Omite el bloque entero. No insertes placeholders, no recurras a stock photos, no generes nada. El artículo funciona sin imágenes adicionales — el banner hero ya cumple esa función.

## Nombrado del bloque de código (paso 6 del workflow)

El bloque de código debe ir precedido de una línea con el nombre de archivo en formato:

`yyyy.mm.dd <fuente>.html`

Donde:

- **`yyyy.mm.dd`** = fecha del correo fuente (`Date` en `<user_context>`), convertida a la zona de despliegue del usuario (America/Mexico_City por defecto). Usa puntos como separador, no guiones. Ejemplos: `2026.05.21`, `2026.11.03`.
- **`<fuente>`** = nombre amigable de la publicación derivado del display name del campo `From`. Conserva mayúsculas/minúsculas y espacios; quita sufijos técnicos como "News", "Newsletter", "Daily", direcciones de correo, o emojis si distorsionan el nombre. Ejemplos de mapeo:
  - `From: LinkedIn News <editors-noreply@linkedin.com>` → `LinkedIn News`
  - `From: IA Para Todos <hola@iaparatodos.mx>` → `IA Para Todos`
  - `From: The Rundown AI <news@therundown.ai>` → `The Rundown AI`
  - `From: Fortune Daily <newsletters@fortune.com>` → `Fortune`
- **`.html`** — extensión fija.

Ejemplo completo: `2026.05.21 IA Para Todos.html`

Formato en chat — nombre del archivo en negritas inmediatamente antes del bloque, en su propia línea:

```
**2026.05.21 IA Para Todos.html**

` ``html
<table role="presentation" ...>
  ...
</table>
` ``
```

Esto permite al usuario hacer Ctrl+A dentro del bloque, copiar, y guardar manualmente como ese archivo en su Desktop o pegar directo en GoHighLevel.

## Notas de decisiones editoriales (obligatorias después del HTML)

Después del bloque HTML, **siempre** incluye una sección titulada exactamente **“Notas de decisiones editoriales:”** con el detrás-de-cámara de las decisiones que tomaste. Es lo que permite al usuario auditar el criterio editorial, replicarlo manualmente, o pedir ajustes con precisión. No es opcional ni "solo si hubo decisiones complicadas": va en cada entrega.

### Formato

- Título en negritas seguido de dos puntos: **Notas de decisiones editoriales:**
- Lista de párrafos cortos (no bullets de markdown). Cada párrafo arranca con la categoría en negritas seguida de dos puntos, y luego la explicación en prosa de una a tres oraciones.
- Tono periodista que documenta su propio trabajo: directo, específico, sin disculpas. Cita fechas, números y atribuciones verbatim cuando aplique.
- Largo total: aproximadamente 200–350 palabras. No infles. Si una categoría no aplica al artículo, omítela; no escribas "no aplica".

### Categorías a cubrir (en este orden cuando apliquen)

1. **Nombre del archivo:** confirma el nombre exacto (`yyyy.mm.dd <Fuente>.html`) y nota la conversión de zona horaria si el correo llegó cerca de medianoche UTC (p. ej. "Fecha local 10 de abril en Mexico_City, el correo llegó a las 00:33 del 10").
2. **Pull quote:** explica qué frase elegiste y por qué. Si es cita textual de una fuente externa, nómbrala; si es la tesis del propio boletín condensada, di que la atribuiste al boletín y por qué esa frase captura el ángulo en una línea memorable. Si omitiste el pull quote, explica por qué.
3. **Estructura escalonada:** describe los bloques que armaste (cuerpo + secciones con kicker propio + análisis), nombrando los ejemplos canónicos o datos que se reproducen verbatim. Si reorganizaste el orden del newsletter fuente, di qué moviste y por qué.
4. **Datos verificables y atribuibles:** lista los nombres propios, papers, cifras y citas que se conservan literalmente del correo fuente, y a quién se atribuyen. Si dejaste un cálculo explícito para que el lector lo verifique, dilo ("el cálculo de Oliver 190 correcto, 185 falso lo dejé explícito en el cuerpo").
5. **Cross-references:** enumera las conexiones editoriales a notas previas que hayas trazado. Incluye fecha, fuente y tópico ("paper de Anthropic + Redwood del 23 de marzo sobre reward hacking + alignment faking"). Si cierras una tetralogía, una serie o una línea editorial recurrente de IA Expo, declálo aquí. **Importante:** solo cita cross-references que sepas que existen en la cobertura previa de IA Expo o que el usuario haya mencionado; no inventes notas previas. Si no tienes contexto de cobertura previa, omite esta categoría o di explícitamente "sin cross-references porque no tengo contexto de cobertura previa".
6. **Análisis con conversaciones operativas accionables:** describe los segmentos profesionales a los que apuntó el bloque de análisis y la acción concreta que cada uno puede ejecutar en las próximas 24–72 horas ("CFOs: auditoría rápida con datos irrelevantes; docentes universitarios: plantilla didáctica directa; directores de producto: tests adversariales como parte de QA"). Si solo cubriste un segmento, explica por qué.
7. **Tono editorial:** describe el registro original del newsletter (irónico, casual, alarmista, técnico) y cómo lo modulaste hacia el registro periodístico-analítico de IA Expo. Nombra pasajes concretos si reescribiste algo cargado.
8. **Imágenes del correo fuente:** declara explícitamente si el correo traía imágenes editoriales (con URL absoluta) y cuáles incluiste o por qué las omitiste. Si el correo es texto puro, di "sin imágenes del correo fuente: el correo es texto puro". Si excluiste logos, botones de UI o avatares pequeños, menciónalo.
9. **Omisiones intencionales:** menciona qué secciones del correo no llevaste al artículo (FAQ, encuesta de "qué cubrimos la próxima semana", footer promocional, anuncios de patrocinadores, llamadas a suscripción del newsletter fuente). El objetivo es que el usuario sepa exactamente qué quedó fuera.

### Ejemplo de bloque cerrado (referencia de tono y forma)

```
**Notas de decisiones editoriales:**

**Nombre del archivo:** 2026.04.10 IA Para Todos.html. Fecha local 10 de abril en Mexico_City (correo a las 00:33 del 10).

**Pull quote:** la frase pivote del newsletter sobre cómo el modelo "parece razonar cuando imita patrones estadísticos y en cuanto introduces algo que rompe el patrón, se cae sin avisar". Atribuida al boletín porque captura la tesis en una línea memorable.

**Estructura escalonada:** cuerpo con el ejemplo de Oliver y los kiwis (44 + 58 + 88 = 190, no 185), cuatro pasos metodológicos, sección "por qué las matemáticas", plantilla lista para usar (Laura y los lápices), sección sobre confianza percibida vs precisión real.

**Datos verificables y atribuibles:** experimento atribuido a Apple, paper como fuente original, los dos ejemplos canónicos (Oliver / Laura) reproducidos textualmente. El cálculo de Oliver (190 correcto, 185 falso) lo dejé explícito en el cuerpo.

**Cross-references:** paper de Anthropic + Redwood del 23 de marzo (reward hacking + alignment faking), ARC-AGI-3 del 27 de marzo (100% humanos vs <1% IA), paper de Stanford del 3 de abril (sesgo de complacencia), reportaje de FuturIA del 8 de abril sobre chatbots educativos. Esto cierra una tetralogía editorial sobre los límites del razonamiento.

**Análisis con conversaciones operativas accionables:** CFOs y equipos de finanzas (auditoría rápida con datos irrelevantes), docentes universitarios y de educación media (plantilla didáctica directa), directores de producto (tests adversariales como parte de QA).

**Tono editorial:** el newsletter original tiene tono irónico moderado ("eso ya deberías saberlo"). Modulé pasajes hacia registro periodístico-analítico conservando los ejemplos canónicos y la tesis técnica.

**Imágenes del correo fuente:** sin imágenes del correo fuente: el correo es texto puro.

**Omisiones intencionales:** omití el FAQ y el footer promocional del boletín.
```

## Recordatorio sobre imágenes editoriales

La sección "Imágenes del correo fuente (paso 4 del workflow)" ya define qué cuenta como imagen editorial y cómo insertarla. Reafírmalo: **cuando el correo fuente contenga fotos, gráficos, capturas de pantalla o infografías con URLs absolutas, incluirlas en el HTML es el comportamiento por defecto, no una opción.** Solo omites cuando el correo es texto puro, cuando las imágenes son ruido del cliente (logos de Substack, botones de UI, avatares <40px, tracking pixels, iconos sociales, patrocinadores), o cuando las URLs son relativas / `cid:` y no resuelven fuera del correo. Reporta la decisión en la nota editorial **Imágenes del correo fuente**.

## Output

Devuelve el HTML en un bloque de código markdown (` ```html `) precedido del nombre de archivo en negritas (ver "Nombrado del bloque de código" arriba), y debajo el bloque **Notas de decisiones editoriales:** con el formato descrito arriba. Sin preámbulo largo. Una línea breve arriba del nombre del archivo ("Listo, aquí está el artículo para [tema]:") y al final ofrece personalización (subject line, preheader, variación más corta) si el usuario lo pide. **No** presentes tarjeta de correo, **no** llames a `present_draft_email`.

Si detectas que el correo no contiene una noticia procesable (es promocional, transaccional, o muy delgado en contenido), dilo en chat y propón qué información hace falta antes de generar el HTML.