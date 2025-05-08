// DOM Elements
const addModal = document.getElementById('addHoKhauModal');
const addForm = document.getElementById('addHoKhauForm');
const searchInput = document.getElementById('searchInput');

// Search functionality
searchInput.addEventListener('keyup', function() {
    const searchTerm = this.value.toLowerCase();
    const tableRows = document.querySelectorAll('.account-table tbody tr');

    tableRows.forEach(row => {
        const rowText = row.textContent.toLowerCase();
        if (rowText.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Modal functions
function openAddModal() {
    addModal.style.display = 'block';
    addForm.reset();
}

function closeAddModal() {
    addModal.style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target === addModal) {
        closeAddModal();
    }
};

// Form submission handling
addForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(addForm);

    fetch('/hokhau/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeAddModal();
            location.reload(); 
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Đã xảy ra lỗi khi thêm hộ khẩu');
    });
});

function deleteAccount(maHoKhau) {
    if (confirm('Bạn có chắc chắn muốn xóa hộ khẩu này?')) {
        fetch(`/hokhau/${maHoKhau}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Reload to update the table
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi xóa hộ khẩu');
        });
    }
}