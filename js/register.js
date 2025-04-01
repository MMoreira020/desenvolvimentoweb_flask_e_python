function validateForm() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    nameError.classList.add('d-none');
    emailError.classList.add('d-none');
    passwordError.classList.add('d-none');

    let isValid = true;

    if (!name) {
        nameError.textContent = 'Please enter your name.';
        nameError.classList.remove('d-none');
        isValid = false;
    }

    if (!email || !email.includes('@')) {
        emailError.textContent = 'Insira um e-mail válido.';
        emailError.classList.remove('d-none');
        isValid = false;
    }

    if (!password || password.length < 6) {
        passwordError.textContent = 'A senha deve ter pelo menos 6 caracteres.';
        passwordError.classList.remove('d-none');
        isValid = false;
    }

    return isValid;
}

// Atualiza o Token CSRF
fetch('/get-csrf-token')
    .then(response => response.json())
    .then(data => {
        document.querySelector('input[name="csrf_token"]').value = data.csrf_token;
    });