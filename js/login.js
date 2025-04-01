function validateForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    emailError.classList.add('d-none');
    passwordError.classList.add('d-none');

    if (!email || !email.includes('@')) {
        emailError.textContent = 'Insira um e-mail válido.';
        emailError.classList.remove('d-none');
        return false;
    }

    if (!password) {
        passwordError.textContent = 'Digite sua senha.';
        passwordError.classList.remove('d-none');
        return false;
    }

    return true;
}

// Atualiza o Token CSRF
fetch('/get-csrf-token')
    .then(response => response.json())
    .then(data => {
        document.querySelector('input[name="csrf_token"]').value = data.csrf_token;
    });