async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const messageDiv = document.getElementById("message");
  
    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
  
      const result = await response.json();
  
      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = 'message success';
      } else {
        messageDiv.textContent = result.error;
        messageDiv.className = 'message error';
      }
    } catch (error) {
      messageDiv.textContent = 'Lỗi kết nối đến máy chủ.';
      messageDiv.className = 'message error';
    }
  }
  