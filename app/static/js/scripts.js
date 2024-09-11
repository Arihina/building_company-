function deleteEntry(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/clients");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function updateEntry(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            full_name: document.getElementById('full_name').value,
            phone_number: document.getElementById('phone_number').value,
            organization_name: document.getElementById('organization_name').value
        })
    }).then(response => {
        if (response.ok) {
            alert('Запись обновлена');
            window.location.reload();
        } else {
            alert('Ошибка при обновлении записи');
        }
    });
}
