CREATE TABLE IF NOT EXISTS animal (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(45) NOT NULL,
  raza VARCHAR(45) NOT NULL,
  comida VARCHAR(45) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO animal (nombre, raza, comida) VALUES
('leon', 'felino', 'carne'),
('perro', 'canino', 'croquetas'),
('gato', 'felino', 'pescado'),
('loro', 'ave', 'semillas'),
('tigre', 'felino', 'carne'),
('cocodrilo', 'reptil', 'carne');