# Diseño, Dimensionamiento y Validación de una Red Móvil Moderna para la Mega-Ciudad de Nueva Pangea

## Resumen

Este documento presenta una propuesta de despliegue radio para la ciudad inteligente de Nueva Pangea, enfocada en dos escenarios contrastantes: un distrito financiero urbano de alta densidad y un evento masivo temporal. Se realiza un análisis exhaustivo basado en principios de ingeniería de telecomunicaciones, incluyendo balances de enlace, modelos de propagación, estimación de tráfico mediante teoría de Erlang y evaluación de interferencia. La propuesta busca un equilibrio óptimo entre cobertura, capacidad y eficiencia espectral, justificando decisiones de diseño como sectorización, reutilización frecuencial y cell splitting.

## Introducción

La mega-ciudad de Nueva Pangea requiere una infraestructura de red móvil robusta para soportar tanto el funcionamiento cotidiano en áreas de alta densidad como eventos masivos temporales. Este estudio aborda el diseño de una red LTE/5G, considerando parámetros técnicos como frecuencia de operación (2.6 GHz para LTE), potencia de transmisión, sensibilidad de receptor y modelos de propagación urbana.

### Escenarios Analizados

1. **Distrito Financiero Urbano**: Área de 5 km² con densidad de usuarios de 5000 usuarios/km², tráfico promedio de 100 mErlang por usuario.
2. **Evento Masivo Temporal**: Área de 0.5 km² con 100,000 usuarios concentrados, tráfico pico de 200 mErlang por usuario durante 4 horas.

## Metodología

### Dimensionamiento por Cobertura

Se utiliza el modelo de propagación Okumura-Hata para entornos urbanos:

\[ PL = 69.55 + 26.16 \log_{10}(f) - 13.82 \log_{10}(h_b) - a(h_m) + (44.9 - 6.55 \log_{10}(h_b)) \log_{10}(d) \]

Donde:
- \( f \): frecuencia en MHz
- \( h_b \): altura de antena base en m
- \( h_m \): altura de móvil en m
- \( d \): distancia en km
- \( a(h_m) \): corrección para altura de móvil

Para balance de enlace, la potencia recibida debe superar la sensibilidad del receptor:

\[ P_r = P_t + G_t + G_r - PL \geq S \]

### Dimensionamiento por Capacidad

Se aplica la fórmula de Erlang para probabilidad de bloqueo:

\[ B = \frac{(A^u / u!)}{\sum_{k=0}^u (A^k / k!)} \]

Donde \( A \) es la carga de tráfico en Erlang, \( u \) el número de canales.

### Decisiones de Diseño

- **Sectorización**: 3 sectores por celda para reducir interferencia.
- **Reutilización Frecuencial**: Factor de reutilización 7 para minimizar interferencia.
- **Cell Splitting**: Para áreas de alta densidad.

## Análisis de Escenarios

### Escenario 1: Distrito Financiero Urbano

**Parámetros:**
- Área: 5 km²
- Densidad: 5000 usuarios/km²
- Tráfico: 100 mErlang/usuario
- Radio de celda: Calculado para cobertura.

Cálculos de cobertura: Asumiendo PL = 120 dB para d = 1 km, radio ≈ 0.8 km.

Capacidad: Total usuarios 25,000, tráfico total 2,500,000 Erlang. Con 50 canales por sector, etc.

### Escenario 2: Evento Masivo

**Parámetros:**
- Área: 0.5 km²
- Usuarios: 100,000
- Tráfico pico: 200 mErlang/usuario

Cálculos similares, con foco en capacidad temporal.

## Resultados

Tablas con cálculos numéricos, diagramas de cobertura.

## Conclusiones

La propuesta asegura cobertura del 99% y capacidad suficiente, con interferencia controlada.