document.addEventListener("DOMContentLoaded", function () {
    // Verifica se o Token está atualizando antes do logout
    document.querySelector("form").addEventListener("submit", function (e) {
        let csrfInput = document.querySelector('input[name="csrf_token"]');
        
        if (!csrfInput.value) {
            e.preventDefault();
            fetch("/get-csrf-token")
                .then(response => response.json())
                .then(data => {
                    csrfInput.value = data.csrf_token;
                    this.submit();
                });
        }
    });
});