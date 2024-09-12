function deleteClient(id) {
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

function deleteW(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/warehouses");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteOrder(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/orders");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteDriver(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/drivers");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteEmpl(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/employees");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteCons(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/consists");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteContract(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/contracts");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function deleteProduct(id) {
  fetch(id, {
    method: 'DELETE'
  }).then(response => {
        if (response.status == 204) {
            window.location.replace("/products");
        } else {
            alert('Ошибка при удалении');
        }
    });
}

function updateClient(event) {
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

function updateDriver(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            full_name: document.getElementById('full_name').value,
            phone_number: document.getElementById('phone_number').value,
            car_type: document.getElementById('car_type').value
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

function updateEmpl(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            full_name: document.getElementById('full_name').value,
            phone_number: document.getElementById('phone_number').value,
            email: document.getElementById('email').value,
            post: document.getElementById('post').value
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

function updateCons(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: document.getElementById('product_id').value,
            data: document.getElementById('data').value,
            order_amount: document.getElementById('order_amount').value,
            account_number: document.getElementById('account_number').value
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

function updateContract(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            contract_consist_id: document.getElementById('contract_consist_id').value,
            client_id: document.getElementById('client_id').value,
            employee_id: document.getElementById('employee_id').value
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

function updateProduct(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: document.getElementById('name').value,
            type: document.getElementById('type').value,
            price: document.getElementById('price').value,
            unit_type: document.getElementById('unit_type').value
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

function updateW(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            quantity: document.getElementById('quantity').value,
            address: document.getElementById('address').value,
            product_id: document.getElementById('product_id').value
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

function updateOrder(event) {
    event.preventDefault();
    fetch(window.location.href, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            contract_id: document.getElementById('contract_id').value,
            warehouse_id: document.getElementById('warehouse_id').value,
            driver_id: document.getElementById('driver_id').value,
            delivery_address: document.getElementById('delivery_address').value,
            prepayment: document.getElementById('prepayment').value,
            product_volume: document.getElementById('product_volume').value,
            status: document.getElementById('status').value
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
