const express = require("express");
const { Board, Servo } = require("johnny-five");

const board = new Board();
const app = express();
const puerto = 3000;

// Variables para los servos
let servo_base, servo_hombro, servo_muneca, servo_garra;

// Inicializar la placa y los servos
board.on("ready", () => {
  console.log("Board ready");

  // Configuración detallada de los servos
  servo_base = new Servo({
    pin: 8,
    range: [0, 180],
    startAt: 90,
  });

  servo_hombro = new Servo({
    pin: 9,
    range: [0, 180],
    startAt: 180,
  });

  servo_muneca = new Servo({
    pin: 10,
    range: [0, 180],
    startAt: 180,
  });

  servo_garra = new Servo({
    pin: 11,
    range: [0, 180],
    startAt: 10,
  });

  console.log("Servos configurados correctamente");
});

// Ruta para recibir los ángulos desde el cliente (Python)
app.get("/:angles", (req, res) => {
  const { angles } = req.params;

  // Dividir los ángulos enviados (formato: 90-120-180)
  const [angle_base, angle_hombro, angle_muneca, angle_garra] = angles
    .split("-")
    .map(Number);

  // Validar si los servos están listos
  if (!servo_base || !servo_hombro || !servo_muneca || !servo_garra) {
    return res.status(500).send("Servos no están listos");
  }

  // Validar los ángulos
  if (
    isNaN(angle_base) ||
    isNaN(angle_hombro) ||
    isNaN(angle_muneca) ||
    angle_base < 0 ||
    angle_base > 180 ||
    angle_hombro < 0 ||
    angle_hombro > 180 ||
    angle_muneca < 0 ||
    angle_muneca > 180
  ) {
    return res
      .status(400)
      .send("Ángulos inválidos. Deben estar entre 0 y 180.");
  }

  // Mover los servos
  servo_base.to(angle_base);
  servo_hombro.to(angle_hombro);
  servo_muneca.to(angle_muneca);
  servo_garra.to(angle_garra);

  console.log(
    `Ángulos recibidos: Base=${angle_base}, Hombro=${angle_hombro}, Muñeca=${angle_muneca}, Garra=${angle_garra}`
  );
  res.send(
    `Ángulos aplicados: Base=${angle_base}, Hombro=${angle_hombro}, Muñeca=${angle_muneca}, Garra=${angle_garra}`
  );
});

// Iniciar el servidor
app.listen(puerto, () => {
  console.log(`Servidor escuchando en el puerto ${puerto}`);
});

app.get("/", (req, res) => {
  res.send("Hello World!");
});
