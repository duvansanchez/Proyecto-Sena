let currentWeekStartDate; // Variable para controlar la semana actual en el calendario

function cargarEspecialidades() {
  const especialidadSelect = document.getElementById("especialidad");
  especialidadSelect.innerHTML =
    '<option value="">Seleccione Especialidad</option>';
  especialidades.forEach((especialidad) => {
    const option = document.createElement("option");
    option.value = especialidad;
    option.textContent = especialidad;
    especialidadSelect.appendChild(option);
  });
}

function cargarMedicosPorEspecialidad(especialidadSeleccionada) {
  const medicoSelect = document.getElementById("medico");
  medicoSelect.innerHTML = '<option value="">Seleccione un Médico</option>';
  if (especialidadSeleccionada) {
    const medicosFiltrados = medicos.filter(
      (medico) => medico.especialidad === especialidadSeleccionada
    );
    medicosFiltrados.forEach((medico) => {
      const option = document.createElement("option");
      option.value = medico.id;
      option.textContent = medico.id + " - " + medico.nombre;
      medicoSelect.appendChild(option);
    });
    medicoSelect.disabled = false;
  } else {
    medicoSelect.disabled = true;
  }
}

// Función para generar un rango de horas entre dos horas dadas
function generarHoras(inicio, fin) {
  const horas = [];
  let horaActual = new Date(`1970-01-01T${inicio}:00`);
  const horaFin = new Date(`1970-01-01T${fin}:00`);

  while (horaActual < horaFin) {
    horas.push(horaActual.toTimeString().substring(0, 5));
    horaActual.setMinutes(horaActual.getMinutes() + 60); // Incremento de 1 hora
  }
  return horas;
}

// Función para obtener las fechas de la semana a partir de una fecha dada (Lunes a Domingo)
function obtenerSemana(fechaReferencia) {
  const fecha = new Date(fechaReferencia);
  const diaSemana = fecha.getDay(); // 0 (Domingo) - 6 (Sábado)
  const fechaInicio = new Date(fecha);
  fechaInicio.setDate(fecha.getDate() - diaSemana + (diaSemana === 0 ? -6 : 1)); // Ajustar si es Domingo
  const semana = [];

  for (let i = 0; i < 7; i++) {
    const fechaDia = new Date(fechaInicio);
    fechaDia.setDate(fechaInicio.getDate() + i);
    semana.push(fechaDia);
  }
  return semana;
}

// Función para mostrar el calendario del médico seleccionado
function mostrarCalendarioMedico(medicoCedula, fechaInicioSemana = new Date()) {
  const medico = medicos.find((m) => m.id == medicoCedula);
  if (medico) {
    const horarioContainer = document.getElementById("horarioMedicoContainer");
    const horarioMedico = document.getElementById("horarioMedico");
    horarioMedico.innerHTML = "";

    currentWeekStartDate = new Date(fechaInicioSemana);

    const semana = obtenerSemana(currentWeekStartDate);
    const diasSemana = [
      "Domingo",
      "Lunes",
      "Martes",
      "Miércoles",
      "Jueves",
      "Viernes",
      "Sábado",
    ];

    // Actualizar etiqueta de la semana actual
    const currentWeekLabel = document.getElementById("currentWeekLabel");
    const fechaInicioLabel = semana[0].toLocaleDateString();
    const fechaFinLabel = semana[6].toLocaleDateString();
    currentWeekLabel.textContent = `Semana del ${fechaInicioLabel} al ${fechaFinLabel}`;

    // Crear encabezados de días
    const headers = document.createElement("div");
    headers.className = "calendar-grid";
    semana.forEach((fechaDia) => {
      const headerCell = document.createElement("div");
      headerCell.className = "day-header";
      headerCell.textContent =
        diasSemana[fechaDia.getDay()] +
        " " +
        fechaDia.getDate() +
        "/" +
        (fechaDia.getMonth() + 1);
      headers.appendChild(headerCell);
    });
    horarioMedico.appendChild(headers);

    // Generar las horas de trabajo del médico durante la semana, horasTrabajo variable que contiene las horas en las que va a trabajar el medico
    const horasTrabajo = {};
    medico.horarios.forEach((horario) => {
      const indiceDia = diasSemana.indexOf(horario.dia);
      if (indiceDia !== -1) {
        const horas = generarHoras(horario.inicio, horario.fin);
        horasTrabajo[indiceDia] = horas;
      }
    });

    const horasDelDia = generarHoras("00:00", "23:00");

    // Crear las celdas del calendario
    horasDelDia.forEach((hora) => {
      const row = document.createElement("div");
      row.className = "calendar-grid";

      for (let i = 0; i < 7; i++) {
        const cell = document.createElement("div");
        cell.className = "calendar-cell";

        const diaSemana = semana[i];
        const fechaString = diaSemana.toISOString().split("T")[0]; //2024-11-06

        const horasDelDia = horasTrabajo[diaSemana.getDay()] || [];

        // Comparamos solo la hora sin minutos en el formato "HH:"
        const horaSinMinutos = hora.substring(0, 2) + ":";
        const horaDisponible = horasDelDia.some((horario) =>
          horario.startsWith(horaSinMinutos)
        );
        const citaOcupada = medico.citas.some((cita) => {
          const citaFecha = cita.fecha.split(" ")[0]; // Extrae solo la fecha sin la hora
          return citaFecha === fechaString && cita.hora === hora;
        });

        if (!horaDisponible) {
          cell.textContent = "Horario no asignado";
          cell.classList.add("disabled");
        }
        if (citaOcupada) {
          cell.classList.add("disabled");
          cell.textContent = "Ocupado";
        }
        if (horaDisponible && !citaOcupada) {
          cell.textContent = hora;
          cell.addEventListener("click", () => {
            seleccionarHora(fechaString, hora, cell);
          });
        }

        if (!horaDisponible && !citaOcupada) {
          cell.textContent = "";
          cell.classList.add("disabled");
        }

        row.appendChild(cell);
      }
      horarioMedico.appendChild(row);
    });

    horarioContainer.style.display = "block";
    document.getElementById("nombre_medico").value =
      medico.id + " - " + medico.nombre;
  } else {
    alert("No se encontró el médico seleccionado.");
    document.getElementById("horarioMedicoContainer").style.display = "none";
    document.getElementById("nombre_medico").value = "";
    return;
  }
}

