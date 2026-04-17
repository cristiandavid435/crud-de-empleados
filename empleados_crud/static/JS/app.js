// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 JavaScript cargado correctamente');

    // ============================================
    // MENÚ HAMBURGUESA
    // ============================================
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    console.log('Menú hamburguesa - Toggle:', navToggle);
    console.log('Menú hamburguesa - Menu:', navMenu);

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('show');
            console.log('✅ Menú toggled, clases:', navMenu.classList);
        });

        // Cerrar menú al hacer click en un enlace
        const navLinks = document.querySelectorAll('.nav_link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('show');
                console.log('✅ Menú cerrado al hacer click en enlace');
            });
        });

        // Cerrar menú al hacer click fuera
        document.addEventListener('click', function(e) {
            if (navMenu.classList.contains('show') && 
                !navMenu.contains(e.target) && 
                !navToggle.contains(e.target)) {
                navMenu.classList.remove('show');
                console.log('✅ Menú cerrado al hacer click fuera');
            }
        });
    } else {
        console.error('❌ No se encontraron elementos del menú hamburguesa');
    }

    // ============================================
    // FUNCIÓN PARA CALCULAR EL TOTAL DE LA NÓMINA
    // ============================================
    function calcularTotal() {
        const salarioInput = document.getElementById("id_salario_base");
        const horasInput = document.getElementById("id_horas_trabajadas");
        const bonificacionesInput = document.getElementById("id_bonificaciones");
        const descuentosInput = document.getElementById("id_descuentos");
        const totalInput = document.getElementById("id_total_pagar");

        if (salarioInput && horasInput && bonificacionesInput && descuentosInput && totalInput) {
            let salario = parseFloat(salarioInput.value) || 0;
            let horas = parseFloat(horasInput.value) || 0;
            let bonificaciones = parseFloat(bonificacionesInput.value) || 0;
            let descuentos = parseFloat(descuentosInput.value) || 0;

            let total = (salario * horas) + bonificaciones - descuentos;
            totalInput.value = total.toFixed(2);
            
            console.log('💰 Total calculado:', total.toFixed(2));
        }
    }

    // Detectar cambios en los campos de nómina
    const salarioBase = document.getElementById("id_salario_base");
    const horasTrabajadas = document.getElementById("id_horas_trabajadas");
    const bonificaciones = document.getElementById("id_bonificaciones");
    const descuentos = document.getElementById("id_descuentos");

    if (salarioBase) {
        salarioBase.addEventListener("input", calcularTotal);
        console.log('✅ Evento agregado a salario base');
    }
    if (horasTrabajadas) {
        horasTrabajadas.addEventListener("input", calcularTotal);
        console.log('✅ Evento agregado a horas trabajadas');
    }
    if (bonificaciones) {
        bonificaciones.addEventListener("input", calcularTotal);
        console.log('✅ Evento agregado a bonificaciones');
    }
    if (descuentos) {
        descuentos.addEventListener("input", calcularTotal);
        console.log('✅ Evento agregado a descuentos');
    }

    // ============================================
    // BÚSQUEDA EN TIEMPO REAL
    // ============================================
    const inputBuscar = document.getElementById('buscar');
    
    console.log('🔍 Input de búsqueda:', inputBuscar);

    if (inputBuscar) {
    inputBuscar.addEventListener('keyup', function () {
        const busqueda = this.value.toLowerCase().trim();
        const filas = document.querySelectorAll('tbody tr');

        filas.forEach(fila => {
            // Si no hay texto → mostrar todo
            if (busqueda === '') {
                fila.style.display = '';
                return;
            }

            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(busqueda) ? '' : 'none';
        });
    });
}


    // ============================================
    const botonesEliminar = document.querySelectorAll('.btn-eliminar');
    
    if (botonesEliminar.length > 0) {
        botonesEliminar.forEach(function(boton) {
            boton.addEventListener('click', function(e) {
                if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
                    e.preventDefault();
                    console.log('❌ Eliminación cancelada');
                } else {
                    console.log('✅ Eliminación confirmada');
                }
            });
        });
        console.log('✅ Confirmación de eliminación agregada a', botonesEliminar.length, 'botones');
    }

    const btnExportar = document.getElementById('exportarExcel');
    const fechaInicio = document.getElementById('fechaInicio');
    const fechaFin = document.getElementById('fechaFin');

    if (btnExportar) {
        btnExportar.addEventListener('click', () => {
            const inicio = fechaInicio?.value;
            const fin = fechaFin?.value;
            const tipo = btnExportar.dataset.tipo;

            // if (!inicio || !fin) {
            //     alert('Selecciona fecha inicio y fecha fin');
            //     return;
            // }

            if (inicio < fin || fin > inicio) {
                alert('La fecha de inicio debe ser mayor a la fecha de fin');
                return;
            }

            window.location.href =
                `/exportar_excel?tipo=${tipo}&fecha_inicio=${inicio}&fecha_fin=${fin}`;
        });
    }
});