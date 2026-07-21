import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Snake en Streamlit", page_icon="🐍", layout="centered")

st.title("🐍 Juego Clásico de Snake")
st.write("¡Haz clic en el cuadro negro y usa las flechas de tu teclado para jugar!")

st.divider()

# Código HTML, CSS y JavaScript del juego inyectado
codigo_snake = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background-color: #ffe6eb; /* El fondo rosadito que ya te gusta */
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    #score-board {
      font-size: 24px;
      font-weight: bold;
      color: #2b2b2b;
      margin-bottom: 15px;
      margin-top: 10px;
    }
    canvas {
      background-color: #1e1e1e;
      border: 4px solid #333;
      border-radius: 10px;
      box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
    }
    .instrucciones {
      margin-top: 10px;
      color: #555;
      font-size: 14px;
    }
  </style>
</head>
<body>

  <div id="score-board">Puntuación: <span id="score">0</span></div>
  <canvas id="gameCanvas" width="400" height="400"></canvas>
  <div class="instrucciones">Presiona la barra espaciadora para reiniciar si pierdes.</div>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const box = 20; // Tamaño de cada cuadro
    let snake;
    let food;
    let score;
    let d;
    let game;

    // Función para iniciar o reiniciar el juego
    function initGame() {
        snake = [];
        snake[0] = { x: 10 * box, y: 10 * box };
        food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box
        };
        score = 0;
        d = null;
        document.getElementById("score").innerText = score;
        if(game) clearInterval(game);
        game = setInterval(draw, 120); // Velocidad del juego
    }

    // Escuchar el teclado
    document.addEventListener("keydown", direction);

    function direction(event) {
        let key = event.keyCode;
        if(key == 37 && d != "RIGHT") { d = "LEFT"; event.preventDefault(); }
        else if(key == 38 && d != "DOWN") { d = "UP"; event.preventDefault(); }
        else if(key == 39 && d != "LEFT") { d = "RIGHT"; event.preventDefault(); }
        else if(key == 40 && d != "UP") { d = "DOWN"; event.preventDefault(); }
        else if(key == 32) { initGame(); event.preventDefault(); } // Barra espaciadora para reiniciar
    }

    // Dibujar el juego
    function draw() {
        // Fondo del canvas
        ctx.fillStyle = "#1e1e1e";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Dibujar la serpiente
        for(let i = 0; i < snake.length; i++) {
            ctx.fillStyle = (i == 0) ? "#4CAF50" : "#81C784"; // Cabeza más oscura que el cuerpo
            ctx.fillRect(snake[i].x, snake[i].y, box, box);
            ctx.strokeStyle = "#1e1e1e";
            ctx.strokeRect(snake[i].x, snake[i].y, box, box);
        }

        // Dibujar la comida (manzana)
        ctx.fillStyle = "#E53935";
        ctx.fillRect(food.x, food.y, box, box);

        // Posición actual de la cabeza
        let snakeX = snake[0].x;
        let snakeY = snake[0].y;

        // Movimiento
        if(d == "LEFT") snakeX -= box;
        if(d == "UP") snakeY -= box;
        if(d == "RIGHT") snakeX += box;
        if(d == "DOWN") snakeY += box;

        // Comer la manzana
        if(snakeX == food.x && snakeY == food.y) {
            score++;
            document.getElementById("score").innerText = score;
            food = {
                x: Math.floor(Math.random() * 20) * box,
                y: Math.floor(Math.random() * 20) * box
            };
        } else {
            // Eliminar la cola si no comió
            snake.pop();
        }

        let newHead = { x: snakeX, y: snakeY };

        // Colisiones (Paredes o consigo misma)
        if(snakeX < 0 || snakeX >= canvas.width || snakeY < 0 || snakeY >= canvas.height || collision(newHead, snake)) {
            clearInterval(game);
            ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.font = "30px Arial";
            ctx.textAlign = "center";
            ctx.fillText("¡Fin del Juego!", canvas.width/2, canvas.height/2);
            ctx.font = "16px Arial";
            ctx.fillText("Presiona Espacio para reiniciar", canvas.width/2, canvas.height/2 + 30);
            return;
        }

        snake.unshift(newHead); // Añadir nueva cabeza
    }

    // Detección de colisión con su propio cuerpo
    function collision(head, array) {
        for(let i = 0; i < array.length; i++) {
            if(head.x == array[i].x && head.y == array[i].y) {
                return true;
            }
        }
        return false;
    }

    // Iniciar al cargar
    initGame();
  </script>
</body>
</html>
"""

# Incrustar el código HTML en Streamlit
components.html(codigo_snake, height=550)

st.divider()
st.write("💡 **Tip:** Si estás desde el celular, lamentablemente las flechas del teclado no aparecerán. ¡Este minijuego está optimizado para computadoras!")
