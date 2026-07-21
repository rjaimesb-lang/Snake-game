import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Snake Móvil", page_icon="🐍", layout="centered")

# Inyección de CSS para fondo azul oscuro, textura y contraste de letra blanca
estilo_fondo = """
<style>
.stApp {
    background-color: #0b192c; /* Color de fondo azul oscuro */
    background-image: radial-gradient(#1a365d 1.5px, transparent 1.5px); /* Textura de puntos */
    background-size: 25px 25px; /* Tamaño de la textura */
}
/* Forzar el color de la letra a claro para generar contraste */
h1, h2, h3, p, label, .stMarkdown {
    color: #f1f5f9 !important;
}
</style>
"""
st.markdown(estilo_fondo, unsafe_allow_html=True)

st.title("🐍 Juego de Snake")
st.write("¡Juega desde tu PC con el teclado o usa los botones táctiles en tu celular!")

st.divider()

# Código HTML, CSS y JavaScript del juego inyectado (con botones)
codigo_snake = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <style>
    body {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background-color: transparent;
      color: white;
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      touch-action: none; /* Previene que la pantalla baje al tocar los botones */
    }
    #score-board {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 15px;
      margin-top: 5px;
    }
    canvas {
      background-color: #112240; /* Azul un poco más claro para el tablero */
      border: 3px solid #64ffda; /* Borde verde neón/cian */
      border-radius: 8px;
      box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
    }
    /* Estilos para los controles móviles */
    .controles {
      display: grid;
      grid-template-columns: 60px 60px 60px;
      grid-template-rows: 60px 60px;
      gap: 10px;
      margin-top: 20px;
      justify-content: center;
    }
    .btn {
      background-color: #1d4ed8; /* Azul brillante para los botones */
      color: white;
      border-radius: 12px;
      font-size: 24px;
      display: flex;
      justify-content: center;
      align-items: center;
      user-select: none;
      cursor: pointer;
      box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .btn:active {
      background-color: #2563eb;
      transform: scale(0.95);
    }
    #btn-up { grid-column: 2; grid-row: 1; }
    #btn-left { grid-column: 1; grid-row: 2; }
    #btn-down { grid-column: 2; grid-row: 2; }
    #btn-right { grid-column: 3; grid-row: 2; }
  </style>
</head>
<body>

  <div id="score-board">Puntuación: <span id="score">0</span></div>
  <canvas id="gameCanvas" width="300" height="300"></canvas>
  
  <!-- D-Pad Virtual para móviles -->
  <div class="controles">
    <div class="btn" id="btn-up" onclick="setDirection('UP')">⬆️</div>
    <div class="btn" id="btn-left" onclick="setDirection('LEFT')">⬅️</div>
    <div class="btn" id="btn-down" onclick="setDirection('DOWN')">⬇️</div>
    <div class="btn" id="btn-right" onclick="setDirection('RIGHT')">➡️</div>
  </div>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const box = 15; // Ajustado para el nuevo tamaño del canvas
    let snake;
    let food;
    let score;
    let d;
    let game;

    function initGame() {
        snake = [];
        snake[0] = { x: 9 * box, y: 9 * box };
        food = {
            x: Math.floor(Math.random() * 19) * box,
            y: Math.floor(Math.random() * 19) * box
        };
        score = 0;
        d = null;
        document.getElementById("score").innerText = score;
        if(game) clearInterval(game);
        game = setInterval(draw, 130); // Velocidad
    }

    // Soporte para teclado en PC
    document.addEventListener("keydown", direction);
    function direction(event) {
        let key = event.keyCode;
        if(key == 37) setDirection('LEFT');
        else if(key == 38) setDirection('UP');
        else if(key == 39) setDirection('RIGHT');
        else if(key == 40) setDirection('DOWN');
        else if(key == 32) initGame();
        
        // Evita que las flechas muevan la página
        if([32, 37, 38, 39, 40].indexOf(key) > -1) {
            event.preventDefault();
        }
    }

    // Soporte para botones táctiles
    function setDirection(newD) {
        if(newD == "LEFT" && d != "RIGHT") d = "LEFT";
        else if(newD == "UP" && d != "DOWN") d = "UP";
        else if(newD == "RIGHT" && d != "LEFT") d = "RIGHT";
        else if(newD == "DOWN" && d != "UP") d = "DOWN";
        // Si el juego terminó, tocar cualquier botón reinicia
        else if(d == "GAME_OVER") initGame();
    }

    function draw() {
        ctx.fillStyle = "#112240";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for(let i = 0; i < snake.length; i++) {
            ctx.fillStyle = (i == 0) ? "#64ffda" : "#48bba3"; // Serpiente color cian
            ctx.fillRect(snake[i].x, snake[i].y, box, box);
            ctx.strokeStyle = "#112240";
            ctx.strokeRect(snake[i].x, snake[i].y, box, box);
        }

        ctx.fillStyle = "#ff4757"; // Comida roja vibrante
        ctx.fillRect(food.x, food.y, box, box);

        let snakeX = snake[0].x;
        let snakeY = snake[0].y;

        if(d == "LEFT") snakeX -= box;
        if(d == "UP") snakeY -= box;
        if(d == "RIGHT") snakeX += box;
        if(d == "DOWN") snakeY += box;

        if(snakeX == food.x && snakeY == food.y) {
            score++;
            document.getElementById("score").innerText = score;
            food = {
                x: Math.floor(Math.random() * 19) * box,
                y: Math.floor(Math.random() * 19) * box
            };
        } else {
            if(d) snake.pop(); // Solo elimina la cola si la serpiente se está moviendo
        }

        let newHead = { x: snakeX, y: snakeY };

        // Colisiones
        if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || (d && collision(newHead, snake))) {
            clearInterval(game);
            ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.font = "24px Arial";
            ctx.textAlign = "center";
            ctx.fillText("¡Perdiste!", canvas.width/2, canvas.height/2 - 10);
            ctx.font = "14px Arial";
            ctx.fillText("Toca una flecha para reiniciar", canvas.width/2, canvas.height/2 + 20);
            d = "GAME_OVER"; // Estado de fin de juego
            return;
        }

        if(d) snake.unshift(newHead);
    }

    function collision(head, array) {
        for(let i = 0; i < array.length; i++) {
            if(head.x == array[i].x && head.y == array[i].y) return true;
        }
        return false;
    }

    initGame();
  </script>
</body>
</html>
"""

# Hemos ampliado el 'height' a 650 para que entren perfectamente los botones del celular
components.html(codigo_snake, height=650)
