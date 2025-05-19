function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function DeleteModalConfirm({ deleteUrl, objectName = 'element', tableId = 'dataTable' }) {
    Swal.fire({
        title: `¿Eliminar ${objectName}?`,
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
    }).then((result) => {
        if (result.isConfirmed) {
            const csrfToken = getCookie('csrftoken');
            fetch(deleteUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                Swal.fire('Eliminado', data.message, 'success');
                $('#' + tableId).DataTable().ajax.reload(null, false);
            })
            .catch(err => {
                Swal.fire('Error', 'No se pudo eliminar.', 'error');
                console.error(err);
            });
        }
    });
}
