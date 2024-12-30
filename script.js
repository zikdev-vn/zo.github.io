function setCookie(name, value, days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${encodeURIComponent(value)};expires=${date.toUTCString()};path=/`;
}

// Hàm lấy cookie
function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return decodeURIComponent(value);
        }
    }
    return null;
}

// Hàm thêm dữ liệu vào lịch sử
function addHistory(data) {
    const table = document.getElementById('history-table');
    const row = document.createElement('div');
    row.classList.add('row');

    data.forEach(item => {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.textContent = item;
        row.appendChild(cell);
    });

    table.appendChild(row);
}

// Hàm lưu dữ liệu
function saveData() {
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const balance = document.getElementById('balance').value;
    const backer = document.getElementById('backer').value;

    if (name && address && balance && backer) {
        const time = new Date().toLocaleString();
        const history = JSON.parse(getCookie('history') || '[]');
        history.push([history.length + 1, name, address, balance, backer, time]);
        setCookie('history', JSON.stringify(history), 7);

        // Thêm vào giao diện
        addHistory([history.length, name, address, balance, backer, time]);

        // Xóa dữ liệu sau khi lưu
        document.getElementById('name').value = '';
        document.getElementById('address').value = '';
        document.getElementById('balance').value = '';
        document.getElementById('backer').value = '';
    } else {
        alert('Vui lòng nhập đầy đủ thông tin!');
    }
}

// Hàm tải dữ liệu từ cookie khi mở trang
function loadHistory() {
    const history = JSON.parse(getCookie('history') || '[]');
    history.forEach(item => addHistory(item));
}

// Gắn sự kiện cho nút lưu
document.getElementById('save-btn').addEventListener('click', saveData);

// Tải lịch sử khi trang mở
window.onload = loadHistory;