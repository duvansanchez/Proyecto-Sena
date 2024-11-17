let horarioMedicoElegido = "";

let inputHidden = document.querySelector(
  '#inputHiddenContainer input[name="horarios[]"]'
); // Input que contiene los horarios a validar e ingresar en la db

// Función para cargar las especialidades
function cargarEspecialidades() {
  const especialidadSeleccionada = document.getElementById("especialidad");
  especialidades.forEach((especialidad) => {
    const option = document.createElement("option");
    option.value = especialidad;
    option.textContent = especialidad;
    especialidadSeleccionada.appendChild(option);
  });
}

// Función para cargar los médicos según la especialidad
function cargarDoctores(especialidad) {
  const doctorSeleccionado = document.getElementById("doctor");
  doctorSeleccionado.innerHTML =
    '<option value="">Seleccione un Médico</option>';
  medicos
    .filter((d) => d.especialidad === especialidad)
    .forEach((doctor) => {
      const option = document.createElement("option");
      option.value = doctor.cedula;
      option.textContent = `${doctor.nombre} ${doctor.apellido}`;
      doctorSeleccionado.appendChild(option);
    });
}

// Función para generar la grilla de horarios
function generarHorarioGrilla() {
  const horarioGrilla = document.getElementById("horarioGrilla");
  horarioGrilla.innerHTML = "";
  const doctorCedula = document.getElementById("doctor").value;
  horarioMedicoElegido = horariosDoctores.filter(
    (h) => h.cedula == doctorCedula
  );

  // Crear encabezados de días
  const diasSemana = [
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
  ];
  diasSemana.forEach((dia) => {
    const diaTitulo = document.createElement("div");
    diaTitulo.className = "day-header";
    diaTitulo.textContent = dia;
    horarioGrilla.appendChild(diaTitulo);
  });

  //Cargar horarios en lista eliminable
  const horarioLista = document.getElementById("horarioLista");
  horarioLista.innerHTML = "";

  horarioMedicoElegido.forEach((horario) => {
    const horarioItem = document.createElement("div");
    horarioItem.className =
      "bg-gray-100 p-2 rounded flex justify-between items-center";
    horarioItem.innerHTML = `<span>${horario.dia}: ${horario.inicio} - ${horario.fin}</span>
    <button class="text-red-500 hover:text-red-700">Eliminar</button>`;

    const button = horarioItem.querySelector('button');

    button.addEventListener('click', () => {
    removerHorario(horario.dia, horario.inicio, horario.fin, button);
    });

    horarioLista.appendChild(horarioItem);
  });
  inputHidden.value = JSON.stringify(horarioMedicoElegido);

  //Crear celda de horario para cada respectivo dia
  diasSemana.forEach((dia) => {
    const cell = document.createElement("div");
    cell.className = "schedule-cell";

    //Validar si el doctor tiene un horario en ese dia
    const diasHorarios = horariosDoctores.filter(
      (s) => s.cedula == doctorCedula && s.dia === dia
    );
    if (diasHorarios.length > 0) {
      cell.innerHTML = diasHorarios
        .map((s) => `${s.inicio} - ${s.fin}`)
        .join("<br>");
    } else {
      cell.innerHTML =
        '<span class="no-disponible">No tiene horario asignado en este dia</span>';
    }

    horarioGrilla.appendChild(cell);
  });
}

function validarExistenciaHorario(horario) {
  const horarioLista = document.getElementById("horarioLista");
  const existe = Array.from(horarioLista.children).some((item) => {
    const textoHorario = item.querySelector("span").textContent;
    const [diaTexto, horasTexto] = textoHorario.split(": ");
    const [inicioTexto, finTexto] = horasTexto.split(" - ");
    return (
      diaTexto === horario.dia &&
      inicioTexto === horario.inicio &&
      finTexto === horario.fin
    );
  });
  return existe;
}

// Función para remover un horario de la lista
function removerHorario(dia, inicio, fin, button) {
  const doctorCedula = document.getElementById("doctor").value;

  // Remover el horario del array
  horariosDoctores = horariosDoctores.filter(
    (horario) =>
      !(
        horario.cedula == doctorCedula &&
        horario.dia === dia &&
        horario.inicio === inicio &&
        horario.fin === fin
      )
  );

  // Remover el elemento de la lista
  const horarioItem = button.parentElement;
  horarioItem.remove();

  // Actualizar la grilla de horarios
  generarHorarioGrilla();
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  cargarEspecialidades();

  document.getElementById("especialidad").addEventListener("change", (e) => {
    cargarDoctores(e.target.value);
    document.getElementById("horarioContenedor").classList.add("hidden");
  });

  //Una vez se haya seleccionado el medico a generar el horario
  document.getElementById("doctor").addEventListener("change", () => {
    //Mostrar para crear horarios
    document.getElementById("horarioContenedor").classList.remove("hidden");
    document.getElementById("horarioLista").innerHTML = "";
    generarHorarioGrilla();
  });

  //Listener una vez se le de en agregar nuevo horario
  document.getElementById("agregarHorario").addEventListener("click", () => {
    const dia = document.getElementById("dia").value;
    const inicio = document.getElementById("inicio").value;
    const fin = document.getElementById("fin").value;
    const doctorCedula = document.getElementById("doctor").value;
    let doctorNombre = "";
    for (let medico of medicos) {
      if (medico["cedula"] == doctorCedula) {
        doctorNombre = medico["nombre"];
      }
    }

    if (dia && inicio && fin) {
      // Convertir las horas a formato de 24 horas para comparar
      const horaInicio = parseInt(inicio.replace(":", ""), 10);
      const horaFin = parseInt(fin.replace(":", ""), 10);

      if (horaInicio >= horaFin) {
        alert("La hora de inicio debe ser menor que la hora de fin");
        return; // No continúa con la ejecución
      }
      const nuevoHorario = {
        cedula: doctorCedula,
        dia,
        inicio,
        fin,
        medico: doctorNombre,
      };

      // Verificar si ya existe un horario para el mismo doctor y día
      const indiceExistente = horariosDoctores.findIndex(
        (horario) => horario.cedula == doctorCedula && horario.dia === dia
      );

      if (indiceExistente !== -1) {
        // Reemplazar el horario existente
        horariosDoctores[indiceExistente] = nuevoHorario;
      } else {
        // Agregar el nuevo horario
        horariosDoctores.push(nuevoHorario);
      }

      generarHorarioGrilla();

      // Limpiar campos
      document.getElementById("dia").value = "";
      document.getElementById("inicio").value = "";
      document.getElementById("fin").value = "";
    } else {
      alert("Por favor, complete todos los campos del horario.");
    }
  });
});
