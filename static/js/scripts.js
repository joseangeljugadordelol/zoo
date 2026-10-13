const form = document.getElementById('form-animal');
const tabla = document.getElementById('tabla-animales');
const mensaje = document.getElementById('mensaje');
const btnGuardar = document.getElementById('btn-guardar');

function mostrarMensaje(texto, tipo) {
  mensaje.textContent = texto;
  mensaje.className = tipo;
}

function pintarAnimales(animales) {
  tabla.innerHTML = '';

  if (animales.length === 0) {
    const fila = document.createElement('tr');
    const celda = document.createElement('td');
    celda.colSpan = 3;
    celda.className = 'vacio';
    celda.textContent = 'Aún no hay animales. Guarda el primero con el formulario.';
    fila.appendChild(celda);
    tabla.appendChild(fila);
    return;
  }

  animales.forEach((animal) => {
    const fila = document.createElement('tr');
    [animal.nombre, animal.raza, animal.comida].forEach((valor) => {
      const celda = document.createElement('td');
      celda.textContent = valor;
      fila.appendChild(celda);
    });
    tabla.appendChild(fila);
  });
}

async function cargarAnimales() {
  try {
    const respuesta = await fetch('/animales');
    if (!respuesta.ok) throw new Error();
    pintarAnimales(await respuesta.json());
  } catch (e) {
    mostrarMensaje('No se pudo cargar la lista. Revisa que MySQL esté corriendo.', 'error');
  }
}

form.addEventListener('submit', async (evento) => {
  evento.preventDefault();

  const animal = {
    nombre: document.getElementById('nombre').value.trim(),
    raza: document.getElementById('raza').value.trim(),
    comida: document.getElementById('comida').value.trim(),
  };

  btnGuardar.disabled = true;
  try {
    const respuesta = await fetch('/animales', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(animal),
    });
    const datos = await respuesta.json();

    if (!respuesta.ok) {
      mostrarMensaje(datos.error || 'No se pudo guardar el animal.', 'error');
      return;
    }

    mostrarMensaje(`Animal guardado: ${datos.nombre}.`, 'ok');
    form.reset();
    document.getElementById('nombre').focus();
    cargarAnimales();
  } catch (e) {
    mostrarMensaje('No se pudo conectar con el servidor.', 'error');
  } finally {
    btnGuardar.disabled = false;
  }
});

cargarAnimales();