// Función para manejar la selección de una hora
function seleccionarHora(fecha, hora, cell) {
  // Limpiar selección previa
  document
    .querySelectorAll(".calendar-cell.selected")
    .forEach((c) => c.classList.remove("selected"));
  // Marcar la celda seleccionada
  cell.classList.add("selected");
  // Actualizar campos del formulario
  document.getElementById("fecha").value = fecha;
  document.getElementById("hora_llegada").value = hora;
}

// Función para cambiar de semana en el calendario
function cambiarSemana(direccion) {
  const diasCambio = direccion === "next" ? 7 : -7;
  currentWeekStartDate.setDate(currentWeekStartDate.getDate() + diasCambio);
  const medicoId = document.getElementById("medico").value;
  if (medicoId) {
    mostrarCalendarioMedico(medicoId, currentWeekStartDate);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  cargarEspecialidades();

  document.getElementById("especialidad").addEventListener("change", (e) => {
    const especialidadSeleccionada = e.target.value;
    cargarMedicosPorEspecialidad(especialidadSeleccionada);
    document.getElementById("medico").value = "";
    document.getElementById("medico").disabled = !especialidadSeleccionada;
    // Ocultar calendario y limpiar nombre del médico
    document.getElementById("horarioMedicoContainer").style.display = "none";
    document.getElementById("nombre_medico").value = "";
  });

  document.getElementById("medico").addEventListener("change", (e) => {
    currentWeekStartDate = new Date(); // Reiniciar a la semana actual
    const medicoCedula = e.target.value;
    if (medicoCedula) {
      mostrarCalendarioMedico(medicoCedula, currentWeekStartDate);
    } else {
      // Ocultar calendario y limpiar nombre del médico
      document.getElementById("horarioMedicoContainer").style.display = "none";
      document.getElementById("nombre_medico").value = "";
    }
  });

  document.getElementById("prevWeekBtn").addEventListener("click", () => {
    cambiarSemana("prev");
  });

  document.getElementById("nextWeekBtn").addEventListener("click", () => {
    cambiarSemana("next");
  });

  document.getElementById("crear_cita").addEventListener("click", (e) => {
    const fecha = document.getElementById("fecha").value;
    const hora = document.getElementById("hora_llegada").value;

    if (!fecha || !hora) {
      alert("Por favor, seleccione una fecha y hora en el calendario.");
      e.preventDefault();
      return;
    }

    document.getElementById("formularioCita").submit();
  });

  // Llamar a la función cuando la página se cargue, por si el campo ya tiene un valor predefinido
  document
    .getElementById("nombre_paciente")
    .addEventListener("input", habilitarCampos);

  function habilitarCampos() {
    const nombrePaciente = document.getElementById("nombre_paciente").value;
    const especialidad = document.getElementById("especialidad");
    const medico = document.getElementById("medico");

    // Si el campo de nombre de paciente no está vacío, habilita los selects
    if (nombrePaciente.trim() !== "") {
      especialidad.disabled = false;
      medico.disabled = false;
    } else {
      especialidad.disabled = true;
      medico.disabled = true;
    }
  }
  habilitarCampos();
});
