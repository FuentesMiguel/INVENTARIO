document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $('#dataTable').DataTable({
        processing: true,
        serverSide: false,
        ajax: {
            url: window.location.href,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            { data: 'name' },
            { data: 'container' },
            { data: 'quantity' },
            { data: 'total_weight' },
            { data: 'net_weight' },
            { data: 'actions', orderable: false, searchable: false },
        ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
        }
    });
});
