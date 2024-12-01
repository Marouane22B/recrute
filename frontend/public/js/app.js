async function registerUser() {
    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log(result);
}

document.getElementById('register-form').addEventListener('submit', (e) => {
    e.preventDefault();
    registerUser();
});
