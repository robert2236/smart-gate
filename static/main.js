const overlayStatus = document.getElementById('overlay-status');
const statusText = document.getElementById('status-text');
const statusName = document.getElementById('status-name');

let currentState = "ESPERANDO";

function updateStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            if (data.estado !== currentState || data.nombre !== statusName.innerText) {
                currentState = data.estado;
                
                // Reset classes
                overlayStatus.className = 'overlay-status';
                
                if (data.estado === 'AUTORIZADO') {
                    overlayStatus.classList.add('autorizado');
                    statusText.innerText = 'ACCESO PERMITIDO';
                    statusName.innerText = data.nombre;
                } else if (data.estado === 'DENEGADO') {
                    overlayStatus.classList.add('denegado');
                    statusText.innerText = 'ACCESO DENEGADO';
                    statusName.innerText = 'DESCONOCIDO';
                } else {
                    statusText.innerText = 'Escaneando Rostro...';
                    statusName.innerText = '';
                }
            }
        })
        .catch(err => console.error("Error fetching status:", err));
}

// Consultar el estado cada 500ms
setInterval(updateStatus, 500);
